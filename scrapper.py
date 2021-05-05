import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
import sys
# pc버전 api
# url = f"https://new.land.naver.com/api/articles/clusters?cortarNo=1141011700&zoom=15&markerId&markerType&selectedComplexNo&selectedComplexBuildingNo&fakeComplexMarker&realEstateType=APT%3AOPST%3AABYG%3AOBYG%3AGM%3AOR%3AVL%3ADDDGG%3AJWJT%3ASGJT%3AHOJT&tradeType=&tag=%3A%3A%3A%3A%3A%3A%3ASMALLSPCRENT%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=false&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&leftLon=126.8992045&rightLon=126.9317987&topLat=37.5879848&bottomLat=37.576930950000005"

# 명지대학교 인문캠퍼스 위치가 중심인 지도.
# center_lat = 37.5785302
# center_lon = 126.9234694
# btm_lat = 37.5625943
# left_lon = 126.8822707
# top_lat = 37.5944627
# right_lon = 126.9646681


def scrapper(center_lat,
             center_lon,
             btm_lat,
             left_lon,
             top_lat,
             right_lon):
    url = f"https://m.land.naver.com/cluster/clusterList?view=atcl&rletTpCd=OR&tradTpCd=A1%3AB1%3AB2%3AB3&z=15&lat={center_lat}&lon={center_lon}&btm={btm_lat}&lft={left_lon}&top={top_lat}&rgt={right_lon}&pCortarNo="
    # sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    # sys.stdout.reconfigure(encoding='utf-8')
    # chrome_options = Options()
    # chrome_options.add_experimental_option(
    #     "excludeSwitches", ["enable-logging"])
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('/workspace/resi-reco-backend/chromedriver',chrome_options=chrome_options)


    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    site_json = json.loads(soup.find("body").text)
    driver.close()

    return site_json

    # bs4 만 쓸 경우 - Selenium 미 사용 시(단, Response 307 뜸)
    # html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    # soup = BeautifulSoup(html, "html.parser")
    # site_json = json.loads(soup.text)
    # result = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    # soup = BeautifulSoup(result.text, "html.parser")
    # for i in site_json:
    #     print(i)
