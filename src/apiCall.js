const fetch = require("node-fetch");

async function callAPI(bedData) {

  // Check if url is is bulk.
  // If bulk iterate through the list
  // check the time format
  // moment("05/22/2012", 'MM/DD/YYYY',true).isValid()
  // See if Check last update key is there
    // If its there see if its a bool
  // if not add false value to it.
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