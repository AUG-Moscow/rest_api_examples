(function($){
  // Print voters on the issue screen after description field
  JIRA.SmartAjax.makeRequest({
    url: '/rest/api/2/issue/'+JIRA.Issue.getIssueKey()+'/votes',    
    complete: function(xhr, textStatus, smartAjaxResult){
      var voters = smartAjaxResult.data.voters;
      if(voters && voters.length){
        voters.forEach(function(voter){
          $('#descriptionmodule').append('\
            <p>Сотрудник '+voter.displayName+' одобряэ</p>\
            ');
        });
      }
    }
  });
  
})(AJS.$);

