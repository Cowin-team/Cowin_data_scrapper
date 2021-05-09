// this script parses the data from http://dashboard.covid19.ap.gov.in/ims/hospbed_reports/ using their /process.php API
const axios = require('axios');
const cheerio = require('cheerio');
const fetch = require("node-fetch");
const moment = require('moment');
const qs = require('qs')
const phpApiUrl = "http://dashboard.covid19.ap.gov.in/ims/hospbed_reports/process.php";
const sheetsURL = "http://127.0.0.1:5000/updateBulk";

const districtIdMap = {
  "Anantapur Beds": 502, "Chittoor Beds": 503, "East godavari Beds": 505, "Guntur Beds": 506, "Krishna Beds": 510,
  "Kurnool Beds": 511, "Prakasam Beds": 517, "Spsr nellore Beds": 515, "Srikakulam Beds": 519,
  "Visakhapatanam Beds": 520, "Vizianagaram Beds": 521, "West godavari Beds": 523, "Ysr Beds": 504
}

for (let sheetName in districtIdMap) {
  let districtId = districtIdMap[sheetName];
  axios({
    method: 'post',
    url: phpApiUrl,
    data: qs.stringify({
      hospdata: 1,
      district: districtId
    }),
    headers: {
      'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
  }).then(res => {
    // console.log(res.data);
    let outputJsonArray = [];
    const $ = cheerio.load(res.data);
    let dataRows = $("tbody tr");
    console.log("Num entires == " + dataRows.length);
    for (let i = 0; i < dataRows.length; i++) {
      let row = dataRows[i];
      let columns = $(row).find("td");
      var rowJson = {};
      rowJson["Name"] = $(columns[1]).text().trim();
      rowJson["COVID Beds"] = $(columns[12]).text().trim();
      rowJson["Oxygen Beds"] = $(columns[9]).text().trim();
      rowJson["ICU"] = $(columns[6]).text().trim();
      rowJson["Ventilator Beds"] = $(columns[13]).text().trim();
      rowJson["Contact"] = $(columns[2]).text().trim();
      let date = new Date().toLocaleString(undefined, {timeZone: 'Asia/Kolkata'})
      date = moment(date).format('YYYY-MM-DD HH:mm:ss');
      rowJson["LAST UPDATED"] = date;
      rowJson["Sheet Name"] = sheetName;
      rowJson["Check LAST UPDATED"] = false;
      outputJsonArray.push(rowJson);
    }
    // console.log(sheetName);
    // console.log(outputJsonArray);
    // console.log("==========================================");
    callAPI(outputJsonArray);
    // converter.json2csv(outputJsonArray, (err, csv) => {
    //   if (err) {
    //     throw err;
    //   }

    // print CSV string
    // console.log(csv);
    // });
  }).catch(error => {
    console.error(error)
  })
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