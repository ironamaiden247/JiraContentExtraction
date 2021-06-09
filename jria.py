# python webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
driver = webdriver.Chrome(chrome_options=options)
driver.maximize_window()
driver.get(
    'https://issues.apache.org/jira/secure/BrowseProjects.jspa?selectedCategory=all&selectedProjectType=software&sortColumn=name&sortOrder=ascending&s=view_projects')
time.sleep(10)
len = 0
# projects= driver.find_elements_by_css_selector("ul.aui-nav>li")
projectlink = []
projectname = []
itemcount = []
# for project in projects :
#     tagid=project.get_attribute("id")
#     tagclassname=project.get_attribute("class")
#     # testing
#     # print(tagid)
#     # print(tagclassname)
#     # print(tagid.find("panel"))
#     # #//endttesting
#     if  tagid.find("panel") > 0 and tagclassname != "" :
#         atagbychild=project.find_elements_by_css_selector("a")
#         for child in atagbychild :
#             link.append(child.get_attribute("href"))
#             len=len+1
# time.sleep(20)
# for  eachlink in link :
#     driver.get(eachlink)
#     time.sleep(3)
i = 1
start = 1
projectco = 0

while (i < 6):
    print(i)
    link = "https://issues.apache.org/jira/secure/BrowseProjects.jspa?selectedCategory=all&selectedProjectType=all&sortColumn=name&sortOrder=ascending&s=view_projects&page=" + str(
        start)
    start = start + 1
    driver.get(link)
    time.sleep(5)
    protable = driver.find_elements_by_css_selector("div.p-list > table.aui")
    if protable:
        for portableone in protable:
            protbody = portableone.find_elements_by_css_selector("tbody.projects-list")
            for protbodyob in protbody:
                protr = protbodyob.find_elements_by_css_selector("tr")
                for tr in protr:
                    atagob = tr.find_elements_by_css_selector("td.cell-type-name > a")
                    for atag in atagob:
                        tdlink = atag.get_attribute("href")
                        tdtext = atag.text
                        projectlink.append(tdlink)
                        projectname.append(tdtext)
                        projectco = projectco + 1

    else:
        break
time.sleep(3)
print(projectco)
projectid = 0
with open('F:/jria.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['projectid', 'projectname',
                     'number of bugs that are closed and resolved and fixed.assign bug is not same as reporter',
                     'number of comments that are closed and resolved and fixed.assign bug is not same as reporter'])
    for project in projectlink:
        projectid = projectid + 1
        length = 0
        commentlen = 0
        driver.get(project)
        time.sleep(5)
        navigatebutob = driver.find_elements_by_css_selector('div#full-issue-navigator');
        for navigatebut in navigatebutob:
            atagob = navigatebut.find_elements_by_css_selector("a");
            for atag in atagob:
                print("passed")
                newlink = atag.get_attribute("href");
                driver.get(newlink)
                time.sleep(5)
                bugmenubutton = driver.find_element_by_xpath(
                    "//*[@id='content']/div[1]/div[3]/div/form/div[1]/div[1]/div[1]/div[1]/div/div[1]/ul/li[2]/div/div")
                bugmenubutton.click()
                print("butclick")
                try:
                    bugbutton = driver.find_element_by_xpath('//label[@data-descriptor-title="Bug"]')
                    bugbutton.click()
                except NoSuchElementException:
                    try:
                        bugbutton = driver.find_element_by_xpath('//label[@data-descriptor-title="Bug"]')
                        bugbutton.click()
                    except NoSuchElementException:
                        print("not found bug button")
                time.sleep(5)
                try:
                    statusmenubutton = driver.find_element_by_xpath(
                        '//*[@id="content"]/div[1]/div[3]/div/form/div[1]/div[1]/div[1]/div[1]/div/div[1]/ul/li[3]/div')
                    statusmenubutton.click()
                except NoSuchElementException:
                    print("no status menu button")
                try:
                    stabutton1 = driver.find_element_by_css_selector(
                        'li > label.item-label[data-descriptor-title="Resolved"]')
                    stabutton1.click()
                except NoSuchElementException:
                    print("not found status resolved")
                try:
                    stabutton2 = driver.find_element_by_xpath('//label[@data-descriptor-title="Closed"]')
                    stabutton2.click()
                except NoSuchElementException:
                    print("not found status closed")
                time.sleep(2)
                try:
                    resoultionmenubut = driver.find_element_by_xpath(
                        '//*[@id="content"]/div[1]/div[3]/div/form/div[1]/div[1]/div[1]/div[1]/div/div[2]/ul/li/div')
                    resoultionmenubut.click()
                except NoSuchElementException:
                    print("not found resoultionmenubut")
                try:
                    resolvebut = driver.find_element_by_xpath('//label[@data-descriptor-title="Fixed"]')
                    resolvebut.click()
                except NoSuchElementException:
                    print("not found resolution fixed")
                try:
                    unresolvebut = driver.find_element_by_xpath('//label[@title="Unresolved"]')
                    unresolvebut.click()
                except NoSuchElementException:
                    print("not found unreolved")
                if projectid == 1:
                    time.sleep(4)
                else:
                    time.sleep(2)
                resoultionmenubut.click()
                print(driver.current_url)
                try:
                    olem = driver.find_element_by_css_selector("div.list-content > ol.issue-list")
                    datakey = []
                    issues = olem.find_elements_by_css_selector("li")
                    for everyissue in issues:
                        datakeyval = everyissue.get_attribute("data-key")
                        print(datakeyval)
                        datakey.append(datakeyval)
                    for everykey in datakey:
                        print("everykey:" + everykey)
                        lielm = driver.find_element_by_xpath("//li[@data-key='" + everykey + "']")
                        driver.execute_script("arguments[0].click();", lielm)
                        time.sleep(2)
                        reporter = driver.find_element_by_xpath("//span[@id='assignee-val']").text
                        assign = driver.find_element_by_xpath("//span[@id='reporter-val']").text
                        try:
                            commentobar = driver.find_elements_by_xpath("//a[@title='Collapse comment']")
                            if reporter != assign:
                                for comment in commentobar:
                                    commentlen = commentlen + 1
                        except NoSuchElementException:
                            print("not found unreolved")
                        print("reporter:" + reporter)
                        print("assign:" + assign)
                        if reporter != assign:
                            length = length + 1
                    m = 1
                    page = 1
                    while (m < 6):
                        try:
                            page = page + 1
                            ahref = driver.find_element_by_xpath("//a[@data-page='" + str(page) + "']")
                            driver.execute_script("arguments[0].click();", ahref)
                            time.sleep(2)
                            olem = driver.find_element_by_css_selector("div.list-content > ol.issue-list")
                            datakey = []
                            issues = olem.find_elements_by_css_selector("li")
                            for everyissue in issues:
                                datakeyval = everyissue.get_attribute("data-key")
                                print(datakeyval)
                                datakey.append(datakeyval)
                            for everykey in datakey:
                                print("everykey:" + everykey)
                                try:
                                    lielm = driver.find_element_by_xpath("//li[@data-key='" + everykey + "']")
                                    driver.execute_script("arguments[0].click();", lielm)
                                except NoSuchElementException:
                                    print("no liitem")
                                time.sleep(4)
                                try:
                                    reporter = driver.find_element_by_xpath("//span[@id='assignee-val']").text
                                    assign = driver.find_element_by_xpath("//span[@id='reporter-val']").text
                                except NoSuchElementException:
                                    print("not compared")
                                try:
                                    commentobar = driver.find_elements_by_xpath("//a[@title='Collapse comment']")
                                    if reporter != assign:
                                        for comment in commentobar:
                                            commentlen = commentlen + 1
                                    print("commentlen:" + str(commentlen))
                                except NoSuchElementException:
                                    print("not found unreolved")
                                print("reporter:" + reporter)
                                print("assign:" + assign)
                                if reporter != assign:
                                    length = length + 1
                        except NoSuchElementException:
                            print("no more menu")
                            break

                except NoSuchElementException:
                    print("no project")
        print("length:" + str(length))
        print("commentlength:" + str(commentlen))
        writer.writerow([str(projectid), projectname[projectid - 1], str(length), str(commentlen)])
        itemcount.append(length)

driver.close()
