def makeSome(args):
  user = checkUser()
  
  try:
    import socket
    import urllib, urllib2
    import re
    socket.setdefaulttimeout(10)
    req = urllib2.Request('https://example.com/jira/secure/CreateIssueDetails.jspa', urllib.urlencode({'pid': '12345', 'issuetype': '3', 'priority': args['priority'], 'summary': args['summary'].encode('utf-8'), 'description': args['description'].encode('utf-8'), 'reporter': user.getName(), 'os_username': 'some-technical-account', 'os_password': 'some-technical-password'}), {'X-Atlassian-Token': 'no-check'})
    response = urllib2.urlopen(req)
    m = re.match('^.*(SOME-\d+)$', response.geturl())
    if m:
      return {'some': m.group(1)}
  except Exception, e:
    log.error(str(e))
    return {'some': None, 'error': str(e)}
    
  return {'some': None}


