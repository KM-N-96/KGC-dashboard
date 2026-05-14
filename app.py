import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="KGC Insight - 에브리타임 밸런스 성과",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 대시보드의 세련된 룩앤필을 위해 CSS를 주입합니다.
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Noto+Sans+KR:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', 'Noto Sans KR', sans-serif;
    }
    
    .main {
        background-color: #f1f5f9;
    }
    
    /* 카드 스타일 */
    .stMetric {
        background: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #c62828;
    }
    
    /* 텍스트 색상 및 스타일 */
    .kgc-red { color: #c62828; }
    
    /* 전략 제언 박스 */
    .strategy-box {
        background: linear-gradient(135deg, #c62828 0%, #8e1b1b 100%);
        color: white;
        padding: 30px;
        border-radius: 25px;
        margin-top: 20px;
    }
    
    /* 인사이트 박스 */
    .insight-card {
        background: white;
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<div style='display:flex; align-items:center; gap:10px; margin-bottom:30px;'><div style='background:#c62828; color:white; padding:5px 12px; border-radius:8px; font-weight:bold;'>K</div><h2 style='margin:0;'>KGC Insight</h2></div>", unsafe_allow_html=True)
    
    st.write("### 🧭 Navigation")
    st.button("📊 Dashboard", use_container_width=True, type="primary")
    st.button("🛒 Sales Analysis", use_container_width=True)
    st.button("👥 Consumer VOC", use_container_width=True)
    st.button("🚀 Strategy", use_container_width=True)
    
    st.divider()
    st.caption("Last updated: 2026.03.27")
    st.info("BM 보고용 실시간 데이터 연동 중")

col_header_left, col_header_right = st.columns([3, 1])

with col_header_left:
    st.title("에브리타임 밸런스 리뉴얼 성과")
    st.write("2026년 3월 4주차 위클리 퍼포먼스 리포트")

with col_header_right:
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("📄 Export PDF Report", use_container_width=True)

st.markdown("### 📈 핵심 성과 지표 (KPI)")
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(label="전체 판매 성장률", value="+13.0%", delta="2.5% vs 전주")
with m2:
    st.metric(label="수도권 편의점 점유", value="15%", delta="강세 유지", delta_color="normal")
with m3:
    st.metric(label="2030 타겟 비중", value="45%", delta="핵심 동력")
with m4:
    st.metric(label="활동 키워드 언급", value="+30%", delta="라이프스타일 확장")

st.markdown("<br>", unsafe_allow_html=True)

col_chart1, col_chart2 = st.columns([2, 1])

with col_chart1:
    st.markdown("#### 📍 채널별 지역 판매 동향")
    
    # 지역별 판매 데이터 프레임 생성
    df_sales = pd.DataFrame({
        '지역': ['수도권 (CVS/몰)', '지방권 (대형마트/로드샵)'],
        '증감률': [15, -2]
    })
    
    fig_sales = px.bar(
        df_sales, 
        x='지역', 
        y='증감률',
        color='지역',
        color_discrete_map={'수도권 (CVS/몰)': '#c62828', '지방권 (대형마트/로드샵)': '#cbd5e1'},
        text_auto='.1f'
    )
    fig_sales.update_layout(
        showlegend=False, 
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title="증감률 (%)",
        xaxis_title=None,
        height=350
    )
    st.plotly_chart(fig_sales, use_container_width=True)

with col_chart2:
    st.markdown("#### 👥 구매 연령층 분포")
    
    df_age = pd.DataFrame({
        '연령': ['2030 사회초년생', '4050 부모세대', '60대 이상/기타'],
        '비중': [45, 35, 20]
    })
    
    fig_age = px.pie(
        df_age, 
        values='비중', 
        names='연령',
        hole=0.6,
        color_discrete_sequence=['#c62828', '#475569', '#cbd5e1']
    )
    fig_age.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(t=10, b=10, l=10, r=10),
        height=350
    )
    st.plotly_chart(fig_age, use_container_width=True)

col_voc, col_key = st.columns(2)

with col_voc:
    st.markdown("#### 💬 Consumer Insights (VOC)")
    st.markdown("""
        <div class='insight-card' style='border-left: 5px solid #10b981;'>
            <div style='display:flex; justify-content:space-between;'>
                <strong style='color:#065f46;'>Positive Sentiment</strong>
                <span style='color:#059669; font-size:0.8em;'>82% Positive</span>
            </div>
            <p style='font-size:0.9em; margin-top:5px; color:#334155;'><i>"선물하기 너무 예뻐요", "쓴맛이 덜해서 운동 중에 먹기 편함"</i></p>
        </div>
        <div class='insight-card' style='border-left: 5px solid #ef4444;'>
            <div style='display:flex; justify-content:space-between;'>
                <strong style='color:#991b1b;'>Pain Points</strong>
                <span style='color:#dc2626; font-size:0.8em;'>Action Required</span>
            </div>
            <p style='font-size:0.9em; margin-top:5px; color:#334155;'><i>"가격 인상 체감돼요", "박스 개봉 시 지기 구조 뻑뻑함 개선 필요"</i></p>
        </div>
    """, unsafe_allow_html=True)

with col_key:
    st.markdown("#### 🏃‍♂️ Lifestyle Keyword Trend")
    
    df_key = pd.DataFrame({
        '키워드': ['등산', '테니스', '헬스/오운완', '직장인선물'],
        '언급량': [35, 30, 25, 10]
    })
    
    fig_key = px.bar(
        df_key, 
        x='언급량', 
        y='키워드', 
        orientation='h',
        color_discrete_sequence=['#f59e0b']
    )
    fig_key.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_showticklabels=False,
        xaxis_title=None,
        yaxis_title=None,
        height=250,
        margin=dict(t=0, b=0)
    )
    st.plotly_chart(fig_key, use_container_width=True)

st.markdown(f"""
    <div class='strategy-box'>
        <h3>💡 Team Leader's Strategy 제언</h3>
        <p style='opacity: 0.9; margin-bottom: 20px;'>데이터 분석 결과에 기반한 금주 핵심 액션 플랜입니다.</p>
        <ul style='list-style: none; padding-left: 0;'>
            <li style='margin-bottom: 10px;'>✅ <b>'오운완' 챌린지 및 아웃도어 스포츠 샘플링 집중:</b> 테니스장/등산로 거점 마케팅 강화</li>
            <li style='margin-bottom: 10px;'>✅ <b>패키징 UX 품질 보완:</b> 생산 부서와 박스 지기 구조 공차 수정 협의 착수</li>
            <li style='margin-bottom: 10px;'>✅ <b>지방권 활성화 프로모션:</b> 대형마트 전용 리뉴얼 기획 패키지 VMD 강화</li>
        </ul>
        <br>
        <button style='background: white; color: #c62828; border: none; padding: 10px 20px; border-radius: 12px; font-weight: bold; cursor: pointer;'>
            View Full Action Plan →
        </button>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: #94a3b8; font-size: 0.8em;'>© 2026 KGC Brand Strategy Team | Internal Use Only</p>", unsafe_allow_html=True)
