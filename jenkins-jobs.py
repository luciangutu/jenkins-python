import jenkins
from datetime import datetime
from credentials import username, password, jenkins_url

server = jenkins.Jenkins(jenkins_url, username=username, password=password)

jobs = server.get_jobs()
#print('{:<40s}{:<85s}{:<10s}{:>8}{:^25s}{:<20s}{:<25s}'.format("Build Name", "URL", "Status", "Number", "Date", "UserName", "Node"))
print('{},{},{},{},{},{},{}'.format("Build Name", "URL", "Status", "Number", "Date", "UserName", "Node"))

for job in jobs:
    job_info = server.get_job_info(job['name'])

    if 'lastSuccessfulBuild' in job_info and job_info['lastSuccessfulBuild']:
        job_number = job_info['lastSuccessfulBuild']['number']
    else:
        job_number = 0

    # ignore builds that were never run
    if job_number == 0:
        continue
    build_info = server.get_build_info(job['name'], job_number)

    jname = job['name']
    jurl = job['url']
    #jstatus = job.get('color', 'N/A')
    jstatus = build_info['result']

    # ignore some broken dicts that don't have the causes or userName part
    if 'causes' in build_info['actions'][1] and 'userName' in build_info['actions'][1]['causes'][0]:
        juser = build_info['actions'][1]['causes'][0]['userName']
    else:
        juser = "N/A"

    jnode = build_info.get('builtOn', 'N/A')


    jdate = datetime.utcfromtimestamp(build_info['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
    #print('{:<40s}{:<85s}{:<10s}{:>8}{:^25s}{:<20s}{:<25s}'.format(jname, jurl, jstatus, job_number, jdate, juser, jnode))
    print('{},{},{},{},{},{},{}'.format(jname, jurl, jstatus, job_number, jdate, juser, jnode))
