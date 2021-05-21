// this script parses the data from covidtelangana.com
var outputJsonArray = [];
var url = "http://127.0.0.1:5000/updateBulk";
fetch("https://covidtelangana.com/data/covidtelangana.com/bed_data.json")
  .then(function (response) {
    return response.json();
  })
  .then(function (bedJson) {
    let list = ['Karimnagar', 'Hyderabad', 'Warangal Urban', 'Siddipet', 'Jangaon', 'Adilabad', 'Badradri', 'Jagtial'];
    for (var key in bedJson) {
      if (list.includes(bedJson[key]["area"])){
      var rowJson = {};
      var rowdata = bedJson[key];
      rowJson["Name"] = rowdata["hospital_name"];
      rowJson["COVID Beds"] = rowdata["available_beds_without_oxygen"];
      rowJson["Oxygen Beds"] = rowdata["available_beds_with_oxygen"];
      rowJson["ICU"] = "N/A";//rowdata["available_icu_beds_without_ventilator"];
      rowJson["Ventilator Beds"] = rowdata["available_icu_beds_with_ventilator"];
      rowJson["Contact"] = rowdata["hospital_phone"];
      rowJson["Area"] = rowdata["area"];
      rowJson["Hospital Category"] = rowdata["hospital_category"];
      rowJson["Address"] = rowdata["hospital_name"] +', '+ rowdata["area"]+", Telengana"
      var date = rowdata["last_updated_on"];
      console.log(date)
      if (date > 0) {
        date = new Date(date); // Or the date you'd like converted.
        date = new Date(date).toLocaleString(undefined, {timeZone: 'Asia/Kolkata'});
        date = moment(date).format('YYYY-MM-DD HH:mm:ss');
        rowJson["LAST UPDATED"] = date;
        rowJson["Check LAST UPDATED"] = true;
      } else {
        rowJson["Check LAST UPDATED"] = false;
      }
      rowJson["Sheet Name"] = rowdata["area"]+" Beds";
      outputJsonArray.push(rowJson);
    }
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
