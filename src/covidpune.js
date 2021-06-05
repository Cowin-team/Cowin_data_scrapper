// this script parses the data from covidpune.com
var outputJsonArray = [];
var url = "http://127.0.0.1:5000/updateBulk";
fetch("https://covidpune.com/data/covidpune.com/bed_data.json")
  .then(function (response) {
    return response.json();
  })
  .then(function (bedJson) {

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
      rowJson["Address"] = rowJson["Name"]+', '+ rowJson["Area"]+', Pune, Maharashtra, India' 
      rowJson["Sheet Name"] = "Pune Beds";
      outputJsonArray.push(rowJson);
    }
    callAPI(outputJsonArray);
  })
  .catch(function (error) {
    console.log("Error: " + error);
  });


async function callAPI(bedData) {
  response = await fetch(url, {
    method: 'POST', // or 'PUT'
    credentials: 'omit',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(bedData)
  })
  const message = await response.json();
  console.log(message)
  if (!response.ok) {
    console.log(`HTTP error! status: ${response.status} message: ${response.json()}`);
  } else {
    console.log(message)
  }
}
