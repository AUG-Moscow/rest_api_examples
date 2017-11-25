(function($){
  // Replace field to value getting from BASE project
  $('#customfield_10400').on('change', function(){
    var projectSelected = $(this).find(":selected").text();

    JIRA.SmartAjax.makeRequest({
      url: '/rest/api/2/search/',
      data: { jql: 'project = BASE and summary ~ "'+projectSelected+'"' },
      complete: function(xhr, textStatus, smartAjaxResult) {
        var issue = smartAjaxResult.data.issues[0];
        $('#customfield_10103').val(issue.fields.customfield_10101.name)
        
      }
    });
  });

})(AJS.$);