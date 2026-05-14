import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# 1. 페이지 설정
st.set_page_config(
    page_title="KGC Insight - 실시간 퍼포먼스",
    page_icon="🍎",
    layout="wide"
)

# 2. 구글 스프레드시트 연결 및 데이터 로드
# 제공해주신 ID를 기반으로 전체 URL 생성
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1BJIfd1sb12RSWmCt3vyQM-w0PgB-lERe_-ntYAyCFiA/edit#gid=0"

def load_data():
    try:
        # GSheetsConnection을 사용하여 데이터 읽기
        conn = st.connection("gsheets", type=GSheetsConnection)
        # 직접 URL을 전달하여 설정 미비로 인한 오류 방지
        df = conn.read(spreadsheet=SPREADSHEET_URL, ttl="1m")
        
        # 데이터 클리닝: 컬럼명 및 라벨 데이터의 앞뒤 공백 제거
        df.columns = df.columns.str.strip()
        if 'label' in df.columns:
            df['label'] = df['label'].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return None

df = load_data()

# 3. 데이터 추출 및 가공
def get_metric_data(label_name):
    if df is not None and not df.empty and 'label' in df.columns:
        try:
            row = df[df['label'] == label_name].iloc[0]
            return {
                'value': row.get('value', 0),
                'delta': row.get('delta', '0%')
            }
        except (IndexError, KeyError):
            pass
    return {'value': 0, 'delta': 'N/A'}

# 지표별 데이터 할당
sales_data = get_metric_data('수도권 판매량')
target_data = get_metric_data('핵심 타겟층(2030)')
keyword_data = get_metric_data('스포츠 키워드 언급')
review_data = get_metric_data('긍정 리뷰 비율')

# 요약 텍스트 (6행 1열 예상)
summary_text = "데이터를 불러올 수 없습니다."
if df is not None and len(df) >= 6:
    summary_text = df.iloc[5, 0]

# 4. UI 스타일링 (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    /* 메트릭 카드 스타일 */
    div[data-testid="metric-container"] {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 6px solid #c62828;
    }
    /* 텍스트 폰트 조정 */
    [data-testid="stMetricLabel"] { font-size: 1.1rem !important; font-weight: 600 !important; }
    </style>
    """, unsafe_allow_html=True)

# 5. 대시보드 상단 헤더
st.title("🍎 에브리타임 밸런스 실시간 퍼포먼스")
st.caption(f"연동 시트 ID: {SPREADSHEET_URL.split('/')[-2]}")

# 6. 주요 지표 (Metrics)
def format_percent(val):
    try:
        # 0.85 같은 소수를 85.0% 형태로 변환
        v = float(val)
        if v <= 1.0 and v > 0:
            return f"{v * 100:.1f}%"
        return f"{v:.1f}%"
    except:
        return str(val)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("수도권 판매 성장", format_percent(sales_data['value']), sales_data['delta'])
with m2:
    st.metric("2030 타겟 비중", format_percent(target_data['value']), target_data['delta'])
with m3:
    st.metric("스포츠 키워드 언급", format_percent(keyword_data['value']), keyword_data['delta'])
with m4:
    st.metric("긍정 리뷰 비율", format_percent(review_data['value']), review_data['delta'])

st.write("") # 간격 조절
st.markdown("---")

# 7. 상세 분석 섹션
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("💡 주간 마케팅 인사이트")
    st.info(f"**실시간 데이터 요약:**\n\n{summary_text}")
    
    with st.expander("📌 향후 전략 제언", expanded=True):
        st.write("""
        - **스포츠 마케팅 강화:** 키워드 언급 증가세에 맞춰 테니스/러닝 크루 협업 확대
        - **리뷰 관리:** 긍정 리뷰 유지를 위한 패키징 개선 피드백 반영
        - **타겟 확장:** 2030 외 타겟군 확장 가능성 검토
        """)

with col_right:
    st.subheader("📊 지표별 달성률 비교")
    try:
        # 차트 데이터 구성
        labels = ['수도권', '2030비중', '키워드', '긍정리뷰']
        values = []
        for d in [sales_data, target_data, keyword_data, review_data]:
            try:
                v = float(d['value'])
                values.append(v * 100 if v <= 1.0 else v)
            except:
                values.append(0)
        
        chart_df = pd.DataFrame({'지표': labels, '달성도(%)': values})
        
        fig = px.bar(
            chart_df, 
            x='지표', 
            y='달성도(%)', 
            color='지표',
            text='달성도(%)',
            color_discrete_sequence=['#c62828', '#1e3a8a', '#fbbf24', '#2dd4bf']
        )
        
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis_range=[0, 110],
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20),
            height=380
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"시각화 데이터를 준비 중입니다... ({e})")
