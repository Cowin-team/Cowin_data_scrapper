// this script parses the data from https://tncovidbeds.tnega.org/ for Tamil Nadu
// npm install --save cheerio puppeteer
const puppeteer = require('puppeteer');

async function getVisibleHandle(selector, page) {
  const elements = await page.$$(selector);
  let hasVisibleElement = false,
    visibleElement = '';

  if (!elements.length) {
    return [hasVisibleElement, visibleElement];
  }

  let i = 0;
  for (let element of elements) {
    const isVisibleHandle = await page.evaluateHandle((e) => {
      const style = window.getComputedStyle(e);
      return (style && style.display !== 'none' &&
        style.visibility !== 'hidden' && style.opacity !== '0');
    }, element);
    var visible = await isVisibleHandle.jsonValue();
    const box = await element.boxModel();
    if (visible && box) {
      hasVisibleElement = true;
      visibleElement = elements[i];
      break;
    }
    i++;
  }

  if (visibleElement) {
    await Promise.all([
      visibleElement.click(),
    ]);
  }
  return [hasVisibleElement, visibleElement];
}

(async function scrape() {
  const browser = await puppeteer.launch({headless: false});
  const page = await browser.newPage();
  page.setDefaultNavigationTimeout(90000);

  await page.goto('https://tncovidbeds.tnega.org/');
  // await page.$('button.dropdown-toggle.btn.btn-outline-dark.btn-xs');

  // let visibleHandle = await getVisibleHandle('div.react-select__control.css-yk16xz-control', page);
  await getVisibleHandle('button.dropdown-toggle.btn.btn-outline-dark.btn-xs', page);
  await getVisibleHandle('div.dropdown-menu.dropdown-menu-right button:nth-child(5)', page);
  await getVisibleHandle('div.react-select__control.css-yk16xz-control', page); //Ariyalur
  await page.click('div#react-select-3-option-0');
  await page.waitForNavigation()
  await getVisibleHandle('div.modal button.mb-5.btn.btn-primary', page); //Ariyalur
  // await page.click('.modal button.mb-5.btn.btn-primary');

  // extracting information from code
  let quotes = await page.evaluate(() => {

    // let quotesElement = document.body.querySelectorAll('.quote');
    // let quotes = Object.values(quotesElement).map(x => {
    //   return {
    //     author: x.querySelector('.author').textContent ?? null,
    //     quote: x.querySelector('.content').textContent ?? null,
    //     tag: x.querySelector('.tag').textContent ?? null,
    //   }
    // });

    return document.body;

  });

  // logging results
  console.log(quotes);
  // await browser.close();

})();