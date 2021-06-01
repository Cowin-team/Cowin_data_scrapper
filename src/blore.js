const axios = require('axios');
const cheerio = require('cheerio');
const puppeteer = require('puppeteer');
const fetch = require("node-fetch");

const siteURL = "http://apps.bbmpgov.in/covid19";
const sheetsURL = "http://127.0.0.1:5000/updateBulk";
let result = [];

// get the PowerBI Table link from the Covid Site
axios({
  method: 'get',
  url: siteURL,
}).then(res => {
  let $ = cheerio.load(res.data);
  let apiUrl = $("iframe").attr("src");
  translatePowerBiTable(apiUrl)
      .then(result => {
        update(result)
            .then(response => {
              console.log("Sheets API Update Response Status ", +response.status)
            })});
}).catch(error => {
  console.error(error)
})

async function translatePowerBiTable(apiUrl) {
  const browser = await puppeteer.launch({headless: false});
  const page = await browser.newPage();
  await page.setViewport({ width : 1200, height : 800 })
  await page.goto(apiUrl, { waitUntil : 'networkidle0' });


  /*
    * BodyCells contain the data we need to scrape. It's the 3rd child of the innerContainer.
    *   document.querySelectorAll(".innerContainer")[1].children[3].children[0]
    * BodyCells are divided into two sides - left & right (unfortunately)
    * Left side of BodyCells : from column Hospital Name to column Blocked General
    *   document.querySelectorAll(".innerContainer")[1].children[3].children[0].children[0]
    * Right side of BodyCells : from column Blocked HDU to column Net Avail. ICU Vent
    *   document.querySelectorAll(".innerContainer")[1].children[3].children[0].children[1]
    * Get a particular Column on either side
    *   document.querySelectorAll(".innerContainer")[1].children[3].children[0].children[x].children[1]
    * Get a row from a given column (cell) on either side
    *   document.querySelectorAll(".innerContainer")[1].children[3].children[0].children[x].children[1].children[0]
  */
  for (let i = 0; i < 10; i++) {
    let subResult = await page.evaluate(async() =>
    {
      //todo : something's up with scroll leading to a lot of hospital data not being recorded. Need's a fix
      document.querySelectorAll(".innerContainer")[1]
          .querySelector(".bodyCells div div:last-of-type div:last-of-type div:last-of-type")
          .scrollIntoView();

      // hospital count in current scroll view
      let hospitalCount = document.querySelectorAll(".innerContainer")[1].children[3].children[0].children[0].children[0].children.length;
      let localResult = [];
      for (let j = 0; j < hospitalCount; j++) {
        // populate hospital name ; 0th column on the left side
        let hospitalName = document.querySelectorAll(".innerContainer")[1].children[3].children[0].children[0].children[0].children[j].innerText;
        // populate general available ; 4th column on the right side
        let genAvail = document.querySelectorAll(".innerContainer")[1].children[3].children[0].children[1].children[3].children[j].innerText;
        // populate HDU available ; 5th column on the right side
        let hduAvail = document.querySelectorAll(".innerContainer")[1].children[3].children[0].children[1].children[4].children[j].innerText;
        // populate ICU available ; 6th column on the right side
        let icuAvail = document.querySelectorAll(".innerContainer")[1].children[3].children[0].children[1].children[5].children[j].innerText;
        // populate ICU Vent available ; 7th column on the right side
        let icuVentAvail = document.querySelectorAll(".innerContainer")[1].children[3].children[0].children[1].children[6].children[j].innerText;
        // populate late updated
        let lastUpdated = document.querySelectorAll("svg[class=card]")[0].getAttribute('aria-label')
              .substring(15,document.querySelectorAll("svg[class=card]")[0].getAttribute('aria-label').length - 1);

        localResult.push({
          "Sheet Name": 'Bangalore Beds',
          "Name":hospitalName,
          "COVID Beds":genAvail,
          "HDU Beds":hduAvail,
          "ICU":icuAvail,
          "Ventilator Beds":icuVentAvail,
          "LAST UPDATED" : lastUpdated,
          "Check LAST UPDATED": false
        });
      }
      return localResult;
    });
    result.push.apply(result, subResult);
  }
  return result;
}

// Update Hospital Data to Google Sheets
async function update(hospitalData) {
  // remove duplicates that are introduced by the scrolling issues
  let uniqueHospitalNamesList = []
  let uniqueHospitals = [];
  for (let i = 0; i< hospitalData.length; i++){
    if (!uniqueHospitalNamesList.includes(hospitalData[i].Name)){
      uniqueHospitalNamesList.push(hospitalData[i].Name);
      uniqueHospitals.push(hospitalData[i]);
    }
  }
  // Uncomment to validate the hospital data sent to sheets api
  console.log(uniqueHospitals);
  console.log("Number of unique hospitals", +uniqueHospitals.length);

  // make a call to sheets api
  // todo : we can move this code to a common module to avoid boiler plate code in multiple files
  return await fetch(sheetsURL, {
    method: 'POST', // or 'PUT'
    credentials: 'omit',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(uniqueHospitals),
  })
}
