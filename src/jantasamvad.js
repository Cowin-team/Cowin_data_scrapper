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
  console.log(covidFacilityData);
  // console.log(covidInfoData);
}