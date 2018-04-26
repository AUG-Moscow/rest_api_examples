def stash(args):
  user = checkUser()
  
  try:
    from java.net import URLEncoder
    from com.atlassian.jira.component import ComponentAccessor
    from com.atlassian.sal.api.net.Request import MethodType

    componentClassManager = ComponentAccessor.getComponentClassManager()
    ApplicationId = componentClassManager.loadClass('com.atlassian.applinks.api.ApplicationId')
    ApplicationLinkResponseHandler = componentClassManager.loadClass('com.atlassian.applinks.api.ApplicationLinkResponseHandler')
    ApplicationLinkService = componentClassManager.loadClass('com.atlassian.applinks.api.ApplicationLinkService')
    
    appLinkService = ComponentAccessor.getComponentOfType(ApplicationLinkService)
    appLink = appLinkService.getApplicationLink(ApplicationId('12345678-abcd-90ef-123a-4b567c89e012'))
    req = None

    if args['method'] == 'createpullrequest' and 'review' in args:
      project = args['review']['project']
      repo = URLEncoder.encode(args['review']['repo'])
      url = '/rest/api/1.0/projects/%s/repos/%s/pull-requests' % (project, repo)
      title = '%s %s' % (args['review']['key'], args['review']['summary'])
      payload = {
        'title': title[:255], 
        'description': None, 
        'state': 'OPEN', 
        'open': True, 
        'closed': False, 
        'fromRef': {
          'id': 'refs/heads/%s' % args['review']['branch'], 
          'repository': {
            'slug': args['review']['repo'], 
            'name': None, 
            'project': {'key': project}
          }
        }, 
        'toRef': {
          'id': 'refs/heads/master',
          'repository': {
            'slug': args['review']['repo'], 
            'name': None, 'project': {'key': project}
          }
        }, 
        'reviewers': [{'user': {'name': u}} for u in list(set(args['review']['reviewers'])) if u != '']
      }
      req = appLink.createAuthenticatedRequestFactory().createRequest(MethodType.POST, url)
      req.setHeader('Content-Type', 'application/json; charset=UTF-8')
      req.setRequestBody(json.dumps(payload))
  
  except Exception, e:
    log.error(str(e))
    return {'result': False, 'error': str(e)}