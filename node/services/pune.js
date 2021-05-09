// this script parses the data from covidpune.com

const fetch = require("node-fetch");
const moment = require("moment");


async function fetchData(url = "https://covidpune.com/data/covidpune.com/bed_data.json") {
  
  var outputJsonArray = [];
  
  let response = await fetch(url)
  
  console.log(response.status); // 200
  console.log(response.statusText); // OK

  if (!response.ok) {
    console.log(`HTTP error! status: ${response.status} message: ${response.json()}`);
  } else {
    let bedJson = await response.json();
    for (var key in bedJson) {
      var rowJson = {};
      var rowdata = bedJson[key];
      rowJson["Name"] = rowdata["hospital_name"];
      rowJson["COVID Beds"] = rowdata["available_beds_without_oxygen"];
      rowJson["Oxygen Beds"] = rowdata["available_beds_with_oxygen"];
      rowJson["ICU"] = rowdata["available_icu_beds_without_ventilator"];
      rowJson["Ventilator Beds"] = rowdata["available_icu_beds_with_ventilator"];
      rowJson["Contact"] = rowdata["hospital_phone"];
      rowJson["Area"] = rowdata["area"];
      rowJson["Hospital Category"] = rowdata["hospital_category"];
      var date = rowdata["last_updated_on"];
      if (date > 0) {
        date = new Date(date); // Or the date you'd like converted.
        date = new Date(date).toLocaleString(undefined, {timeZone: 'Asia/Kolkata'});
        date = moment(date).format('YYYY-MM-DD HH:mm:ss');
        rowJson["LAST UPDATED"] = date;
        rowJson["Check LAST UPDATED"] = true;
      } else {
        rowJson["Check LAST UPDATED"] = false;
      }
      rowJson["Sheet Name"] = "Pune Beds";
      outputJsonArray.push(rowJson);
    }
  }
  return outputJsonArray ;
}

exports.fetchData = fetchData;