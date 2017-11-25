(function($){

  $('.wf-trans').on('click', function(){
    var wfId = $(this).attr('wf-id');
    JIRA.SmartAjax.makeRequest({
      url: '/rest/api/2/issue/'+JIRA.Issue.getIssueId()+'/transitions',
      type: 'POST',
      data: JSON.stringify({
        'transition' : { 'id': wfId }
      }),
      contentType: "application/json"
    });
  });

})(AJS.$);