'''
Script to scrap data pertaining to certain projects from Jira repository
'''

import requests as req
import json
import mysql.connector

# mysql connect part
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="bug_report"
)
mycursor = mydb.cursor()
projectkeys = ['GROOVY', 'HARMONY', 'CASSANDRA', 'INFRA',
               'CXF']  # append project keys of project whose information needs to be collected
# projectkeys.append('GROOVY')
# projectkeys.append('HARMONY')
# projectkeys.append('CASSANDRA')
# projectkeys.append('INFRA')
# projectkeys.append('CXF')
for projectkey in projectkeys:
    url = 'https://issues.apache.org/jira/rest/api/2/search?jql=issuetype=Bug%20and%20resolution=Fixed%20and%20status%20in%20(Resolved,%20Closed)%20and%20project=%22' + projectkey + '%22%20and%20assignee%20!=%20EMPTY&startAt=0&maxResults=50'
    respstr = req.get(url).content
    parsed_json = (json.loads(respstr))
    totlen = parsed_json['total']
    start_at = 0
    maxlength = 50
    issuelength = 0
    i = 0
    while (i < 1):
        url = 'https://issues.apache.org/jira/rest/api/2/search?jql=issuetype=Bug%20and%20resolution=Fixed%20and%20status%20in%20(Resolved,%20Closed)%20and%20project=%22' + projectkey + '%22%20and%20assignee%20!=%20EMPTY&startAt=' + str(
            start_at) + '&maxResults=' + str(maxlength)
        respstr = req.get(url).content
        ##json_parsed data
        parsed_json = (json.loads(respstr))
        projissue = parsed_json['issues']
        for bug in projissue:
            # apiurl=bug['self']
            # respstr_api=req.get(apiurl).content
            # api_parsed_json = (json.loads(respstr_api))
            # bugkey=""
            field = bug['fields']
            assign = field['assignee']
            ass_disp = ""
            rep_name = ""
            try:
                ass_disp = assign['displayName']
            except:
                ass_disp = ""
            reporter = field['reporter']
            try:
                rep_name = reporter['displayName']
            except:
                rep_name = ""
            if rep_name != ass_disp:
                apiurl = bug['self']
                respstr_api = req.get(apiurl).content
                api_parsed_json = (json.loads(respstr_api))
                print(apiurl)
                print(api_parsed_json)
                bugkey = ""
                try:
                    bugkey = api_parsed_json['key']
                except:
                    bugkey = ""
                fields = api_parsed_json['fields']
                try:
                    bugname = fields['summary']
                except:
                    bugname = ""
                print(bugname)
                try:
                    priority = fields['priority']
                    try:
                        priorityname = priority['name']
                    except:
                        priorityname = ""
                except:
                    priorityname = ""
                print("priorityname:" + priorityname)
                try:
                    status = fields['status']
                    try:
                        statusname = status['name']
                    except:
                        statusname = ""
                except:
                    statusname = ""
                print("statusname:" + statusname)
                try:
                    affect_version = fields['versions']
                    try:
                        affect_versionname = affect_version[0]['name']
                    except:
                        affect_versionname = ""
                except:
                    affect_versionname = ""
                print("affect_versionname:" + affect_versionname)
                try:
                    resolution = fields['resolution']
                    try:
                        resolutionname = resolution['name']
                    except:
                        resolutionname = ""
                except:
                    resolutionname = ""
                print("resolutionname:" + resolutionname)
                try:
                    fix_version = fields['fixVersions']
                    try:
                        fix_version_name = fix_version[0]['name']
                    except:
                        fix_version_name = ""
                except:
                    fix_version_name = ""
                print("fix_version_name:" + fix_version_name)
                try:
                    components = fields['components']
                    compontstr = ""
                    m = 0
                    for component in components:
                        m = m + 1
                        if m == len(components):
                            compontstr = compontstr + component['name']
                        else:
                            compontstr = compontstr + component['name'] + ","

                except:
                    compontstr = ""
                print("components:" + compontstr)

                labels = fields['labels']
                labelstr = ""
                j = 0
                for label in labels:
                    j = j + 1
                    if j == len(labels):
                        labelstr = labelstr + label
                    else:
                        labelstr = labelstr + label + ","

                    labelstr = ""
                print("label:" + labelstr)
                environmentstr = ""
                try:
                    environment = fields['environment']
                except:
                    environment = ""
                environmentstr = str(environment)
                print("environment:" + environmentstr)
                try:
                    assign = fields['assignee']
                    try:
                        assignname = assign['name']
                    except:
                        assignname = ""
                except:
                    assignname = ""
                print("assignname:" + str(assignname))
                try:
                    reporter = fields['reporter']
                    try:
                        reportername = reporter['name']
                    except:
                        reportername = ""
                except:
                    reportername = ""
                print("reportername:" + reportername)
                try:
                    votes = fields['votes']
                    try:
                        votecount = votes['votes']
                    except:
                        votecount = 0
                except:
                    votecount = 0
                print("votecount:" + str(votecount))
                try:
                    watches = fields['watches']
                    try:
                        watchCount = watches['watchCount']
                    except:
                        watchCount = 0
                except:
                    watchCount = 0
                print("watchCount" + str(watchCount))
                try:
                    description = str(fields['description'])
                except:
                    description = ""
                print("description:" + description)
                try:
                    date_create = fields['created']
                except:
                    date_create = ""
                print("date_create:" + date_create)
                try:
                    date_resolution = fields['resolutiondate']
                except:
                    date_resolution = ""
                print("date_resolution" + date_resolution)
                commenter = []
                commentcon = []
                idarray = ""
                try:
                    comment = fields['comment']
                    comments = comment['comments']
                    for evcomment in comments:
                        authorname = evcomment['author']['name']
                        commentcontent = evcomment['body']
                        crdatetime = evcomment['created']
                        commenter.append(authorname)
                        commentcon.append(commentcontent)
                        sql = "INSERT INTO comments (bugid,commenter,comment,codatetime) VALUES (%s, %s,%s,%s)"
                        val = (bugkey, authorname, commentcontent, crdatetime)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        lastid = mycursor.lastrowid
                        idarray = idarray + str(lastid) + ","
                except:
                    print("no issue")
                sql1 = "INSERT INTO bugs (projectname,bugid,bugtitle,priority,status,resolution,affect_version,components,fixversion,labels,environment,assignee,reporter,votes,watchers,date_time_created,date_time_resolved,description,comments) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val1 = (
                    projectkey, bugkey, bugname, priorityname, statusname, resolutionname, affect_versionname,
                    compontstr,
                    fix_version_name, labelstr, environmentstr, assignname, reportername, str(votecount),
                    str(watchCount),
                    date_create, date_resolution, description, idarray)
                mycursor.execute(sql1, val1)
                mydb.commit()
        start_at = start_at + 50
        print("start_at:" + str(start_at))
        if (start_at > totlen):
            break
