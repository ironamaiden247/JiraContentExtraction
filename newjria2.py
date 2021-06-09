# module import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import requests as req
import json

# webdrier configuration
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
driver = webdriver.Chrome(chrome_options=options)
driver.maximize_window()
driver.get(
    'https://issues.apache.org/jira/secure/BrowseProjects.jspa?selectedCategory=all&selectedProjectType=software&sortColumn=name&sortOrder=ascending&s=view_projects')
time.sleep(10)
len = 0
projectname = []
itemcount = []
i = 1
start = 1
apirequrl = ""
projectco = 0
projectkeyarr = []
# python selenium web scraping with chrome web driver to get project name  
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
                    projectkeyname = tr.find_element_by_css_selector("td.cell-type-key").text
                    projectkeyarr.append(projectkeyname)
                    for atag in atagob:
                        tdtext = atag.text
                        projectname.append(tdtext)
                        projectco = projectco + 1

    else:
        break
time.sleep(3)

driver.close()
index = 0
with open('D:/jria.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['projectid', 'projectname',
                     'number of bugs'])
    for projectkey in projectkeyarr:
        ## main result api request
        url = 'https://issues.apache.org/jira/rest/api/2/search?jql=issuetype=Bug%20and%20resolution=Fixed%20and%20status%20in%20(Resolved,%20Closed)%20and%20project=%22' + projectkey + '%22%20and%20assignee%20!=%20EMPTY&startAt=0&maxResults=50'
        respstr = req.get(url).content
        ##json_parsed data
        parsed_json = (json.loads(respstr))
        print(projectkey)
        print(index)
        project = projectname[index]
        index = index + 1
        totlen = parsed_json['total']
        i = 0
        start_at = 0
        maxlength = 50
        issuelength = 0
        while (i < 1):
            url = 'https://issues.apache.org/jira/rest/api/2/search?jql=issuetype=Bug%20and%20resolution=Fixed%20and%20status%20in%20(Resolved,%20Closed)%20and%20project=%22' + projectkey + '%22%20and%20assignee%20!=%20EMPTY&startAt=' + str(
                start_at) + '&maxResults=' + str(maxlength)
            respstr = req.get(url).content
            ##json_parsed data
            parsed_json = (json.loads(respstr))
            projissue = parsed_json['issues']
            for bug in projissue:
                field = bug['fields']
                assign = field['assignee']
                ass_disp = assign['displayName']
                reporter = field['reporter']
                try:
                    rep_name = reporter['displayName']
                except:
                    rep_name = ""
                if rep_name != ass_disp:
                    issuelength = issuelength + 1
            start_at = start_at + 50
            print("start_at:" + str(start_at))
            if (start_at > totlen):
                break
        print(issuelength)
        writer.writerow([index, project, issuelength])
