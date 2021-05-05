// this script parses the data from covidpune.com
var outputJsonArray = [];
var url = "http://127.0.0.1:5000/update";
var xhr = new XMLHttpRequest();
fetch("https://covidpune.com/data/covidpune.com/bed_data.json")
  .then(function (response) {
    return response.json();
  })
  .then(function (bedJson) {

    for (var key in bedJson) {
      var rowJson = {};
      var rowdata = bedJson[key];
      rowJson["Name"] = rowdata["hospital_name"];
      rowJson["COVID Beds"] = rowdata["available_beds_without_oxygen"] + "/" + rowdata["total_beds_without_oxygen"];
      rowJson["Oxygen Beds"] = rowdata["available_beds_with_oxygen"] + "/" + rowdata["total_beds_with_oxygen"];
      rowJson["ICU"] = rowdata["available_icu_beds_without_ventilator"] + "/" + rowdata["total_icu_beds_without_ventilator"];
      rowJson["Ventilator Beds"] = rowdata["available_icu_beds_with_ventilator"] + "/" + rowdata["total_icu_beds_with_ventilator"];
      rowJson["Contact"] = rowdata["hospital_phone"];
      rowJson["Area"] = rowdata["area"];
      rowJson["Hospital Category"] = rowdata["hospital_category"];
      var date = rowdata["last_updated_on"];
      if (date > 0)
        rowJson["LAST UPDATED"] = new Date(rowdata["last_updated_on"]).toLocaleString(undefined, {timeZone: 'Asia/Kolkata'});
      else
        rowJson["LAST UPDATED"] = "Not available"
      rowJson["Sheet Name"] = "Pune Beds";
      outputJsonArray.push(rowJson);

      console.log(rowJson);
      xhr.open("POST", url, true);
      //Send the proper header information along with the request
      xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
      xhr.send(rowJson);
    }
    console.log(JSON.stringify(outputJsonArray));
  })
  .catch(function (error) {
    console.log("Error: " + error);
  });