const fetch = require("node-fetch");
const moment = require("moment");
const url = "http://127.0.0.1:5000/updateBulk"

async function send(bedData) {

    // // If beddata is a list select update bulk
    // if (Array.isArray(bedData)){
    //   url = url + "/updateBulk"
      
    //   // for (var key in bedData) {
    //   //   var rowJson = {};
    //   //   var rowdata = bedData[key];
    //   //   // Check data time format
    //   // }
    // }
    console.log(url)
    response = await fetch(url, {
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


exports.send = send;