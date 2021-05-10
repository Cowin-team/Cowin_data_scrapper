// this script parses the data from https://coronabeds.jantasamvad.org/covid-info.js
const axios = require('axios');

var oxygen = [];
var medicine = [];
var doctor = [];
var helpline = [];
var plasma = [];
var hospital = [];
var meals = [];


var sheetsURL = "http://127.0.0.1:5000/updateBulk";
var srcURL = "https://resources.covidkashmir.org/_next/data/rcjyOrFHMzV5jsSPucGWC/index.json";

axios({
  method: 'get',
  url: srcURL,
}).then(res => {
  console.log(res.data);
  let outputJsonArray = [];
  let dataRows = res.data.pageProps.data;
  console.log("Num entires == " + dataRows.length);
  for (let i = 0; i < dataRows.length; i++) {
    let row = dataRows[i];
    var rowJson = {};
    rowJson["Name"] = row["title"] + " : " + row["subtitle"];
    rowJson["Contact"] = row["contact"];
    rowJson["Source"] = row["sourcetitle"] + " " + row["sourcelink"];
    rowJson["Notes"] = row["notes"];

    if (row["type"] == "Oxygen")
      oxygen.push(rowJson);
    if (row["type"] == "Medicine")
      medicine.push(rowJson);
    if (row["type"] == "Doctor")
      doctor.push(rowJson);
    if (row["type"] == "Helpline")
      helpline.push(rowJson);
    if (row["type"] == "Plasma")
      plasma.push(rowJson);
    if (row["type"] == "Hospital")
      hospital.push(rowJson);
    if (row["type"] == "Meal")
      meals.push(rowJson);
  }
  // console.log(oxygen);
  // callAPI(outputJsonArray);
  // const fs = require("fs") //npm install fs
  // const json2xls = require('json2xls');
  //
  // fs.writeFileSync('oxygen.xlsx', json2xls(oxygen), 'binary');
  // fs.writeFileSync('medicine.xlsx', json2xls(medicine), 'binary');
  // fs.writeFileSync('doctor.xlsx', json2xls(doctor), 'binary');
  // fs.writeFileSync('plasma.xlsx', json2xls(plasma), 'binary');
  // fs.writeFileSync('helpline.xlsx', json2xls(helpline), 'binary');
  // fs.writeFileSync('hospital.xlsx', json2xls(hospital), 'binary');
  // fs.writeFileSync('meals.xlsx', json2xls(meals), 'binary');

}).catch(error => {
  console.error(error)
})

async function callAPI(data) {
  response = await fetch(sheetsURL, {
    method: 'POST', // or 'PUT'
    credentials: 'omit',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
  const message = await response.json();
  if (!response.ok) {
    console.log(`HTTP error! status: ${response.status} message: ${response.json()}`);
  } else {
    console.log(message)
  }
}