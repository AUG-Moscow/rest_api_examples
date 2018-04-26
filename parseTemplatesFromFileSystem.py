def parseIssueDocument(args):
  user = checkUser()
  if args and 'issue' in args and 'template' in args and 'map' in args:
    try:
      permissionManager = ComponentAccessor.getPermissionManager()
      issueManager = ComponentAccessor.getIssueManager()

      issue = issueManager.getIssueByCurrentKey(args['issue'])
      if issue:
        if not permissionManager.hasPermission(ProjectPermissions.WORK_ON_ISSUES, issue, user):
          raise Exception("You haven't permissions in %s " % args['issue'])
        valuesMap = args['map']
        template = JythonUtil.getJythonPath()+'/templates/'+args['template']
        if os.path.isfile(template):
          text = open(template, 'r').read()
          for replaceKey, replaceText in valuesMap.items():
            # skip empty values
            if len(replaceText) > 0:
              replaceText = replaceText.encode('utf8')
              text = text.replace(replaceKey, str(replaceText))
          # unparsed keys will be blank strings 
          text = re.sub(r'\$\{.*\}', '', text) 

          return {'result': True, 'doc': text.decode('utf-8')}

    except Exception, e:
      log.error(str(e))
      return {'result': False, 'error': str(e)}

  return {'result': False}

