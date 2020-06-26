import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import plotly.graph_objects as go

import pymysql
import streamlit as st

import datetime

purpose = ['사무용', '게임용', '고성능 작업용(영상 편집 등)']
cpu_brand = ['Intel', 'AMD']
gpu_brand = ['GForce', 'Radeon']
today = datetime.date.today()
yesterday = today - relativedelta(months = 1)

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

st.sidebar.header("부품 가격 동향 옵션")
st.sidebar.markdown("선택한 부품에 대한 가격 정보를 조정하는 설정 창 입니다.")
start_date = st.sidebar.date_input('부품 가격 동향 시작 일자', yesterday)
end_date = st.sidebar.date_input("부품 가격 동향 종료 일자", today)
# Main Title Setting 
st.title("컴못알을 위한 조립 PC 견적 참고 키트({})".format(purpose_button))
st.markdown(
    """
    조립 PC에 대해 잘 알지 못하는 사람(컴못알)은 컴퓨터를 구매할 때 무엇을 고려해야 하는지 잘 알지 못합니다. 이런 사람들을 위해 참고할 수 있는 대시보드입니다.

    이 대시보드는 다음과 같은 문제를 해결할 수 있을 것이라 예상합니다.

    1. 구매자의 목적에 부합한 PC 부품 선택

    2. PC의 호환성과 성능 병목 현상 문제 방지

    이 대시보드는 언제까지나 참고용이며, 구매 전 전문가에게 상담하는 것을 추천합니다.

    이 페이지는 현재 제작 중입니다.

    추천 사이트: [IT 인벤 PC 견적 게시판](http://www.inven.co.kr/board/it/2631)

    대시보드 최종 수정일: 2020/06/26

    [See Source Code](https://github.com/SSANGMAN/Danawa)
    """)

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

def CurrentPrice(dataframe, component):
    recent_time = datetime.datetime.now().hour
    df = dataframe.loc[(dataframe['HOUR'] == recent_time) & (dataframe['PRICE'] < int(budget_box) * 10000)]
    
    while len(df) == 0:
        df = dataframe.loc[(dataframe['HOUR'] == recent_time) & (dataframe['PRICE'] < int(budget_box) * 10000)]
        recent_time -= 1

        if len(df) != 0:
            break
    if (component == 'cpu'):
        return df[['NAME', 'PRICE', 'SOCKET']]

    elif component == 'mb':
        return df[['BRAND', 'NAME', 'PRICE', 'SOCKET']]
    
    elif component == 'gpu':
        return df[['BRAND','NAME', 'PRICE']]

    elif component == 'ram':
        return df[['NAME', 'PRICE', 'PURPOSE', 'BRAND']]


cpu_df = import_data(table = "cpu", start_date = today, end_date = today)
cpu_df = CurrentPrice(cpu_df, component = 'cpu')

if selected_cpu_brand == 'Intel':
    filter_cpu_df = cpu_df[cpu_df['NAME'].str.contains(r'인텔')]
elif selected_cpu_brand == 'AMD':
    filter_cpu_df = cpu_df[cpu_df['NAME'].str.contains(r'AMD')]

st.dataframe(filter_cpu_df)
select_cpu = st.selectbox("CPU 선택", filter_cpu_df['NAME'].unique().tolist())
selected_cpu_socket = filter_cpu_df.loc[filter_cpu_df['NAME'] == select_cpu]['SOCKET'].unique()
subtract_cpu_budget = int(budget_box) * 10000 - filter_cpu_df.loc[filter_cpu_df['NAME'] == select_cpu]['PRICE'].unique()

st.markdown(
    """
    아래 그래프는 선택한 CPU의 가격 동향입니다. 이 그래프를 통해서 현재 CPU의 가격이 부풀려진 가격인지 확인 할 수 있습니다.
    """
)
vis_cpu_df = import_data(table = "cpu", start_date = start_date, end_date = end_date)
daily_cpu_price = vis_cpu_df.groupby(["CRAWL_DATE", "NAME"])['PRICE'].mean().reset_index().set_index("CRAWL_DATE")
st.line_chart(daily_cpu_price.loc[daily_cpu_price['NAME'] == select_cpu]['PRICE'])

st.text("잔여 예산: {}원".format(subtract_cpu_budget[0]))


st.header("Main Board 선택")
st.markdown(
    """
    CPU를 선택했다면, 이제 메인보드를 선택해야합니다. 메인보드는 쉽게 말해, 컴퓨터의 혈관이자 신경계라고 생각하시면 됩니다. 

    컴퓨터는 CPU, 램, 그래픽카드 등으로 구성되어 있는데, 이러한 부품들은 서로 따로 놀 수 는 없고 각 부품들을 하나로 연결해주는 회로와 신호를 밖으로 보낼 수 있는 출력 포트가 필요합니다. 

    이 기능을 가지고 있는 부품이 메인보드입니다. 쉽게 말해, 컴퓨터의 안정성을 좌우하기 때문에 예산을 아끼지 말하야 하는 부품 중 하나라고 할 수 있습니다. 

    메인보드에는 CPU를 장착할 수 있는 소켓이 존재합니다. 이런 소켓은 CPU마다 상이할 수 있기 때문에 위에서 선택한 CPU와 호환이 되는 메인보드를 선택해야 합니다.
    """
)

st.subheader("제조사 선택")
st.markdown(
    """
    이제 메인보드의 브랜드를 선택해야 합니다. 메인보드 제조사는 크게 MSI, ASRock, GIGABYTE, ASUS까지 네 곳이 있습니다. BIOSTAR는 제품 이슈가 너무 많아 배제합니다.  
    
    아래 브랜드를 선택하면 제조사별 특징에 대해 설명이 함께 나와있으므로 참고하여 선택합니다.
    """
)
mb_df = import_data(table = "mainboard", start_date = today, end_date = today)
mb_df = CurrentPrice(mb_df, component = 'mb')
mb_brand = st.selectbox("메인보드 제조사 선택", mb_df['BRAND'].unique())

if mb_brand == 'MSI':
    st.markdown(
        """
        가성비 있는 가격에 독자적인 프로그램을 통해 안정성 확보. 하지만 고성능 PC에는 부적합하다는 의견이 많다.
        """
    )
elif mb_brand == "ASUS":
    st.markdown(
        """
        버그가 거의 없어 오버클럭(강제 성능 향상) 등 고성능 PC에 적합하다. 하지만 높은 가격대를 보이는 브랜드.
        """
    )
elif mb_brand == "ASRock":
    st.markdown(
        """
        ASUS의 산하 마이너 브랜드. 높은 가성비를 모토로하며 어느정도 안정성도 보장한다. 하지만 고성능 PC에는 부적합하다는 의견이 많다.
        """
    )
elif mb_brand == "GIGABYTE":
    st.markdown(
        """
        ASUS보다 가성비가 좋은 편이며 잔 버그가 거의 없어 안정성이 뛰어나다. 다만, 국내 AS평이 좋지 않다는 것이 단점.
        """
    )

st.subheader("칩셋 선택")
st.markdown(
    """
    선택한 CPU에 맞는 소켓을 가진 메인보드를 선택하는 과정은 '칩셋' 또한 고려해야합니다.

    칩셋에 대한 정보는 제품 이름에서 Z490-A, B460M 등과 같은 네이밍을 확인하면 됩니다.

    칩셋은 포트 수, 장착 슬롯 등 편의성의 차이가 가장 두드러집니다. 또한 상위 칩셋 제품일 수록 전원부가 더 튼튼하다거나 방열판이 더많이 붙어있다는 차이가 존재합니다.

    따라서, 고성능의 CPU를 사용할수록 안정성을 위해 상위 칩셋의 제품을 사용하는 것이 일반적입니다.

    다음 내용은 칩셋에 대한 간단한 설명입니다.
    """
)
if selected_cpu_brand == 'Intel':
    st.markdown(
        """
        H310: 최하위 칩셋. 사무용 및 저사양 게이밍을 목적으로 견적을 구성한다면 추천

        B460: 보급형 칩셋. 일반적인 게이밍 PC로 견적을 구성한다면 추천

        Z490: 하이엔드용 칩셋. 
        """
    )
elif selected_cpu_brand == 'AMD':
    st.markdown(
        """
        A320: 최하위 칩셋. 극한의 가성비를 원한다면 추천

        B450: 보급형 칩셋. 일반적인 게이밍 PC로 견적을 구성한다면 추천

        X470: 뭔가 애매한 포지션을 유지하고있는 칩셋. 이거를 선택할바엔 X570 추천

        X570: 하이엔드용 칩셋. 높아진 칩셋 발열량을 감당하기 위해 메인보드 자체에 소평 팬이 장착되어있음.
        
        메인보드 선택에 대한 추가적인 정보는 다음 링크를 참고하세요
        
        [CPU에 걸맞은 메인보드 찾기, 인텔 9세대 커피레이크 리프레시 메인보드 고르기](http://www.ilovepc.co.kr/news/articleView.html?idxno=21238)
        """
    )
st.text(
    """
    선택한 CPU는 {} 입니다. 

    이 CPU에 맞는 소켓 {} 을 가진 {}사 메인보드를 검색합니다.
    """.format(select_cpu, selected_cpu_socket[0], mb_brand))

filter_mb_df = mb_df.loc[(mb_df['SOCKET'] == selected_cpu_socket[0])&(mb_df['PRICE'] < subtract_cpu_budget[0]) & (mb_df['BRAND'] == mb_brand)]
st.dataframe(filter_mb_df)
select_mb = st.selectbox("메인보드 선택", filter_mb_df['NAME'].unique().tolist())
subtract_mb_budget = int(subtract_cpu_budget) - filter_mb_df.loc[filter_mb_df['NAME'] == select_mb]['PRICE'].unique()

vis_mb_df = import_data(table = "mainboard", start_date = start_date, end_date = end_date)
daily_mb_price = vis_mb_df.groupby(["CRAWL_DATE", "NAME"])['PRICE'].mean().reset_index().set_index("CRAWL_DATE")
st.line_chart(daily_mb_price.loc[daily_mb_price['NAME'] == select_mb]['PRICE'])

st.text("잔여 예산: {}원".format(subtract_mb_budget[0]))

if (purpose_button == '게임용') |(purpose_button == '고성능 작업용(영상 편집 등)'):
    st.header("GPU 선택")
    st.markdown(
        """
        드디어, 게임과 작업에 가장 중요하다고 볼 수 있는 그래픽카드(GPU)를 선택하는 단계입니다. 성능에 따라 가장 많은 비용이 필요할 수 있습니다.

        GPU의 브랜드는 일반적으로 Nvidia의 GForce, AMD의 Radeon이 있습니다. 예전부터 GForce는 게임, Radeon은 3D 작업, 영상 편집에 유리하다는 인식이 강했습니다.

        여기에서 클럭 수가 어떻다, VRAM이 어떻다를 설명하기에는 너무 복잡하기 때문에 생략하고 간단하게 설명만 하고 넘어가겠습니다.

        Radeon은 영상편집같은 다중 작업에 유리하고 중간 사양급 게임을 하기엔 훨씬 유리합니다. 그러나, 게임 위주로 컴퓨터를 사용한다면 지포스가 가성비 대비 훨씬 유리합니다.

        세부적인 정보는 다음 링크를 통해 확인할 수 있습니다.
        
        [라데온 지포스 그래픽카드 차이점 비교!](https://m.blog.naver.com/PostView.nhn?blogId=lks09251&logNo=221269840032&proxyReferer=https:%2F%2Fwww.google.com%2F)
        """ 
    )
    selected_gpu_brand = st.selectbox("GPU 브랜드 선택", gpu_brand)
        
    gpu_df = import_data(table = 'gpu', start_date = today, end_date = today)
    gpu_df = CurrentPrice(gpu_df, component = 'gpu')

    if selected_gpu_brand == 'GForce':
        filter_gpu_df = gpu_df[gpu_df['NAME'].str.contains(r'지포스')]
    elif selected_cpu_brand == 'Radeon':
        filter_gpu_df = gpu_df[gpu_df['NAME'].str.contains(r'라데온')]

    filter_gpu_df = filter_gpu_df.loc[(filter_gpu_df['PRICE'] < subtract_mb_budget[0])]

    st.dataframe(filter_gpu_df[['NAME', 'PRICE']])
    select_gpu = st.selectbox("GPU 선택", filter_gpu_df['NAME'].unique().tolist())
    subtract_gpu_budget = int(subtract_mb_budget) - filter_gpu_df.loc[filter_gpu_df['NAME'] == select_gpu]['PRICE'].unique()

    st.markdown(
    """
    아래 그래프는 선택한 GPU의 가격 동향입니다. 이 그래프를 통해서 현재 CPU의 가격이 부풀려진 가격인지 확인 할 수 있습니다.
    """
)
    vis_gpu_df = import_data(table = "gpu", start_date = start_date, end_date = end_date)
    daily_gpu_price = vis_gpu_df.groupby(["CRAWL_DATE", "NAME"])['PRICE'].mean().reset_index().set_index("CRAWL_DATE")
    st.line_chart(daily_gpu_price.loc[daily_gpu_price['NAME'] == select_gpu]['PRICE'])

    st.text("잔여 예산: {}원".format(subtract_gpu_budget[0]))

else:
    pass

st.header("RAM 선택")
st.markdown(
    """
    여기까지 오느라 수고 많으셨습니다. 이제 PC의 성능을 좌우하는 부품 선택의 마지막 RAM입니다.

    RAM은 쉽게 말해 컴퓨터가 한 번에 많은 일을 할 수 있는 규모를 결정하는 부품입니다.

    CPU가 아무리 일을 많이 할 수 있어봤자, 이를 수용할 수 있는 책상이 없다면 말짱 도루묵이 됩니다. 이 때, 책상의 역할을 하는 것이 RAM입니다.
    
    RAM을 선택하는 방법은 정말 단순하게 생각하자면 (그냥 삼성 RAM을 사용하시면 됩니다.)

    일반적으로, 게임용 PC 견적에는 8g x 2 = 16g를 추천합니다.
    """
)
ram_df = import_data(table = 'ram', start_date = today, end_date = today)
ram_df = CurrentPrice(ram_df, component = 'ram')
ram_brand = st.selectbox("RAM 브랜드 선택", ram_df['BRAND'].unique())

filter_ram_df = ram_df.loc[(ram_df['PURPOSE'] == 'PC용') & (ram_df['BRAND'] == ram_brand)]
st.dataframe(filter_ram_df.drop(columns = ['PURPOSE', 'BRAND']))

select_ram = st.selectbox("RAM 선택", filter_ram_df['NAME'].tolist())

vis_ram_df = import_data(table = "ram", start_date = start_date, end_date = end_date)
daily_ram_price = vis_ram_df.groupby(["CRAWL_DATE", "NAME"])['PRICE'].mean().reset_index().set_index("CRAWL_DATE")
st.line_chart(daily_ram_price.loc[daily_ram_price['NAME'] == select_ram]['PRICE'])

ram_quantity = int(st.text_input("RAM 수량"))
subtract_ram_budget = int(subtract_gpu_budget) - (filter_ram_df.loc[filter_ram_df['NAME'] == select_ram]['PRICE'].unique()) * ram_quantity

st.text("잔여 예산: {}원".format(subtract_ram_budget[0]))