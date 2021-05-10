// this script parses the data from https://coronabeds.jantasamvad.org/covid-info.js
const axios = require('axios');
// const cheerio = require('cheerio');

var outputJsonArray = [];
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
    if (row["type"] == "Oxygen") {
      var rowJson = {};
      rowJson["Name"] = row["title"] + " : " + row["subtitle"];
      rowJson["Contact"] = row["contact"];
      rowJson["Source"] = row["sourcelink"];
      rowJson["Notes"] = row["notes"];
      outputJsonArray.push(rowJson);
    }
  }
  console.log(outputJsonArray);
  // callAPI(outputJsonArray);
  // const fs = require("fs") //npm install fs
  // const json2xls = require('json2xls');
  // const xls = json2xls(outputJsonArray);
  // fs.writeFileSync('data.xlsx', xls, 'binary');
}).catch(error => {
  console.error(error)
})

async function callAPI(oxygenData) {
  response = await fetch(sheetsURL, {
    method: 'POST', // or 'PUT'
    credentials: 'omit',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(oxygenData),
  })
  const message = await response.json();
  if (!response.ok) {
    console.log(`HTTP error! status: ${response.status} message: ${response.json()}`);
  } else {
    console.log(message)
  }
}