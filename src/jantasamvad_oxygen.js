// this script parses the data from https://coronabeds.jantasamvad.org/covid-info.js
const axios = require('axios');
const cheerio = require('cheerio');

var outputJsonArray = [];
var sheetsURL = "http://127.0.0.1:5000/updateBulk";
var srcURL = "https://oxygen.jantasamvad.org/";

axios({
  method: 'get',
  url: srcURL,
}).then(res => {
  // console.log(res.data);
  let outputJsonArray = [];
  const $ = cheerio.load(res.data);
  let dataRows = $("tbody tr");
  // console.log("Num entires == " + dataRows.length);
  for (let i = 0; i < dataRows.length; i++) {
    let row = dataRows[i];
    let columns = $(row).find("td");
    var rowJson = {};
    rowJson["Name"] = $(columns[1]).text().split("\n")[0].trim();
    let tel = $(columns[1]).find("a").attr("href");
    if (!!tel)
      rowJson["Contact"] = tel.replace("tel:", "");
    rowJson["Address"] = $(columns[2]).text().trim();
    let location = $(columns[2]).find("a");
    if (!!location)
      rowJson["URL"] = $(columns[2]).find("a").attr("href");

    outputJsonArray.push(rowJson);
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