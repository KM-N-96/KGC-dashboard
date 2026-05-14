import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# 페이지 설정 (반드시 모든 st 함수 중 가장 위에 와야 합니다)
st.set_page_config(page_title="KGC Insight - 실시간 연동", layout="wide")

# 1. 구글 스프레드시트 연결 (secrets.toml 설정 기반)
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. 데이터 불러오기 (이미지상의 시트 구조 반영)
try:
    # 데이터 로드 (시트 전체 읽기)
    df = conn.read(ttl="1m") # 1분마다 갱신
    
    # 헬퍼 함수: 라벨로 값을 찾아오는 기능
    def get_row(label):
        return df[df['label'] == label].iloc[0]

    # 각 지표 데이터 추출
    sales_row = get_row('수도권 판매량')
    target_row = get_row('핵심 타겟층(2030)')
    keyword_row = get_row('스포츠 키워드 언급')
    review_row = get_row('긍정 리뷰 비율')
    
    # 7행의 요약 텍스트 (A7 셀 부근 데이터 추출)
    # pandas 인덱스 기준으로 6번이 시트의 7행입니다.
    summary_text = df.iloc[5, 0] if len(df) > 5 else "데이터를 분석 중입니다."

except Exception as e:
    st.error(f"데이터 연동 중 오류 발생: {e}")
    # 오류 발생 시 대시보드가 깨지지 않도록 기본값 설정
    summary_text = "데이터 연결 상태를 확인해주세요."
    sales_row = target_row = keyword_row = review_row = {'value': 0, 'delta': 'N/A'}

# 커스텀 CSS (KGC 브랜드 컬러 및 카드 디자인)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    div[data-testid="metric-container"] {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #c62828;
    }
    </style>
    """, unsafe_allow_now=True)

# --- UI 렌더링 시작 ---
st.title("🍎 에브리타임 밸런스 실시간 성과")
st.caption("구글 스프레드시트 데이터와 1분 간격으로 동기화 중입니다.")

# 상단 KPI 섹션
m1, m2, m3, m4 = st.columns(4)

with m1:
    # 0.95 -> 95% 형태로 표시
    val = f"{float(sales_row['value']) * 100:.1f}%" if isinstance(sales_row['value'], (int, float)) else sales_row['value']
    st.metric(label="수도권 판매 성장", value=val, delta=sales_row['delta'])

with m2:
    val = f"{float(target_row['value']) * 100:.1f}%" if isinstance(target_row['value'], (int, float)) else target_row['value']
    st.metric(label="2030 타겟 비중", value=val, delta=target_row['delta'])

with m3:
    # 0.3 -> +30% 형태로 표시
    k_val = f"+{float(keyword_row['value']) * 100:.1f}%" if isinstance(keyword_row['value'], (int, float)) else keyword_row['value']
    st.metric(label="스포츠 키워드 언급", value=k_val, delta=keyword_row['delta'])

with m4:
    val = f"{float(review_row['value']) * 100:.1f}%" if isinstance(review_row['value'], (int, float)) else review_row['value']
    st.metric(label="긍정 리뷰 비율", value=val, delta=review_row['delta'])

st.markdown("---")
col_info, col_chart = st.columns([1, 1])

with col_info:
    st.subheader("💡 금주 핵심 인사이트")
    st.info(summary_text)
    
    st.success("""
    **팀장 제언:**
    - 수도권 편의점 채널에 '스포츠 한정판' 패키지 우선 배정 검토
    - 7행의 요약문은 시트에서 직접 수정하면 실시간으로 반영됩니다.
    """)

with col_chart:
    st.subheader("주요 지표 시각화")
    # 간단한 비교 차트
    chart_data = pd.DataFrame({
        '지표': ['수도권', '2030', '키워드', '긍정리뷰'],
        '성과(%)': [float(sales_row['value'])*100, float(target_row['value'])*100, float(keyword_row['value'])*100, float(review_row['value'])*100]
    })
    fig = px.bar(chart_data, x='지표', y='성과(%)', color='지표', 
                 color_discrete_sequence=['#c62828', '#1e3a8a', '#fbbf24', '#2dd4bf'])
    fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
