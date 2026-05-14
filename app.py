import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# 페이지 설정 (가장 상단에 위치해야 함)
st.set_page_config(page_title="KGC Insight - 실시간 연동", layout="wide")

# 1. 구글 스프레드시트 연결 (Streamlit Cloud의 Secrets 설정을 참조함)
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 2. 데이터 불러오기 (시트 전체 읽기, 1분마다 캐시 갱신)
    # 이 함수가 실제 스프레드시트의 데이터를 가져오는 핵심 코드입니다.
    df = conn.read(ttl="1m")
    
    # 헬퍼 함수: 특정 라벨명을 가진 행의 데이터를 가져옴
    def get_row_data(label_name):
        return df[df['label'] == label_name].iloc[0]

    # 이미지(image_bcd33d.png)의 label 열 기준으로 데이터 추출
    sales_data = get_row_data('수도권 판매량')
    target_data = get_row_data('핵심 타겟층(2030)')
    keyword_data = get_row_data('스포츠 키워드 언급')
    review_data = get_row_data('긍정 리뷰 비율')
    
    # 7행의 요약 텍스트 추출 (시트의 A7 셀에 해당하는 위치)
    summary_text = df.iloc[5, 0] if len(df) > 5 else "분석 데이터를 불러오는 중입니다."

except Exception as e:
    st.error(f"데이터 연동 중 오류 발생: {e}")
    # 오류 시 대시보드 중단을 방지하기 위한 기본값
    summary_text = "연결 설정을 확인해주세요."
    sales_data = target_data = keyword_data = review_data = {'value': 0, 'delta': 'N/A'}

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    div[data-testid="metric-container"] {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #c62828;
    }
    </style>
    """, unsafe_allow_now=True)

st.title("🍎 에브리타임 밸런스 실시간 퍼포먼스")
st.caption("구글 스프레드시트(kgcdata260514)와 실시간 동기화 중입니다.")

m1, m2, m3, m4 = st.columns(4)

with m1:
    # 0.95 -> 95% 변환 표시
    val = f"{float(sales_data['value']) * 100:.0f}%" if isinstance(sales_data['value'], (int, float)) else sales_data['value']
    st.metric(label="수도권 판매 성장", value=val, delta=sales_data['delta'])

with m2:
    # 80.00% 형식 유지
    val = f"{float(target_data['value']) * 100:.1f}%" if isinstance(target_data['value'], (int, float)) else target_data['value']
    st.metric(label="2030 타겟 비중", value=val, delta=target_data['delta'])

with m3:
    # 0.3 -> +30% 변환
    val = f"+{float(keyword_data['value']) * 100:.0f}%" if isinstance(keyword_data['value'], (int, float)) else keyword_data['value']
    st.metric(label="스포츠 키워드 언급", value=val, delta=keyword_data['delta'])

with m4:
    # 82.40% 형식
    val = f"{float(review_data['value']) * 100:.1f}%" if isinstance(review_data['value'], (int, float)) else review_data['value']
    st.metric(label="긍정 리뷰 비율", value=val, delta=review_data['delta'])

st.markdown("---")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("💡 주간 마케팅 인사이트")
    st.info(summary_text)
    st.success("**팀장 제언:** 2030의 스포츠 활동 접점(테니스, 등산) 마케팅을 강화하고, 패키징 개봉성 이슈를 조속히 해결할 것.")

with col_right:
    st.subheader("지표별 성과 시각화")
    # 시각화를 위한 임시 데이터프레임
    chart_df = pd.DataFrame({
        '지표': ['수도권', '2030비중', '키워드', '긍정리뷰'],
        '성과(%)': [float(sales_data['value'])*100, float(target_data['value'])*100, float(keyword_data['value'])*100, float(review_data['value'])*100]
    })
    fig = px.bar(chart_df, x='지표', y='성과(%)', color='지표', color_discrete_sequence=['#c62828', '#1e3a8a', '#fbbf24', '#2dd4bf'])
    fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', height=350)
    st.plotly_chart(fig, use_container_width=True)
