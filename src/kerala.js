// this script parses the data from https://covid19jagratha.kerala.nic.in/home/addHospitalDashBoard

const puppeteer = require('puppeteer');
const fetch = require("node-fetch");
const siteURL = "https://covid19jagratha.kerala.nic.in/home/addHospitalDashBoard";
const sheetsURL = "http://127.0.0.1:5000/updateBulk";
var outputJsonArray = [];

async function getVisibleHandle(selector, page) {
  const elements = await page.$$(selector);
  let hasVisibleElement = false,
    visibleElement = '';

  if (!elements.length) {
    return [hasVisibleElement, visibleElement];
  }

  let i = 0;
  for (let element of elements) {
    const isVisibleHandle = await page.evaluateHandle((e) => {
      const style = window.getComputedStyle(e);
      return (style && style.display !== 'none' &&
        style.visibility !== 'hidden' && style.opacity !== '0');
    }, element);
    var visible = await isVisibleHandle.jsonValue();
    const box = await element.boxModel();
    if (visible && box) {
      hasVisibleElement = true;
      visibleElement = elements[i];
      break;
    }
    i++;
  }

  if (visibleElement) {
    await Promise.all([
      visibleElement.click(),
    ]);
  }
  return [hasVisibleElement, visibleElement];
}

async function scrapeKerala() {
  // const browser = await puppeteer.launch({headless: false, args: ['--auto-open-devtools-for-tabs']});
  const browser = await puppeteer.launch({headless: false});
  const page = await browser.newPage();
  page.setDefaultNavigationTimeout(0);
  await page.goto(siteURL, {waitUntil: 'networkidle0', timeout: 0});
  await page.waitForSelector('#distId');
  let districts = await page.evaluate(() => {
    let options = document.querySelectorAll("#distId option");
    let list = Array.from(options).map(elem => elem.text);
    list.shift()
    return list;
  })

  scrapeInSequence();

  async function scrapeInSequence() {
    let distId = 1;
    for (var dist of districts) {
      await getVisibleHandle('#distId_chosen', page);
      await page.waitFor(300);
      await page.keyboard.press('ArrowDown');
      await page.keyboard.press('Enter');

      await getVisibleHandle('button[type="submit"]', page);
      await page.waitFor(5000);

      await getVisibleHandle('.hos a', page);
      await page.waitForSelector('#hosTable_length select');
      await page.select('#hosTable_length select', '-1');

      let output = await page.evaluate((dist, siteURL) => {
        let dataRows = document.querySelectorAll('#hosTable tbody tr');
        // console.log(dist);
        let outputArray = [];
        for (let i = 0; i < dataRows.length; i++) {
          let row = dataRows[i];
          let columns = $(row).find("td");
          // console.log("row " + i + " == " + columns);
          var rowJson = {};
          rowJson["Name"] = $(columns[0]).text().trim();
          rowJson["COVID Beds"] = $(columns[5]).text().trim();
          // rowJson["Oxygen Beds"] = bedData[1].split("ICU")[0].trim();
          rowJson["ICU"] = $(columns[7]).text().trim();
          rowJson["Oxygen Beds"] = "";
          rowJson["Ventilator Beds"] = $(columns[8]).text().trim()
          // rowJson["Contact"] = $(columns[1]).text().trim().split(":")[2].split("Direction")[0].trim();
          let date = moment($(columns[6]).text().trim(), "DD-MM-YYYY hh:mm:ssa").format('YYYY-MM-DD HH:mm:ss')
          rowJson["LAST UPDATED"] = date;
          rowJson["Sheet Name"] = dist.toLowerCase() + " beds";
          rowJson["Check LAST UPDATED"] = false;
          rowJson["Address"] = rowJson["Name"] + ", " + dist + ", Kerala";
          rowJson["Source URL"] = siteURL;
          outputArray.push(rowJson);
        }
        // console.log(outputArray)
        return outputArray;
      }, dist, siteURL)

      await getVisibleHandle('#hospitalModal i.fa.fa-close', page);
      await page.waitFor(500);

      // get oxygen data which is in a separate place
      await page.waitForSelector('div.oxybed a');
      await getVisibleHandle('div.oxybed a', page);
      await page.waitFor(500);

      await page.waitForSelector('#hospitalModal select');
      await page.select('#hospitalModal select', '-1');
      let oxygen = await page.evaluate((dist, siteURL) => {
        let dataRows = document.querySelectorAll('#hospitalModal tbody tr');
        let oxygenArray = [];
        for (let i = 0; i < dataRows.length; i++) {
          let row = dataRows[i];
          let columns = $(row).find("td");
          var rowJson = {};
          rowJson["Name"] = $(columns[0]).text().trim();
          rowJson["Oxygen Beds"] = $(columns[2]).text().trim();
          rowJson["Sheet Name"] = dist.toLowerCase() + " beds";
          rowJson["Source URL"] = siteURL;
          rowJson["Check LAST UPDATED"] = false;
          rowJson["Address"] = rowJson["Name"] + ", " + dist + ", Kerala";
          oxygenArray.push(rowJson);
        }
        console.log(oxygenArray);
        // debugger;
        return oxygenArray;
      }, dist, siteURL)
      // merge the oxygen data into the overall data
      await getVisibleHandle('#hospitalModal i.fa.fa-close', page);
      await page.waitFor(300);

      for (let i = 0; i < oxygen.length; i++) {
        let row = oxygen[i];
        let name = row["Name"];
        let hospExists = false;
        for (let j = 0; j < output.length; j++) {
          if (output[j]["Name"].toLowerCase() === name.toLowerCase()) {
            output[j]["Oxygen Beds"] = row["Oxygen Beds"];
            hospExists = true;
            break;
          }
        }
        if (!hospExists) {
          output.push(oxygen[i]);
        }
      }
      outputJsonArray.push.apply(outputJsonArray, output);
      distId++;
    }
    await browser.close();
    console.log(outputJsonArray);

    callAPI(outputJsonArray);
  }
};

scrapeKerala();

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
