# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
import sys
import time
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
    
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
              'Referer': 'https://m.land.naver.com/'}


    # sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    # sys.stdout.reconfigure(encoding='utf-8')
    # chrome_options = Options()
    # chrome_options.add_experimental_option(
    #     "excludeSwitches", ["enable-logging"])
    # display = Display(visible=0, size=(1920,1080))
    # display.start()
    # user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

    # options = Options()
    # options.add_argument('--window-size=1420,1080')
    # options.add_argument('--headless')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--no-sandbox')
    # options.add_argument('user-agent={0}'.format(user_agent))
    # driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)

    # driver.get(url)
    # time.sleep(1)
    # html = driver.page_source
    # soup = BeautifulSoup(html, "lxml")
    # site_json = json.loads(soup.find("body").text)

    res = requests.get(url, headers=header)
    site_json = json.loads(res.text)
    return site_json
    
    # site_json = requests.get(url).json()
    # result_json = json.loads(site_json.text, encoding='utf-8')
    # return site_json

    # bs4 만 쓸 경우 - Selenium 미 사용 시(단, Response 307 뜸)
    # html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    # soup = BeautifulSoup(html, "html.parser")
    # site_json = json.loads(soup.text)
    # result = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    # soup = BeautifulSoup(result.text, "html.parser")
    # for i in site_json:
    #     print(i)
