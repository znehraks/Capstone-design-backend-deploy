import requests
from bs4 import BeautifulSoup
import json
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# import time
# import io
# import sys
# # pc버전 api
# # url = f"https://new.land.naver.com/api/articles/clusters?cortarNo=1141011700&zoom=15&markerId&markerType&selectedComplexNo&selectedComplexBuildingNo&fakeComplexMarker&realEstateType=APT%3AOPST%3AABYG%3AOBYG%3AGM%3AOR%3AVL%3ADDDGG%3AJWJT%3ASGJT%3AHOJT&tradeType=&tag=%3A%3A%3A%3A%3A%3A%3ASMALLSPCRENT%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=false&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&leftLon=126.8992045&rightLon=126.9317987&topLat=37.5879848&bottomLat=37.576930950000005"

# # 명지대학교 인문캠퍼스 위치가 중심인 지도.
# # center_lat = 37.5785302
# # center_lon = 126.9234694
# # btm_lat = 37.5625943
# # left_lon = 126.8822707
# # top_lat = 37.5944627
# # right_lon = 126.9646681


# def scrapper(center_lat,
#              center_lon,
#              btm_lat,
#              left_lon,
#              top_lat,
#              right_lon):
#     url = f"https://m.land.naver.com/cluster/clusterList?view=atcl&rletTpCd=OR&tradTpCd=A1%3AB1%3AB2%3AB3&z=15&lat={center_lat}&lon={center_lon}&btm={btm_lat}&lft={left_lon}&top={top_lat}&rgt={right_lon}&pCortarNo="

#     # sys.stdout.reconfigure(encoding='utf-8')
#     # chrome_options = Options()
#     # chrome_options.add_experimental_option(
#     #     "excludeSwitches", ["enable-logging"])
#     # driver = webdriver.Chrome(
#     #     executable_path=".\\chromedriver.exe", options=chrome_options)

#     header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
#               'Referer': 'https://m.land.naver.com/'}
#     # driver.get(url)
#     # html = driver.page_source
#     # soup = BeautifulSoup(html, "lxml")
#     # site_json = json.loads(soup.find("body").text)
#     # driver.close()
#     res = requests.get(url, headers=header)
#     site_json = json.loads(res.text)
#     return site_json

#     # bs4 만 쓸 경우 - Selenium 미 사용 시(단, Response 307 뜸)
#     # html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
#     # soup = BeautifulSoup(html, "html.parser")
#     # site_json = json.loads(soup.text)
#     # result = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
#     # soup = BeautifulSoup(result.text, "html.parser")
#     # for i in site_json:
#     #     print(i)

import requests
from bs4 import BeautifulSoup
import json
# https://www.dabangapp.com/api/3/marker/multi-room?api_version=3.0.1&call_type=web&filters=%7B%22multi_room_type%22%3A%5B0%2C1%2C2%5D%2C%22selling_type%22%3A%5B0%2C1%2C2%5D%2C%22deposit_range%22%3A%5B0%2C999999%5D%2C%22price_range%22%3A%5B0%2C999999%5D%2C%22trade_range%22%3A%5B0%2C999999%5D%2C%22maintenance_cost_range%22%3A%5B0%2C999999%5D%2C%22room_size%22%3A%5B0%2C999999%5D%2C%22supply_space_range%22%3A%5B0%2C999999%5D%2C%22room_floor_multi%22%3A%5B1%2C2%2C3%2C4%2C5%2C6%2C7%2C-1%2C0%5D%2C%22division%22%3Afalse%2C%22duplex%22%3Afalse%2C%22room_type%22%3A%5B1%2C2%5D%2C%22use_approval_date_range%22%3A%5B0%2C999999%5D%2C%22parking_average_range%22%3A%5B0%2C999999%5D%2C%22household_num_range%22%3A%5B0%2C999999%5D%2C%22parking%22%3Afalse%2C%22animal%22%3Afalse%2C%22short_lease%22%3Afalse%2C%22full_option%22%3Afalse%2C%22built_in%22%3Afalse%2C%22elevator%22%3Afalse%2C%22balcony%22%3Afalse%2C%22loan%22%3Afalse%2C%22safety%22%3Afalse%2C%22pano%22%3Afalse%2C%22deal_type%22%3A%5B0%2C1%5D%7D&location=%5B%5B126.9280038%2C37.5441994%5D%2C%5B126.9598038%2C37.6265994%5D%5D&version=1&zoom=15

# btm_lat 126.9001522 차이: 0.0437516
# left_lon 37.5708922 차이: 0.0145072
# top_lat 126.948904 차이: 0.0050002
# right_lon 37.5903801 차이: 0.0049808

# 명지대 위도 126.9439038
# 명지대 경도 37.5853994
# 126.9280038 37.5441994 126.9598038 37.6265994


def dabang_scrapper(btm_lat,
                    left_lon,
                    top_lat,
                    right_lon):
    url = f"https://www.dabangapp.com/api/3/marker/multi-room?api_version=3.0.1&call_type=web&filters=%7B%22multi_room_type%22%3A%5B0%2C1%2C2%5D%2C%22selling_type%22%3A%5B0%2C1%2C2%5D%2C%22deposit_range%22%3A%5B0%2C999999%5D%2C%22price_range%22%3A%5B0%2C999999%5D%2C%22trade_range%22%3A%5B0%2C999999%5D%2C%22maintenance_cost_range%22%3A%5B0%2C999999%5D%2C%22room_size%22%3A%5B0%2C999999%5D%2C%22supply_space_range%22%3A%5B0%2C999999%5D%2C%22room_floor_multi%22%3A%5B1%2C2%2C3%2C4%2C5%2C6%2C7%2C-1%2C0%5D%2C%22division%22%3Afalse%2C%22duplex%22%3Afalse%2C%22room_type%22%3A%5B1%2C2%5D%2C%22use_approval_date_range%22%3A%5B0%2C999999%5D%2C%22parking_average_range%22%3A%5B0%2C999999%5D%2C%22household_num_range%22%3A%5B0%2C999999%5D%2C%22parking%22%3Afalse%2C%22animal%22%3Afalse%2C%22short_lease%22%3Afalse%2C%22full_option%22%3Afalse%2C%22built_in%22%3Afalse%2C%22elevator%22%3Afalse%2C%22balcony%22%3Afalse%2C%22loan%22%3Afalse%2C%22safety%22%3Afalse%2C%22pano%22%3Afalse%2C%22deal_type%22%3A%5B0%2C1%5D%7D&location=%5B%5B{btm_lat}%2C{left_lon}%5D%2C%5B{top_lat}%2C{right_lon}%5D%5D&version=1&zoom=15"

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
              'Referer': 'https://m.dabangapp.com/'}
    res = requests.get(url, headers=header)
    site_json = json.loads(res.text)
    return site_json


# btm_lat = 126.9439038 - 0.0159
# left_lon = 37.5853994 - 0.0412
# top_lat = 126.9439038 + 0.0159
# right_lon = 37.5853994 + 0.0412
# # print(btm_lat,
# #       left_lon,
# #       top_lat,
# #       right_lon)
# print(scrapper(btm_lat,
#                left_lon,
#                top_lat,
#                right_lon))
