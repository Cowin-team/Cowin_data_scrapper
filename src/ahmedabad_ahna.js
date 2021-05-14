// this script parses the data from https://ahna.org.in/covid19.html for bangalore

const axios = require('axios');
const cheerio = require('cheerio');
const request = require('request')
const fetch = require("node-fetch");
const moment = require('moment');
const qs = require('qs')
const fs = require('fs')
const apiURL = "https://ahna.org.in/covid19.html";
const sheetsURL = "http://127.0.0.1:5000/updateBulk";
const PDFParser = require("pdf2json");
const xlsxFile = require('read-excel-file/node');

axios({
  method: 'post',
  url: apiURL,
  data: qs.stringify({
    type: "getSearchResult",
    resourceid: 3,
    stateid: "Maharashtra",
    cityid: "Mumbai (MH)",
    location: ""
  }),
  headers: {
    'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
}).then(res => {
  // console.log(res.data);
  let outputJsonArray = [];
  const $ = cheerio.load(res.data);
  let src = "https://ahna.org.in/" + $("iframe").attr("src");
  let xlFileName = "ahmdbd.xlsx";
  const pdf2excel = require('pdf-to-excel');

  new Promise((resolve, reject) => {
    pdf2excel.genXlsx(src, xlFileName)
  }).then(
    parseExcel(xlFileName)
  )

}).catch(error => {
  console.error(error)
})

function parseExcel(xlPath) {
  xlsxFile(xlPath).then((rows) => {
    console.log(rows);
    // console.table(rows);
  })
}