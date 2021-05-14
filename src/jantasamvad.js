// this script parses the data from https://coronabeds.jantasamvad.org/covid-info.js
const request = require('request')
const moment = require('moment')
const fetch = require("node-fetch");

var outputJsonArray = [];
var sheetsURL = "http://127.0.0.1:5000/updateBulk";
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
    //rowJson["Contact"] = covidFacilityData[facilityName]["contact_numbers"];
    rowJson["URL"] = covidFacilityData[facilityName]["location"];
    rowJson["Sheet Name"] = "Delhi Beds"
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

    if (!!date) {
      date = date.split(",");
      date = new Date(date[1] + " 2021 " + date[0]);
      date = moment(date).format('YYYY-MM-DD HH:mm:ss');
      rowJson["LAST UPDATED"] = date;
    }
    rowJson["Check LAST UPDATED"] = false;
    outputJsonArray.push(rowJson);
  }
   callAPI(outputJsonArray);
  console.log(outputJsonArray);
  // one time save to excel
  // const fs = require("fs")//npm install fs
  // var json2xls = require('json2xls');
  // var xls = json2xls(outputJsonArray);
  // fs.writeFileSync('data.xlsx', xls, 'binary');
}

async function callAPI(bedData) {
  response = await fetch(sheetsURL, {
    method: 'POST', // or 'PUT'
    credentials: 'omit',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(bedData),
  })
  const message = await response.json();
  if (!response.ok) {
    console.log(`HTTP error! status: ${response.status} message: ${response.json()}`);
  } else {
    console.log(message)
  }
}
