import streamlit as st

# 1. 웹 앱 제목 및 설명
st.title("📊 상한가 헌터 헤리의 버핏식 내재 가치 계산기")
st.write("기업의 핵심 재무 데이터를 입력하고 '구하기' 버튼을 누르면, 딥러닝 봇이 사용하는 DCF 모델 기반의 적정 주가를 계산해 드립니다!")

# 2. 초보자를 위한 데이터 찾는 법 (도움말 창)
with st.expander("❓ 각 항목의 데이터는 어디서 찾나요? (클릭해서 펼쳐보기)"):
    st.markdown("""
    * **현재 잉여현금흐름(FCF):** [네이버 증권] > 종목검색 > 종목분석 > 기업재무분석 표 맨 아래 'FCF' 수치 입력 (미국주는 [야후 파이낸스] > Financials > Cash Flow > 'Free Cash Flow' 입력)
    * **총 발행 주식 수:** [네이버 증권] 종목 메인 화면 우측 '상장주식수' 전체 숫자 입력 (미국주는 [야후 파이낸스] > Statistics > 'Shares Outstanding' 확인)
    * **할인율(%):** 워렌 버핏의 기회비용입니다. 잘 모르겠다면 무난한 우량주는 **8.5%**, 미래가 다소 불확실한 위험 주식은 **10%**를 입력하세요.
   * **예상 성장률(%):** [네이버 증권] '컨센서스' 탭의 증권사 추정치 참고. (보통 안정적인 성숙기업 3-5%, 우량 기술주 10-15%, 초고속 성장주 20% 이상)
# 3. 구독자 입력 칸 만들기 (기본값 세팅)
current_fcf = st.number_input("1. 현재 잉여현금흐름 (FCF, 단위: 억원 또는 달러)", value=50000)
shares = st.number_input("2. 총 발행 주식 수 (주)", value=6000000)
discount_rate_input = st.number_input("3. 할인율 (%) (예: 8.5%면 8.5 입력)", value=8.5)
growth_rate_input = st.number_input("4. 향후 5년 예상 연평균 성장률 (%) (예: 12%면 12 입력)", value=12.0)

# 백분율을 소수로 변환
r = discount_rate_input / 100
g = growth_rate_input / 100
g_terminal = 0.02  # 영구 성장률은 물가상승률 수준인 2%로 아주 보수적으로 고정

# 4. '구하기' 버튼 및 계산 로직
if st.button("적정 주가 구하기"):
    fcf = current_fcf
    pv_of_fcf = 0
    
    # 5년간의 현금흐름 할인
    for t in range(1, 6):
        fcf = fcf * (1 + g)
        pv_of_fcf += fcf / ((1 + r) ** t)
        
    # 영구 가치 계산 및 할인
    terminal_value = (fcf * (1 + g_terminal)) / (r - g_terminal)
    pv_of_tv = terminal_value / ((1 + r) ** 5)
    
    # 최종 적정 주가 도출
    total_value = pv_of_fcf + pv_of_tv
    price_per_share = total_value / shares
    
    # 결과 화면 출력
    st.success(f"💡 계산된 1주당 적정 주가는 **{int(price_per_share):,} (원/달러)** 입니다!")
    st.info("현재 시장 주가가 이 계산된 가격보다 낮다면, 워렌 버핏이 말하는 훌륭한 '안전마진'이 확보된 상태입니다.")
