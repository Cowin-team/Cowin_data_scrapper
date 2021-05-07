// this script parses the data from https://coronabeds.jantasamvad.org/covid-info.js
const request = require('request')

var outputJsonArray = [];
var sheetsURL = "http://127.0.0.1:5000/update";
var apiInfoURL = "https://coronabeds.jantasamvad.org/covid-info.js";
var apiFacilitiesURL = "https://coronabeds.jantasamvad.org/covid-facilities.js";
var covidFacilityData = {};
var covidInfoData = {};

request(apiFacilitiesURL, function (
  error,
  response,
  body
) {
  covidFacilityData = body.split(" = ")[1].replace(";", "");
  covidFacilityData = JSON.parse(covidFacilityData);

  request(apiInfoURL, function (
    error,
    response,
    body
  ) {
    covidInfoData = body.split(" = ")[1].replace(";", "");
    covidInfoData = JSON.parse(covidInfoData);
    parseJSON();
  })
})

// parse the fetched data in the function below
function parseJSON() {
  // console.log(covidFacilityData);
  // console.log(covidInfoData);
  let bedData = covidInfoData["beds"];
  let oxygenBedData = covidInfoData["oxygen_beds"];
  let icuBedData = covidInfoData["covid_icu_beds"];
  let ventilatorData = covidInfoData["ventilators"];
  let icuWithouVentilator = covidInfoData["icu_beds_without_ventilator"]; // will add it to icubeddata

  for (let facilityName in covidFacilityData) {
    var rowJson = {};
    // console.log(facilityName);
    rowJson["Name"] = facilityName;
    rowJson["Address"] = covidFacilityData[facilityName]["address"];
    rowJson["Contact"] = covidFacilityData[facilityName]["contact_numbers"];
    rowJson["URL"] = covidFacilityData[facilityName]["location"];

    let date;
    if (!!bedData[facilityName]) {
      rowJson["COVID Beds"] = bedData[facilityName]["vacant"];
      date = bedData[facilityName]["last_updated_at"];
    }

    if (!!oxygenBedData[facilityName]) {
      rowJson["Oxygen Beds"] = oxygenBedData[facilityName]["vacant"];
      date = oxygenBedData[facilityName]["last_updated_at"];
    }

    if (!!icuBedData[facilityName]) {
      date = icuBedData[facilityName]["last_updated_at"];
      if (!!icuWithouVentilator[facilityName])
        rowJson["ICU"] = icuBedData[facilityName]["vacant"] + icuWithouVentilator[facilityName]["vacant"];
      else
        rowJson["ICU"] = icuBedData[facilityName]["vacant"];
    }
    if (!!ventilatorData[facilityName]) {
      rowJson["Ventilator Beds"] = ventilatorData[facilityName]["vacant"];
      date = ventilatorData[facilityName]["last_updated_at"];
    }

    if (!!date)
      rowJson["LAST UPDATED"] = new Date(date).toISOString();
    // console.log(rowJson);
    // console.log("====================================");
    outputJsonArray.push(rowJson);
  }
  console.log(outputJsonArray);

  // one time save to excel
  // const fs = require("fs")//npm install fs
  // var json2xls = require('json2xls');
  // var xls = json2xls(outputJsonArray);
  // fs.writeFileSync('data.xlsx', xls, 'binary');
}