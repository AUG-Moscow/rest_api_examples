$('#odkl-some-button').click(function(){
  var $button = $(this);
  JIRA.Loading.showLoadingIndicator();
  JIRA.SmartAjax.makeRequest({
    url: '/rest/jss/1.0/jython/invoke/makeSomeTask',
    type: 'POST',
    data: JSON.stringify({
      priority: 1,
      summary: $('#summary').val(),
      description: $('#description').val() || '';
    }),
    dataType: 'json',
    contentType: "application/json",
    complete: function(xhr, textStatus, smartAjaxResult){
      if(smartAjaxResult.successful){
        JIRA.Loading.hideLoadingIndicator();
        var data = smartAjaxResult.data;
        $('#create-issue-submit').removeAttr('disabled');
        $('<span class="aui-lozenge aui-lozenge-success">Внешняя таска создана</span>').insertAfter($button);
        $button.remove();
        var $desc = $('#description');
        $desc.val('By the task: '+data.some+$desc.val());
      }
    }
  });
});



