// this script parses the data from http://covid.rcmedicrew.org/ using their /scripts/getSearch.php API
const axios = require('axios');
const cheerio = require('cheerio');
const fetch = require("node-fetch");
var moment = require('moment');
const qs = require('qs')


async function fetchData(url = "http://covid.rcmedicrew.org/scripts/getSearch.php"){
  
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

  let response = await axios({
                  method: 'post',
                  url: url,
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
  })
  .then(res => {
    let outputJsonArray = [];
    const $ = cheerio.load(res.data);
    let dataRows = $("tbody tr");
    for (let i = 0; i < dataRows.length; i++) {
      let row = dataRows[i];
      let columns = $(row).find("td");
      var rowJson = {};
      rowJson["Name"] = $(columns[1]).text().trim().split("Location:")[0].trim();
      let bedData = $(columns[5]).text().trim().replace("Beds Without Oxygen :", "").split(":");
      rowJson["COVID Beds"] = bedData[0].split("Beds With Oxygen")[0].trim();
      rowJson["Oxygen Beds"] = bedData[1].split("ICU")[0].trim();
      rowJson["ICU"] = bedData[2].split("Ventilator")[0].trim();
      rowJson["Ventilator Beds"] = bedData[3].trim();
      rowJson["Contact"] = $(columns[1]).text().trim().split(":")[2].split("Direction")[0].trim();
      let date = new Date($(columns[7]).text());
      date = moment(date).format('YYYY-MM-DD HH:mm:ss');
      rowJson["LAST UPDATED"] = date;
      rowJson["Sheet Name"] = "Mumbai Beds";
      rowJson["Check LAST UPDATED"] = false;
      outputJsonArray.push(rowJson);
    }
    return outputJsonArray
  }).catch(error => {
    console.error(error)
  })
  return response
}

// async function callAPI(bedData) {
//   response = await fetch(sheetsURL, {
//     method: 'POST', // or 'PUT'
//     credentials: 'omit',
//     headers: {
//       'Content-Type': 'application/json',
//     },
//     body: JSON.stringify(bedData),
//   })
//   const message = await response.json();
//   if (!response.ok) {
//     console.log(`HTTP error! status: ${response.status} message: ${response.json()}`);
//   } else {
//     console.log(message)
//   }
// }



exports.fetchData = fetchData;