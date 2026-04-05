import streamlit as st

# 1. 웹 앱 제목 및 설명
st.title("📊 상한가 헌터 헤리의 버핏식 내재 가치 계산기")
st.write("기업의 핵심 재무 데이터를 입력하고 '구하기' 버튼을 누르면, 딥러닝 봇이 사용하는 DCF 모델 기반의 적정 주가를 계산해 드립니다!")

# 2. 구독자 입력 칸 만들기 (기본값 세팅)
current_fcf = st.number_input("1. 현재 잉여현금흐름 (FCF, 단위: 억원)", value=50000)
shares = st.number_input("2. 총 발행 주식 수 (주)", value=6000000)
discount_rate_input = st.number_input("3. 할인율 (%) (예: 8.5%면 8.5 입력)", value=8.5)
growth_rate_input = st.number_input("4. 향후 5년 예상 연평균 성장률 (%) (예: 12%면 12 입력)", value=12.0)

# 백분율을 소수로 변환
r = discount_rate_input / 100
g = growth_rate_input / 100
g_terminal = 0.02  # 영구 성장률은 2%로 고정

# 3. '구하기' 버튼 및 계산 로직
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
    st.success(f"💡 계산된 1주당 적정 주가는 **{int(price_per_share):,}원** 입니다!")
    st.info("현재 시장 주가가 이 계산된 가격보다 낮다면, 훌륭한 '안전마진'이 확보된 것입니다.")