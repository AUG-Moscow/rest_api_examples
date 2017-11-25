import requests, json

dutyPerson = 'get-me-from-anywhere'
jiraURL = 'https://jira.example.com'
jiraLogin = 'somebody'
jiraPass = 'somepass'

# get authorized jira connection
session = requests.session()
auth_connect = session.post(jiraURL+'/rest/auth/1/session', 
  data=json.dumps({
    'username': jiraLogin, 
    'password': jiraPass
  }), 
  headers={
    'Content-type': 'application/json', 
    'X-Atlassian-Token': 'no-check'
  }, 
  verify=False)

# put new email attribute
jiraChAttr = session.put(
  jiraURL+'/rest/api/2/myself', 
  data=json.dumps({
    'password': jiraPass, 
    'emailAddress': dutyPerson+'@dummy.example.com'
    }),  
  headers={
  'Content-type': 'application/json'
  }, 
  verify=False)

# print if ok or not
if jiraChAttr.status_code == 200:
  print '[OK] Username %s has been set as %s' 
  % (dutyPerson, jiraLogin)
else:
  raise Exception('Returned code %s, reason: %s' 
    % (jiraChAttr.status_code, jiraChAttr.text))
