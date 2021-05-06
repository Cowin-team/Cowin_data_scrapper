// this script parses the data from https://tncovidbeds.tnega.org/api/hospitals
// install nodejs then npm install axios
const axios = require('axios')

// BE CAREFUL WHILE EDITING sheetDistrictMap
// keys correspond to the sheet names in google spread sheet, and values to the district ids used on tnega website
const sheetDistrictMap = {
  "Ariyalur Beds": "5ea0abd3d43ec2250a483a4f", "chengalpattu Beds": "5ea0abd4d43ec2250a483a61",
  "Chennai Beds": "5ea0abd2d43ec2250a483a40", "Coimbatore beds": "5ea0abd3d43ec2250a483a4a",
  "cuddalore Beds": "5ea0abd3d43ec2250a483a50", "dharmapuri Beds": "5ea0abd2d43ec2250a483a43",
  "dindigul Beds": "5ea0abd3d43ec2250a483a4b", "erode Beds": "5ea0abd2d43ec2250a483a48",
  "kallakurichi beds": "5ea0abd4d43ec2250a483a5f", "kancheepuram Beds": "5ea0abd2d43ec2250a483a41",
  "Nagercoil Beds": "5ea0abd3d43ec2250a483a5c", "Karur Beds": "5ea0abd3d43ec2250a483a4c",
  "krishnagiri Beds": "5ea0abd3d43ec2250a483a5d", "Madurai Beds": "5ea0abd3d43ec2250a483a56",
  "Mayiladuthurai beds": "60901c5f2481a4362891d572", "nagapattinam Beds": "5ea0abd3d43ec2250a483a51",
  "namakkal Beds": "5ea0abd2d43ec2250a483a47", "nilgiris beds": "5ea0abd3d43ec2250a483a49",
  "Perambalur Beds": "5ea0abd3d43ec2250a483a4e", "pudukkottai Beds": "5ea0abd3d43ec2250a483a54",
  "ramanathapuram beds": "5ea0abd3d43ec2250a483a59", "ranipet beds": "5ea0abd4d43ec2250a483a63",
  "Salem Beds": "5ea0abd2d43ec2250a483a46", "sivagangai beds": "5ea0abd3d43ec2250a483a55",
  "tenkasi Beds": "5ea0abd4d43ec2250a483a60", "Thanjavur Beds": "5ea0abd3d43ec2250a483a53",
  "Theni Beds": "5ea0abd3d43ec2250a483a57", "Thiruchirappalli Beds": "5ea0abd3d43ec2250a483a57",
  "Thirupathur Beds": "5ea0abd4d43ec2250a483a62", "Thiruvarur Beds": "5ea0abd3d43ec2250a483a52",
  "Thoothukudi Beds": "5ea0abd3d43ec2250a483a5a", "Tirunelveli Beds": "5ea0abd3d43ec2250a483a5b",
  "Tiruppur Beds": "5ea0abd4d43ec2250a483a5e", "Tiruvallur Beds": "5ea0abd1d43ec2250a483a3f",
  "Tiruvannamalai Beds": "5ea0abd2d43ec2250a483a44", "Vellore Beds": "5ea0abd2d43ec2250a483a42",
  "Villupuram Beds": "5ea0abd2d43ec2250a483a45", "Virudhunagar Beds": "5ea0abd3d43ec2250a483a58"
}

for (let sheetName in sheetDistrictMap) {
  // console.log(sheetName+"=="+sheetDistrictMap[sheetName]);
  axios.post('https://tncovidbeds.tnega.org/api/hospitals', {
    District: sheetDistrictMap[sheetName],
    FacilityTypes: ["CHO", "CHC", "CCC"],
    IsGovernmentHospital: true,
    IsPrivateHospital: true,
    pageLimit: 100
  })
    .then(res => {
      var outputJsonArray = [];
      console.log("res.data.length == " + res.data.length);
      for (i = 0; i < res.data.result.length; i++) {
        var rowJson = {};
        var rowdata = res.data.result[i];
        rowJson["Name"] = rowdata["Name"];
        rowJson["COVID Beds"] = rowdata["CovidBedDetails"]["VaccantNonO2Beds"];
        rowJson["Oxygen Beds"] = rowdata["CovidBedDetails"]["VaccantO2Beds"];
        rowJson["ICU"] = rowdata["CovidBedDetails"]["VaccantICUBeds"];
        rowJson["Contact"] = rowdata["MobileNumber"];
        var date = rowdata["CovidBedDetails"]["LastUpdatedTime"];
        if (date > 0)
          rowJson["LAST UPDATED"] = new Date(date * 1000).toLocaleString(undefined, {timeZone: 'Asia/Kolkata'});
        else
          rowJson["LAST UPDATED"] = "Not available"
        rowJson["Sheet Name"] = sheetName;
        outputJsonArray.push(rowJson);
      }
      console.log("Parsed sheet: " + sheetName);
      console.log(outputJsonArray);
      console.log("===============================================================================================");
    })
    .catch(error => {
      console.error(error)
    })
}