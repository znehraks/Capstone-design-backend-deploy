from scrapper import scrapper
import json
import csv
import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import io
import sys


# 먼저 학교 이름으로 학교의 중심 위도,경도를 알아오기
def find_address(univ_name):
    # 서울소재대학교 주소 csv에서 가져옴
    univ = open('seoul_universities.csv', 'r')
    univ_r = csv.reader(univ)
    # univ_address에 필요한 대학교 주소 데이터 추출
    univ_address = ""
    for i in univ_r:
        if univ_name == i[3]:
            univ_address = i[8]
            break
    univ.close()
    print(univ_address)

    url = f"https://map.naver.com/v5/api/search?caller=pcweb&query={univ_address}"

    sys.stdout.reconfigure(encoding='utf-8')
    chrome_options = Options()
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(
        executable_path=".\\chromedriver.exe", options=chrome_options)

    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    address_json = json.loads(soup.find("body").text)
    driver.close()
    return address_json


address_json = find_address("경희대학교")
try:
    address_lon = float(address_json["result"]["place"]["list"][0]["x"])
    address_lat = float(address_json["result"]["place"]["list"][0]["y"])
except:
    address_lon = float(
        address_json["result"]["address"]["jibunsAddress"]["list"][0]["x"])
    address_lat = float(
        address_json["result"]["address"]["jibunsAddress"]["list"][0]["y"])

print(address_lat, address_lon)

# 알아 온 위도, 경도를 바탕으로 상하좌우,중심 위도경도를 구함
center_lat = address_lat
center_lon = address_lon
btm_lat = address_lat - 0.0159
left_lon = address_lon - 0.0412
top_lat = address_lat + 0.0159
right_lon = address_lon + 0.0412


site_json = scrapper(center_lat, center_lon, btm_lat,
                     left_lon, top_lat, right_lon)

items = site_json["data"]["ARTICLE"]
refined_items = []
for i in items:
    refined_items.append({
        "lgeo": i["lgeo"],
        "count": i["count"],
        "lat": i["lat"],
        "lon": i["lon"]
    })

# 나온 매물 리스트들 좌표로 각각의 lgeo를 인덱스로 하여

# 그 lego의 lat, lon을 이용한 거리이용 가중치를 모두 구함
# 학교 좌표와 해당 매물과의 거리를 모두 구하여(맨하탄거리) 1위부터 꼴찌까지 가중치를 구함(이전에, Q2의 최대거리에서 필터링하여 해당 거리를 벗어나는 좌표에 있는 항목은 이 단계에서 걸러냄)


# 각 매물에서 해당 구에 속한 지하철역중 가장 가까운 것의 거리를 가중치로 매겨서 그것 역시 1위부터 꼴찌까지 가중치로 매김


# 구 별 범죄율로 가중치 구함(위도,경도 값으로 해당 점이 어느 구에 속하는지 판별 후, 그 구의 범죄율 가중치로 정함)


# 매물 수로 난도 가중치를 구함(나온 refined_items의 count가 많은 것 순으로 높은 점수를 매겨서 등수 별로 순차적인 가중치를 정함
# 예. 매물이 총 50개이면 1위 100점, 2위 98점, 3위 96점 ... 50위 0점)


# 최종 Top5 혹은 Top3의 lat, lon 좌표를 구함
# 이 Top에 포함되는 항목의 구체적인 정보 서술 및 시각화
# 지도에 마크로 표시해주는 방법도 좋으리라 생각함 + 매물 및 동네의 추가 정보까지 제공

print(refined_items)
