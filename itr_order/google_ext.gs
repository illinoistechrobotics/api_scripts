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
  var row, resp, rc, rdata;
  for (var i = 1; i <= numRows; i++) {
      row = sheet.getRange(dataRange.getCell(i,1).getRow(), 1, 1, 12)
      Logger.log(row.getBackground());
    if(row.getBackground() == '#00ff00'){
      resp = doPost(JSON.stringify(row.getValues()[0]));
      rc = resp.getResponseCode();
      if(rc == 200 || rc == 201){
        rdata = JSON.parse(resp.getContentText());
        //Logger.log(resp.getContentText());
        Browser.msgBox('Order list change on row '+String(row.getRow())+" accepted.", Browser.Buttons.OK);
        row.setBackground('#9900FF');
      } else if(rc == 400){
        rdata = JSON.parse(resp.getContentText());
        //Logger.log(resp.getContentText());
        Browser.msgBox('Please correct the following issues on row '+String(row.getRow())+":\n"+rdata.message, Browser.Buttons.OK);
        row.setBackground('#FF0000');
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
  return response;
}

