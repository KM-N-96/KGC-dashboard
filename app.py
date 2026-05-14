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
    # pandas는 0번부터 시작하므로 6번 인덱스가 7행임
    summary_text = df.iloc[5, 0] if len(df) > 5 else "데이터를 분석 중입니다."

except Exception as e:
    st.error(f"시트 데이터를 읽는 중 오류가 발생했습니다: {e}")
    # 오류 발생 시 기본값 설정
    summary_text = "데이터 연결 상태를 확인해주세요."

# --- UI 렌더링 시작 ---
st.title("에브리타임 밸런스 리뉴얼 성과 (실시간)")
st.caption("구글 스프레드시트 데이터 실시간 동기화 중")

# 상단 KPI 섹션
m1, m2, m3, m4 = st.columns(4)

with m1:
    # 0.95 -> 95% 형태로 표시 (필요 시 조정 가능)
    val = f"{float(sales_row['value']) * 100:.0f}%" if isinstance(sales_row['value'], (int, float)) else sales_row['value']
    st.metric(label="수도권 판매량", value=val, delta=sales_row['delta'])

with m2:
    st.metric(label="2030 타겟 비중", value=target_row['value'], delta=target_row['delta'])

with m3:
    # 0.3 -> +30% 형태로 변환 시각화
    k_val = f"+{float(keyword_row['value']) * 100:.0f}%" if isinstance(keyword_row['value'], (int, float)) else keyword_row['value']
    st.metric(label="스포츠 키워드 언급", value=k_val, delta=keyword_row['delta'])

with m4:
    st.metric(label="긍정 리뷰 비율", value=review_row['value'], delta=review_row['delta'])

# 시트 7행의 요약 텍스트를 강조해서 표시
st.markdown("---")
st.subheader("💡 금주 핵심 인사이트 (시트 자동 연동)")
st.info(summary_text)

import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# 페이지 설정 (기존과 동일)
st.set_page_config(page_title="KGC Insight - 실시간 연동", layout="wide")

# 1. 구글 스프레드시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. 데이터 불러오기 (데이터가 있는 시트 이름 입력)
# 'sales_data' 시트에서 데이터를 읽어온다고 가정
try:
    df = conn.read(worksheet="sales_data", ttl="5m") # 5분마다 캐시 갱신
    
    # 예시: 시트의 특정 셀 값을 변수에 할당
    # 시트 구조: [지표, 값] 형태라고 가정
    total_growth = df[df['지표'] == '전체 성장률']['값'].values[0]
    metropolitan_sales = df[df['지표'] == '수도권 성장률']['값'].values[0]
    target_30s = df[df['지표'] == '2030 비중']['값'].values[0]
except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다. 시트 연결을 확인하세요.")
    total_growth, metropolitan_sales, target_30s = 0, 0, 0

# --- 이하 기존 대시보드 UI 코드 (변수만 연동) ---

st.title("에브리타임 밸런스 리뉴얼 성과 (실시간)")

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="전체 판매 성장률", value=f"+{total_growth}%")
with m2:
    st.metric(label="수도권 편의점 점유", value=f"{metropolitan_sales}%")
with m3:
    st.metric(label="2030 타겟 비중", value=f"{target_30s}%")

# 차트 데이터도 df를 활용해 px.bar(df, ...) 형태로 구현 가능합니다.
st.success("✅ 구글 스프레드시트와 실시간 연동 중입니다.")
