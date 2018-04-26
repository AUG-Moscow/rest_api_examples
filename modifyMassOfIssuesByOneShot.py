
def clearFieldsForUser(args):
  actor = checkUser()

  if not ComponentAccessor.getGroupManager().isUserInGroup(actor, 'jira-background-services'):
    return { 'result': False, 'error': 'This action allows only for special technical accounts' }
  
  if not (args and 'username' in args and 'project' in args):
    return { 'result': False, 'error': 'Not enought arguments, please put "username" and "project" both'}

  try:
    from com.atlassian.jira.component import ComponentAccessor
    from com.atlassian.jira.bc.issue.search import SearchService
    from com.atlassian.jira.web.bean import PagerFilter
    from com.atlassian.jira.event.type import EventDispatchOption

    customFieldManager = ComponentAccessor.getCustomFieldManager()
    searchService = ComponentAccessor.getComponent(SearchService)
    issueManager = ComponentAccessor.getIssueManager()
    issueService = ComponentAccessor.getIssueService()

    query = "project = %s and reporter = %s and type = "Data" and resolution is not Empty and updated <= startOfMonth()" % (args['project'], args['username'])
    returnData = { 'result': True, 'issues': [] }
    
    cfIds = [10501, 10502, 10503]
    customfields = []
    for cfId in cfIds:
      customField = customFieldManager.getCustomFieldObject(cfId)
      if customField:
        customfields.append(customField)
    
    parseResult = searchService.parseQuery(actor, query)
    if parseResult.isValid():
      results = searchService.search(actor, parseResult.getQuery(), PagerFilter(100))
      if results.getTotal() > 0:
        issues = results.getIssues()
        for issue in issues:
          issueKey = issue.getKey()
          issue = issueManager.getIssueObject(issueKey) # get mutable issue
          issueInputParameters = issueService.newIssueInputParameters()
          description = issue.getDescription() or ''
          description = description + u'\n\n\n*Additional information:*\n{panel}'
          for cf in customfields:
            cfName = cf.getName()
            cfType = cf.getCustomFieldType().getName()
            cfValue = issue.getCustomFieldValue(cf)
            if cfValue:
              if cfType == 'Checkboxes':
                cfValue = str(cfValue).encode('utf-8')
              if cfType == 'User Picker (single user)':
                cfValue = cfValue.getKey()
              description = str(description) + '\n' + str(cfName) + ': ' + str(cfValue)
              issue.setCustomFieldValue(cf, None)
          description = description + '{panel}\n'
          # change issue
          issue.setDescription(str(description).decode('utf-8'))
          issueManager.updateIssue(actor, issue, EventDispatchOption.ISSUE_UPDATED, False)
          returnData['issues'].append(issueKey)

    return results

  except Exception, e:
    return { 'result': False, 'error': 'Procedure has been failed, reason: %s' % str(e) }