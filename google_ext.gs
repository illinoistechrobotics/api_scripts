var header_sz = 3;

function onEdit(e){
  var sheet = e.range.getSheet();
  var range = e.range;
  if(range.getRow() <= header_sz){
    return;
  }
  var dataRange = sheet.getRange(range.getRow(),1,(range.getLastRow()-range.getRow()+1),12)
  handleEdit(dataRange);
}
function onChange(e){
  var range = SpreadsheetApp.getActiveRange();
  if(range.getRow() <= header_sz){
    return;
  }
  var sheet = range.getSheet();
  var dataRange = sheet.getRange(range.getRow(),1,(range.getLastRow()-range.getRow()+1),12)
  handleEdit(sheet,dataRange);
}

function handleEdit(sheet, dataRange){
  var numRows = dataRange.getNumRows();
  var row, resp;
  for (var i = 1; i <= numRows; i++) {
      row = sheet.getRange(dataRange.getCell(i,1).getRow(), 1, 1, 12)
      Logger.log(row.getBackground());
    if(row.getBackground() == '#00ff00'){
      resp = doPost(JSON.stringify(row.getValues()[0]));
      if(resp == 200){
        resp = row.setBackground('#9900FF');
      } else if(resp == 400){
        resp = row.setBackground('#FF0000');
     }
  }
 }
}
function doPost(str){
  var headers = { 
    "Authorization" : "Basic <AUTHSTR>"
  };

  var options =
   {
     "contentType" : "application/json",
     "method" : "post",
     "headers" : headers,
     "payload" : str,
     "muteHttpExceptions" : true
   };

  var response = UrlFetchApp.fetch("https://kaminski.pw/order_list/api/v1/itr_order", options);
  Logger.log(response.getResponseCode());
  return response.getResponseCode();
}

