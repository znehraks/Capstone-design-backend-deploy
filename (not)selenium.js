const webdriver = require("selenium-webdriver");
const chrome = require("selenium-webdriver/chrome");

const run = async (
  center_lat,
  center_lon,
  btm_lat,
  left_lon,
  top_lat,
  right_lon
) => {
  const url = `https://m.land.naver.com/cluster/clusterList?view=atcl&rletTpCd=OR&tradTpCd=A1%3AB1%3AB2%3AB3&z=15&lat=${center_lat}&lon=${center_lon}&btm=${btm_lat}&lft=${left_lon}&top=${top_lat}&rgt=${right_lon}&pCortarNo=`;
  const service = new chrome.ServiceBuilder("./chromedriver.exe").build();
  chrome.setDefaultService(service);

  const driver = await new webdriver.Builder().forBrowser("chrome").build();

  await driver.get(url);
  let json = await (
    await driver.findElement(webdriver.By.tagName("body"))
  ).getText();
  json.then((text) => {
    console.log(text);
  });

  //   setTimeout(async () => {
  //     await driver.quit();
  //     process.exit(0);
  //   }, 3000);
};
try {
  run(
    37.5785302,
    126.9234694,
    37.5625943,
    126.8822707,
    37.5944627,
    126.9646681
  );
} catch (e) {
  console.log(e);
}
