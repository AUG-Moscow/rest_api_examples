 $context.find('#odkl-print-ref').on('click', function(){
    var createdMoment = moment($('#created-val .livestamp').attr('datetime'));
    var jiraUserTZOffset = createdMoment.parseZone().zone();
    var valuesMap = {
      '${issueKey}': issueKey,
      '${clientLegalAddress}': $('#customfield_10110-val').text().trim(),
      '${clientINN}': $('#customfield_10237-val').text().trim(),
      '${clientCompany}': $('#summary-val').text().trim(),
      '${signDate}': createdMoment.zone(jiraUserTZOffset).format('DD.MM.YYYY'),
      '${clientPerson}': $('#customfield_10101-val').text().trim(),
      '${clientPersonOccupation}': $('#customfield_10102-val').text().trim()
    };
    if($('#customfield_11309-val').text().trim() == 'есть') {
      valuesMap['${clientCountry}'] = $('#customfield_10413-val').text().trim();
    }

    var printScreen = window.open();
    JIRA.SmartAjax.makeRequest({
      url: '/rest/jss/1.0/jython/invoke/parseIssueDocument',
      type: 'POST',
      contentType: "application/json",
      data: JSON.stringify({
        'issue': issueKey,
        'template': 'DOC_ner_reference_template.html',
        'map': valuesMap
      }),
      complete: function(xhr, textStatus, smartAjaxResult) {
        if(smartAjaxResult.successful && smartAjaxResult.data.result) {
          var docText = smartAjaxResult.data.doc;
          printScreen.document.write(docText); 
          printScreen.document.title = document.title;
        }
        else {
          printScreen.close()
          JIRA.Messages.showErrorMsg('Не получилось загрузить справку. Пожалуйста, обратитесь к администратору.')
        }
      }
    });
  }); 