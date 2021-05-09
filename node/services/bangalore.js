const fetch = require("node-fetch");
var getJSON = require('get-json')
const moment = require("moment");
const qs = require('qs')

function getHTML () {
    getJSON('http://www.whateverorigin.org/get?url=' + encodeURIComponent('http://bbmpgov.com/chbms/') + '&callback=?', 
    function (data) {
      var parser = new DOMParser();
      htmlSource = parser.parseFromString(data.contents, 'text/html');
      let outputJsonArray = [];
      const $ = cheerio.load(res.data);
    });
}

async function fetchData(url = "https://covidpune.com/data/covidpune.com/bed_data.json") {
    let response = await fetch(url)
}