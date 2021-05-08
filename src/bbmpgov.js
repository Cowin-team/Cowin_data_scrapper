// this script parses the data from bbmpgov.com for bangalore

var outputJsonArray = [];
var htmlSource;

window.onload = function () {
  $.getJSON('http://www.whateverorigin.org/get?url=' + encodeURIComponent('http://bbmpgov.com/chbms/') + '&callback=?', function (data) {
    var parser = new DOMParser();
    htmlSource = parser.parseFromString(data.contents, 'text/html');
    parseHTML();
  });
};

var url = "http://127.0.0.1:5000/updateBulk";

function parseHTML() {
  // console.log(htmlSource);
  var lastUpdated = htmlSource.querySelector("h5").innerText.substring(7, 19);
  lastUpdated = new Date(lastUpdated);
  lastUpdated = moment(lastUpdated).format('YYYY-MM-DD HH:mm:ss');
  // get the data for Government Hospitals
  var rows = htmlSource.querySelectorAll("#GovernmentHospitalsDetail tbody tr");

  for (var i = 0; i < rows.length - 1; i++) {
    var rowJson = {};
    // console.log(rows[i]);
    var columnData = rows[i].querySelectorAll("td");
    rowJson["Name"] = columnData[1].innerText;
    rowJson["COVID Beds"] = columnData[12].innerText;
    rowJson["HDU Beds"] = columnData[13].innerText;
    rowJson["ICU"] = columnData[14].innerText;
    rowJson["Ventilator Beds"] = columnData[15].innerText;
    rowJson["LAST UPDATED"] = lastUpdated;
    rowJson["Sheet Name"] = "Bangalore Beds";
    rowJson["Check LAST UPDATED"] = true;
    outputJsonArray.push(rowJson);
    // callAPI(rowJson);
  }

  rows = htmlSource.querySelectorAll("#GovernmentMedical tbody");
  // get the data for Government Medical Colleges
  var medCollegeData = rows[1].querySelectorAll("tr");
  for (var i = 0; i < medCollegeData.length - 1; i++) {
    var rowJson = {};
    // console.log(medCollegeData[i]);
    var columnData = medCollegeData[i].querySelectorAll("td");
    rowJson["Name"] = columnData[1].innerText;
    rowJson["COVID Beds"] = columnData[12].innerText;
    rowJson["HDU Beds"] = columnData[13].innerText;
    rowJson["ICU"] = columnData[14].innerText;
    rowJson["Ventilator Beds"] = columnData[15].innerText;
    rowJson["LAST UPDATED"] = lastUpdated;
    rowJson["Sheet Name"] = "Bangalore Beds";
    rowJson["Check LAST UPDATED"] = true;
    // console.log(rowJson);
    outputJsonArray.push(rowJson);
    // callAPI(rowJson);
  }

  // get the data for Private hospitals
  var pvtHospData = rows[2].querySelectorAll("tr");
  for (var i = 0; i < pvtHospData.length - 1; i++) {
    var rowJson = {};
    // console.log(pvtHospData[i]);
    var columnData = pvtHospData[i].querySelectorAll("td");
    rowJson["Name"] = columnData[1].innerText;
    rowJson["COVID Beds"] = columnData[12].innerText;
    rowJson["HDU Beds"] = columnData[13].innerText;
    rowJson["ICU"] = columnData[14].innerText;
    rowJson["Ventilator Beds"] = columnData[15].innerText;
    rowJson["LAST UPDATED"] = lastUpdated;
    rowJson["Sheet Name"] = "Bangalore Beds";
    rowJson["Check LAST UPDATED"] = true;
    // console.log(rowJson);
    outputJsonArray.push(rowJson);
    // callAPI(rowJson);
  }

  // get the data for Private medical colleges
  var pvtMedCollegeData = rows[3].querySelectorAll("tr");
  for (var i = 0; i < pvtMedCollegeData.length - 1; i++) {
    var rowJson = {};
    // console.log(pvtMedCollegeData[i]);
    var columnData = pvtMedCollegeData[i].querySelectorAll("td");
    rowJson["Name"] = columnData[1].innerText;
    rowJson["COVID Beds"] = columnData[3].innerText;
    rowJson["LAST UPDATED"] = lastUpdated;
    rowJson["Sheet Name"] = "Bangalore Beds";
    rowJson["Check LAST UPDATED"] = true;
    // console.log(rowJson);
    outputJsonArray.push(rowJson);
    // callAPI(rowJson);
  }

  callAPI(outputJsonArray);
  // console.log(JSON.stringify(outputJsonArray));
}

async function callAPI(bedData) {
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