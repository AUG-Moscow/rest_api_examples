(function($){

  JIRA.SmartAjax.makeRequest({
    url: '/rest/api/2/issue/'+JIRA.Issue.getIssueKey()+'/transitions',
    complete: function(xhr, textStatus, smartAjaxResult) {
      var transitions = smartAjaxResult.data.transitions;
      if(transitions.length){
        transitions.forEach(function(trans){
          $('#descriptionmodule').append('\
            <p>\
              Для перехода из '+trans.name+' в '+trans.to.name+' нажмите \
              <a class=wf-trans href=# wf-id='+trans.id+'>здесь</a>\
            </p>');
        });
      }
    }
  });

})(AJS.$);