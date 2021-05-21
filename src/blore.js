// this script parses the data from http://covid.rcmedicrew.org/ using their /scripts/getSearch.php API
// install nodejs then npm install axios
const axios = require('axios');
const cheerio = require('cheerio');
const fetch = require("node-fetch");
const moment = require('moment');
const puppeteer = require('puppeteer');
const qs = require('qs')
// const converter = require('json-2-csv');

const siteURL = "http://apps.bbmpgov.in/covid19/index.html";
const sheetsURL = "http://127.0.0.1:5000/updateBulk";

axios({
  method: 'get',
  url: siteURL,
}).then(res => {
  // console.log(res.data);
  let outputJsonArray = [];
  let $ = cheerio.load(res.data);
  let apiUrl = $("iframe").attr("src");
  console.log(apiUrl);
  callPowerBiApi(apiUrl)
}).catch(error => {
  console.error(error)
})

async function callPowerBiApi(apiUrl) {
  // const browser = await puppeteer.launch({headless: false, args: ['--auto-open-devtools-for-tabs']});
  const browser = await puppeteer.launch({headless: false});
  const page = await browser.newPage();
  page.setDefaultNavigationTimeout(0);
  await page.goto(apiUrl, {waitUntil: 'networkidle0', timeout: 0});
  await page.waitForSelector('.innerContainer');

  await page.evaluate(() => document.querySelectorAll(".innerContainer")[1].querySelector(".bodyCells>div div:last-of-type div:last-of-type div:last-of-type").scrollIntoView());
  await page.evaluate(() => document.querySelectorAll(".innerContainer")[1].querySelector(".bodyCells>div div:last-of-type div:last-of-type div:last-of-type").scrollIntoView());
  await page.evaluate(() => document.querySelectorAll(".innerContainer")[1].querySelector(".bodyCells>div div:last-of-type div:last-of-type div:last-of-type").scrollIntoView());
  await page.evaluate(() => document.querySelectorAll(".innerContainer")[1].querySelector(".bodyCells>div div:last-of-type div:last-of-type div:last-of-type").scrollIntoView());
  // await page.waitFor(2000);
  await page.evaluate(() => document.querySelectorAll(".innerContainer")[1].querySelector(".bodyCells>div div:last-of-type div:last-of-type div:last-of-type").scrollIntoView());
  await page.evaluate(() => document.querySelectorAll(".innerContainer")[1].querySelector(".bodyCells>div div:last-of-type div:last-of-type div:last-of-type").scrollIntoView());
  await page.evaluate(() => document.querySelectorAll(".innerContainer")[1].querySelector(".bodyCells>div div:last-of-type div:last-of-type div:last-of-type").scrollIntoView());
  await page.evaluate(() => document.querySelectorAll(".innerContainer")[1].querySelector(".bodyCells>div div:last-of-type div:last-of-type div:last-of-type").scrollIntoView());
  await page.evaluate(() => document.querySelectorAll(".innerContainer")[1].querySelector(".bodyCells>div div:last-of-type div:last-of-type div:last-of-type").scrollIntoView());
  await page.evaluate(() => document.querySelectorAll(".innerContainer")[1].querySelector(".bodyCells>div div:last-of-type div:last-of-type div:last-of-type").scrollIntoView());
  let outputData = await page.evaluate(() => {
    let leftData = document.querySelectorAll(".innerContainer")[1].querySelectorAll(".bodyCells>div div:first-of-type div");
    // debugger;
    leftData.push(document.querySelectorAll(".innerContainer")[1].querySelectorAll(".bodyCells>div div:nth-of-type(3) div"));
    let rightData = document.querySelectorAll(".innerContainer")[1].querySelectorAll(".bodyCells>div div:nth-of-type(2) div");
    rightData.push(document.querySelectorAll(".innerContainer")[1].querySelectorAll(".bodyCells>div div:nth-of-type(4) div"));
    // console.log($(".innerContainer")[1]);
    let cells = $(html).find(".bodyCells div:first-child");
    console.log(cells);
  })
}