// this script parses the data from covidpune.com
fetch("https://covidpune.com/data/covidpune.com/bed_data.json")
  .then(function (response) {
    return response.json();
  })
  .then(function (bedJson) {
    var outputJsonArray = [];
    for (var key in bedJson) {
      var rowJson = {};
      var rowdata = bedJson[key];
      rowJson["Name"] = rowdata["hospital_name"];
      rowJson["COVID_beds"] = rowdata["available_beds_without_oxygen"];
      rowJson["Oxygen_beds"] = rowdata["available_beds_with_oxygen"];
      rowJson["ICU"] = rowdata["available_icu_beds_without_ventilator"];
      rowJson["Ventilator_Beds"] = rowdata["available_icu_beds_with_ventilator"];
      rowJson["Contact"] = rowdata["hospital_phone"];
      rowJson["Area"] = rowdata["area"];
      rowJson["Hospital_category"] = rowdata["hospital_category"];
      rowJson["Last_updated"] = new Date(rowdata["last_updated_on"]).toLocaleString(undefined, {timeZone: 'Asia/Kolkata'});;
      outputJsonArray.push(rowJson);
    }
    console.log("outputJsonArray == " + JSON.stringify(outputJsonArray));
  })
  .catch(function (error) {
    console.log("Error: " + error);
  });