// this script parses the data from http://covid.rcmedicrew.org/ using their /scripts/getSearch.php API
// install nodejs then npm install axios
const axios = require('axios');
const cheerio = require('cheerio');
const qs = require('qs')
const apiURL = "http://covid.rcmedicrew.org/scripts/getSearch.php";
const idPlaceMap = {
  "1": ["Tilak Nagar"],
  "2": [" "],
  "3": [" "],
  "4": ["Connaught palace", "North east delhi"],
  "6": ["Connaught Place, Lajpat Nagar, Karol Bagh", "Greater Kailash", "Greater Kailash- 1", "Kalkaji",
    "Khirki Extension", "Nehru Enclave ,Kalkaji Temple", "Qutub Minar", "Safdarjung Enclave", "Saket District Centre",
    "Shanti Niketan Moti Bagh", "Sheikh Sarai"]
}
for (let resourceId in idPlaceMap) {
  let placeList = idPlaceMap[resourceId];
  for (let i in placeList) {
    let place = placeList[i];
    // ideally the axios call need to be placed here, but keeping it out of the loop to just update the covid beds
  }
}

axios({
  method: 'post',
  url: apiURL,
  data: qs.stringify({
    type: "getSearchResult",
    resourceid: 3,
    stateid: "Delhi",
    cityid: "New Delhi (DL)",
    location: ""
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
    // console.log("row " + i + " == " + columns);
    var rowJson = {};
    rowJson["Name"] = $(columns[1]).text().trim().split("Location:")[0].trim();
    let bedData = $(columns[5]).text().trim().replace("Beds Without Oxygen :", "").split(":");
    rowJson["COVID Beds"] = bedData[0].split("Beds With Oxygen")[0].trim();
    rowJson["Oxygen Beds"] = bedData[1].split("ICU")[0].trim();
    rowJson["ICU"] = bedData[2].split("Ventilator")[0].trim();
    rowJson["Ventilator Beds"] = bedData[3].trim();
    rowJson["Contact"] = $(columns[1]).text().trim().split(":")[2].split("Direction")[0].trim();
    rowJson["LAST UPDATED"] = $(columns[7]).text();
    rowJson["Sheet Name"] = "Delhi Beds";
    outputJsonArray.push(rowJson);
    // for (let j = 0; j < columns.length; j++) {
    //   console.log("column " + j + " == " + $(columns[j]).text());
    //   console.log("++++++++++++++++");
    // }
    // console.log("============================================================")
  }
  console.log(outputJsonArray);
}).catch(error => {
  console.error(error)
})
