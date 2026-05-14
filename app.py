import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="KGC Insight - Premium Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Pretendard', sans-serif;
        background-color: #0f1116;
        color: #ffffff;
    }

    .header-container {
        padding: 2rem 0rem;
        background: linear-gradient(90deg, #1e1e26 0%, #0f1116 100%);
        border-bottom: 2px solid #d32f2f;
        margin-bottom: 2rem;
        border-radius: 0 0 20px 20px;
        text-align: center;
    }

    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px !important;
        border-radius: 18px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(4px);
        transition: transform 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border: 1px solid #d32f2f;
    }

    [data-testid="stMetricLabel"] { color: #94a3b8 !important; font-weight: 500 !important; font-size: 1rem !important; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-weight: 800 !important; font-size: 2.2rem !important; }
    </style>
    """, unsafe_allow_html=True)

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1BJIfd1sb12RSWmCt3vyQM-w0PgB-lERe_-ntYAyCFiA/edit#gid=0"

@st.cache_data(ttl=60)
def load_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet=SPREADSHEET_URL, ttl="1m")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        return None

df = load_data()

def clean_value_for_chart(v):
    """문자열 형태의 데이터(95.0%, +40% 등)를 차트용 숫자로 변환합니다."""
    if isinstance(v, (int, float)):
        return float(v) * 100 if v <= 1.0 else float(v)
    try:
        # %, +, ,(콤마) 제거 후 숫자로 변환
        clean_v = str(v).replace('%', '').replace('+', '').replace(',', '').strip()
        return float(clean_v)
    except:
        return 0.0

def get_metric_data(label_name):
    if df is not None and not df.empty and 'label' in df.columns:
        try:
            row = df[df['label'].astype(str).str.strip() == label_name].iloc[0]
            return {'value': row.get('value', 0), 'delta': row.get('delta', '0%')}
        except: pass
    return {'value': 0, 'delta': 'N/A'}

# 데이터 로드
sales = get_metric_data('수도권 판매량')
target = get_metric_data('핵심 타겟층(2030)')
keyword = get_metric_data('스포츠 키워드 언급')
review = get_metric_data('긍정 리뷰 비율')
summary = df.iloc[5, 0] if df is not None and len(df) >= 6 else "데이터를 불러오는 중입니다..."

st.markdown(f"""
    <div class="header-container">
        <h1 style='margin:0; color:#ffffff; font-size: 2.5rem;'>KGC 🍎 에브리타임 밸런스</h1>
        <p style='color:#94a3b8; font-size: 1.1rem; margin-top:0.5rem;'>REAL-TIME PERFORMANCE MONITORING</p>
    </div>
    """, unsafe_allow_html=True)

def format_display_val(v, plus=False):
    """메트릭 표시용 포맷팅"""
    try:
        num = float(v)
        if num <= 1.0: return f"{'+' if plus else ''}{num*100:.1f}%"
        return f"{'+' if plus else ''}{num:.1f}%"
    except: return str(v)

m1, m2, m3, m4 = st.columns(4)
with m1: st.metric("수도권 성장률", format_display_val(sales['value']), sales['delta'])
with m2: st.metric("2030 타겟 비중", format_display_val(target['value']), target['delta'])
with m3: st.metric("스포츠 키워드", format_display_val(keyword['value'], True), keyword['delta'])
with m4: st.metric("긍정 리뷰", format_display_val(review['value']), review['delta'])

st.markdown("<br>", unsafe_allow_html=True)

col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown("### 📊 Key Performance Indicator (KPI)")
    try:
        # 데이터 정제 적용 (문자열 -> 숫자)
        vals = [
            clean_value_for_chart(sales['value']),
            clean_value_for_chart(target['value']),
            clean_value_for_chart(keyword['value']),
            clean_value_for_chart(review['value'])
        ]
        labels = ['Regional', 'Target 2030', 'Keywords', 'Positive Review']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=labels, y=vals,
            marker=dict(
                color=vals,
                colorscale=[[0, '#334155'], [0.5, '#d32f2f'], [1, '#ff5252']],
                line=dict(color='#ffffff', width=0.5)
            ),
            text=[f"{v:.1f}%" for v in vals],
            textposition='auto',
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8'),
            margin=dict(l=0, r=0, t=20, b=0),
            height=400,
            yaxis=dict(range=[0, 115], gridcolor='rgba(255,255,255,0.05)', title="성취도 (%)"),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)')
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"데이터 변환 오류: {e}")

with col_right:
    st.markdown("### 💡 Executive Insights")
    st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 15px; border-left: 5px solid #d32f2f;">
            <p style="color:#e2e8f0; font-size:1.1rem; line-height:1.6;">{summary}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🚀 전략적 실행 방안 (Action Plan)", expanded=True):
        st.markdown("""
        - **Premium Branding:** 고관여 스포츠(테니스/러닝) 중심 팝업 강화
        - **Quality Feedback:** 리뷰 데이터 기반 패키징 UX 개선 태스크포스(TF) 가동
        - **Growth Hacking:** 수도권 판매 성장세를 지방 거점 도시로 확산 전략 수립
        """)

st.markdown("---")
st.caption("Sync Status: 🟢 Connected to Google Sheets | Last Updated: Real-time")
