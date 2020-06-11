import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import plotly.graph_objects as go

import pymysql
import streamlit as st

import datetime

purpose = ['사무용', '게임용', '고성능 작업용(영상 편집 등)']
cpu_brand = ['Intel', 'AMD']
today = datetime.date.today()

def import_data(table, start_date, end_date):
    connect = pymysql.connect(host = 'localhost', user = 'root', password = '4643', db = 'danawa', charset = 'utf8mb4')
    cur = connect.cursor()
    
    col_sql = "SHOW FULL COLUMNS FROM {}".format(table)
    cur.execute(col_sql)
    col_info = cur.fetchall()
    
    columns = [col[0] for col in col_info]
    
    sql = "SELECT * FROM {} WHERE DATE(CRAWL_DATE) >= '{}' AND DATE(CRAWL_DATE) <= '{}'".format(table,start_date, end_date)
    print(sql)
    
    cur.execute(sql)
    result = cur.fetchall()
    
    connect.close()
    
    df = pd.DataFrame(result, columns = columns)
    
    return df

# Main Title Setting 
st.title("컴못알을 위한 조립 PC 견적 참고 키트")
st.markdown(
    """
    조립 PC에 대해 잘 알지 못하는 사람(컴못알)은 컴퓨터를 구매할 때 무엇을 고려해야 하는지 잘 알지 못합니다. 이런 사람들을 위해 참고할 수 있는 대시보드입니다.

    이 대시보드는 다음과 같은 문제를 해결할 수 있을 것이라 예상합니다.

    1. 구매자의 목적에 부합한 PC 부품 선택

    2. PC의 호환성과 성능 병목 현상 문제 방지

    이 대시보드는 언제까지나 참고용이며, 구매 전 전문가에게 상담하는 것을 추천합니다.

    이 페이지는 현재 제작 중입니다.

    추천 사이트: [IT 인벤 PC 견적 게시판](http://www.inven.co.kr/board/it/2631)

    대시보드 최종 수정일: 2020/06/11

    [See Source Code](https://github.com/SSANGMAN/Danawa)
    """)

# Sidebar Setting
## Condition
st.sidebar.header("성향 파악")
st.sidebar.markdown("""구매자의 성향을 파악합니다.""")

purpose_button = st.sidebar.selectbox(
    '구매 목적: PC를 구매하는 목적을 선택해주세요. 여러 가지 목적이 존재한다면, 가장 비중이 높은 것을 선택합니다.', options = purpose,
    index = 0)

budget_box = st.sidebar.text_input(
    "예산(만원): PC를 구매할 수 있는 예산을 아래에 기입해주세요. 예산을 결정하기 어렵다면 아래를 참고해주세요.")

st.sidebar.text(
    """
    *참고용*

    사무용: 50만원 미만

    중저사양 게임용(리그 오브 레전드, 메이플스토리, 피파4 등): 80만원 미만

    고사양 게임용(배틀그라운드, 오버워치): 130만원 미만

    80만원 미만으로도 고사양 게임을 플레이 할 수 있습니다. 
    
    그러나, 옵션 타협을 고려해야 합니다. 
    """
)

# MainPage Setting
st.header("CPU 선택")
st.markdown(
    """
    모든 PC의 선택은 CPU에서부터 시작합니다. CPU의 브랜드는 Intel과 AMD가 있습니다. 
    
    예전에야 'CPU하면 Intel이지!' 라고했지만 최근에는 AMD의 라이젠이 급부상하며, 대부분의 구매자는 뭘 사야할지 고민하곤 합니다.

    선택에 있어서 간단하게 설명하자면, 오직 게임만 하는 구매자라면 Intel을 추천합니다. 라이젠을 제대로 활용하기 위해선 바이오스 업데이트나 오버클럭을 활용해야 하기 때문입니다.

    구구절절 설명하기에는 어려움이 따르기 때문에 링크 달아두겠습니다. CPU의 선택은 메인보드와 GPU의 선택에 있어서 중요하기 때문에 확인해보는 것을 추천합니다.

    [인텔, 라이젠 CPU 초심자용 기초 가이드](https://nounow.net/2020/03/25/%EC%9D%B8%ED%85%94-%EB%9D%BC%EC%9D%B4%EC%A0%A0-cpu-%EA%B5%AC%EB%A7%A4-%EA%B0%80%EC%9D%B4%EB%93%9C/)

    Intel과 AMD 중 결정을 하셨다면 다음을 선택해주세요!
    """)
selected_cpu_brand = st.selectbox("CPU 제조사", cpu_brand)
st.markdown(
    """
    CPU 제조사를 선택하셨다면, 이제 용도에 맞는 CPU를 선택해야 합니다. 좌측에서 선택하셨던 PC의 용도를 고려하여 제품을 보여드리겠습니다.

    제품의 순서는 현재 Danawa에서 판매 순위를 기준으로 오름차순으로 정렬됩니다. (판매 순위 1위, 2위, 3위...) 
    
    한 가지 주의해야 할 점은 컴퓨터는 CPU만으로 작동하지 않는다는 것입니다. 따라서, 남은 부품에 대한 예산을 고려하고 선택하셔야 합니다.
    """)

def CurrentPrice(dataframe):
    recent_time = datetime.datetime.now().hour
    df = dataframe.loc[(dataframe['HOUR'] == recent_time) & (dataframe['PRICE'] < int(budget_box) * 10000)]
    
    while len(df) == 0:
        df = dataframe.loc[(dataframe['HOUR'] == recent_time) & (dataframe['PRICE'] < int(budget_box) * 10000)]
        recent_time -= 1

        if len(df) != 0:
            break
    
    return df[['NAME', 'PRICE']]

cpu_df = import_data(table = "cpu", start_date = today, end_date = today)
cpu_df = CurrentPrice(cpu_df)

if selected_cpu_brand == 'Intel':
    filter_cpu_df = cpu_df[cpu_df['NAME'].str.contains(r'인텔')]
elif selected_cpu_brand == 'AMD':
    filter_cpu_df = cpu_df[cpu_df['NAME'].str.contains(r'AMD')]

st.dataframe(filter_cpu_df)

