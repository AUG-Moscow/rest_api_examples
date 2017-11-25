(function($){
  // Скрипт находит некоторые залинкованные таски, вытаскивает из них ассигнеров и рисует позади дескрипшна

  // найти у задачи все связи
  JIRA.SmartAjax.makeRequest({
    url: '/rest/api/2/issue/'+JIRA.Issue.getIssueKey(),
    data: {fields: ['issuelinks'] },
    complete: function(xhr, textStatus, smartAjaxResult) {
      var issuelinks = smartAjaxResult.data.fields.issuelinks;
      // если запрос вернул нам массив со связями, перебираем их
      if(issuelinks.length){
        issuelinks.forEach(function(link){
          // нам интересны только таски, прилинкованные inward связью
          if(link.inwardIssue){
            // к каждой связанной таске делаем запрос, дабы узнать номер, тему и исполнителя
            JIRA.SmartAjax.makeRequest({
              url: '/rest/api/2/issue/'+link.inwardIssue.key,
              data: {fields: ['summary', 'assignee']},
              complete: function(xhr, textStatus, smartAjaxResult){
                // разбираем поля по няшным переменным
                var issueKey = smartAjaxResult.data.key;
                var summary = smartAjaxResult.data.fields.summary;
                var assignee = smartAjaxResult.data.fields.assignee;
                // если у задачи есть исполнитель, сохраняем только ФИО
                if(assignee){
                  assignee = assignee['displayName'];
                }
                // если же задача неназначена, исполнитель будет null, а это смотрится некрасиво
                else{
                 assignee = 'неизвестен'
                }
                // Полученные данные пририсовываем в конце описания задачи
                $('#descriptionmodule').append('\
                  </p>\Прилинкованная таска: '+issueKey+': '+summary+'.\
                   Ведет ее сотрудник: '+assignee+'</p>')
              }
            });
          }        
        });
      }    
    }
  });
})(AJS.$);