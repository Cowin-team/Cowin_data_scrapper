// this script parses the data from https://excise.wb.gov.in/CHMS/Public/Page/CHMS_Public_Hospital_Bed_Availability.aspx
const puppeteer = require('puppeteer');
const districtList = ["020", "001", "003", "008", "016", "017", "004", "006", "005", "007", "022", "021", "019", "009",
  "012", "013", "023", "010", "002", "011", "014", "015", "018"];
outputJsonArray = [];
const url = "https://excise.wb.gov.in/CHMS/Public/Page/CHMS_Public_Hospital_Bed_Availability.aspx";

async function scrape(did, hospType) {
  // const browser = await puppeteer.launch({headless: false, args: ['--auto-open-devtools-for-tabs']});
  const browser = await puppeteer.launch({headless: false});
  const page = await browser.newPage();
  page.setDefaultNavigationTimeout(0);
  await page.goto(url, {waitUntil: 'networkidle0', timeout: 0});
  await page.waitForSelector('#ctl00_ContentPlaceHolder1_ddl_District');

  await page.click(hospType);
  await page.select('#ctl00_ContentPlaceHolder1_ddl_District', did);
  await page.waitForSelector('tbody tr');

  // extracting information from code
  let outputData = await page.evaluate(() => {
    let output = [];
    let dataRows = document.body.querySelectorAll("tbody tr");
    let cityName = document.querySelector("#ctl00_ContentPlaceHolder1_ddl_District").selectedOptions[0].textContent.trim();
    console.log(cityName)
    // return dataRows.length;
    console.log("Num entries == " + dataRows.length);
    dataRows.forEach((dataRow) => {
      let rowJson = {};
      // debugger;
      rowJson["Name"] = dataRow.querySelector('h5').textContent.trim().replace(/\s+/g, ' ');
      // let h3 = dataRow.querySelectorAll('li h3.text-success')[3].textContent;
      rowJson["COVID Beds"] = dataRow.querySelectorAll('li h3.text-success')[7].textContent;
      rowJson["Oxygen Beds"] = dataRow.querySelectorAll('li h3.text-success')[11].textContent;
      rowJson["ICU"] = dataRow.querySelectorAll('li h3.text-success')[19].textContent;
      rowJson["Ventilator Beds"] = dataRow.querySelectorAll('li h3.text-success')[23].textContent;
      rowJson["HDU Beds"] = dataRow.querySelectorAll('li h3.text-success')[15].textContent;
      rowJson["Address"] = dataRow.querySelector('.row>div').textContent.trim().replace(/\s+/g, ' ');
      rowJson["Contact"] = dataRow.querySelector('.rounded-pill.bg-success').textContent.trim().replace(/\s+/g, ' ');
      rowJson["Sheet Name"] = cityName + " Beds";
      rowJson["Source URL"] = "https://excise.wb.gov.in/CHMS/Public/Page/CHMS_Public_Hospital_Bed_Availability.aspx";
      output.push(rowJson);
    })
    return output;
  });
  outputJsonArray = outputJsonArray.concat(outputData);
  console.log("data == ");
  console.log(outputData);

  await browser.close();
};


districtList.forEach(getData);

async function getData(districtId) {
  await scrape(districtId, "[for=ctl00_ContentPlaceHolder1_rdo_Govt_Flag_0]")
  await scrape(districtId, "[for=ctl00_ContentPlaceHolder1_rdo_Govt_Flag_1]")
  await scrape(districtId, "[for=ctl00_ContentPlaceHolder1_rdo_Govt_Flag_2]")
  console.log("+++++++++++++++++Full JSON below+++++++++++++++++");
  console.log(outputJsonArray);
}