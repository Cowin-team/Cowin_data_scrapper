# How does it work?

The web scraping is basically a 3-step process.
1. Scrape the site
2. Parse the data and convert it into desired format
3. Save the data to google sheets or the data repository

Scraping the site itself can be easy to difficult depending on how it is implemented.
1. First look for the data source in the network tab (using developer console in the browser). If you are able to find the API calls then you already have the data available at your dispoal. For example, https://covidpune.com/ makes API calls to https://covidpune.com/data/covidpune.com/bed_data.json, now you just need to go to step 2 and parse this data. See [covidpune.js](https://github.com/Cowin-team/Cowin_data_scrapper/blob/main/src/covidpune.js) file for further details. This is the simplest example of scraping.
2. However, sometimes the API calls will not go through due to CORS error which is our nemesis in the web scraping process. In this case, you can use the `whateverorigin` (http://www.whateverorigin.org/) to send the API calls. However, the response needs to be in JSOn format for this to work. See [bbmpgov.js](https://github.com/Cowin-team/Cowin_data_scrapper/blob/main/src/bbmpgov.js) for example.
3. If you get the CORS error and either response is not in a JSON format or request is not a GET but POST request, then you can not use the plain vanilla javascript to fetch the API response. You will need to resort to axios which is a node module. Install node, followed by `npm install axios`. See [tnega.js](https://github.com/Cowin-team/Cowin_data_scrapper/blob/main/src/tnega.js) for an example in which request was POST. If the response is in HTML format, you will need the cheerio (`npm install cheerio`) module as well. See [rcmedicrew.js](https://github.com/Cowin-team/Cowin_data_scrapper/blob/main/src/rcmedicrew.js) and [andhra.js](https://github.com/Cowin-team/Cowin_data_scrapper/blob/main/src/andhra.js) for examples.
4. With CORS error and response being in javascript format, using node request module is easiest (`npm install request`). See [jantasamvad.js](https://github.com/Cowin-team/Cowin_data_scrapper/blob/main/src/jantasamvad.js) for an example.
5. If you are unable to isolate the API calls, but the website is static, then simply fetch the page html and parse the data from the DOM.
6. If you are unable to isolate the API calls, but the website is dynamic, then it is going to be the hardest of all. You will need to use the puppeteer module (`npm install puppeteer`). It works like selenium and uses its own headless browser to make requests. See [puppeteerSample.js](https://github.com/Cowin-team/Cowin_data_scrapper/blob/main/src/puppeteerSample.js) for an example.

# Running the scrapers
1. To run the plain javascript based scrapers such as covidpune.js and bbmpgov.js, simply put the script in the dummy.html file and run the html file in the browser.
2. Tun run the node based scrapers, simply type `node filename` in console. For example, to run andhra.js file, type `node src/andhra.js` when located in the project root directory and then hit enter.
