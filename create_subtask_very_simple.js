(function($){
  
  JIRA.SmartAjax.makeRequest({
    url: '/rest/api/2/issue',
    type: 'POST',
    data: JSON.stringify({
      'fields': {
        'project': {'id': '10704'},
        'issuetype': {'id': '5'},
        'summary': 'My Test Task',
        'description': 'Test description',
        'parent': {'id': JIRA.Issue.getIssueKey()}
      }
    }),
    dataType: 'json',
    contentType: "application/json"
  });

})(AJS.$);