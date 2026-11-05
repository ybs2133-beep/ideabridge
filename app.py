import streamlit as st
import google.generativeai as genai
import os

# 1. 검색엔진 최적화(SEO) 및 브라우저 탭 설정 (구글 및 네이버 메타 태그 포함)
st.set_page_config(
    page_title="아이디어스토어 (IdeaStore) - AI 아이디어 가치평가 및 블라인드 거래",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <head>
        <meta name="description" content="내 머릿속 숨은 아이디어, 도용 걱정 없이 안전하게 AI로 평가받고 거래하세요. 예비창업자 AI 사업성 진단 및 블라인드 티저 매칭 플랫폼">
        <meta name="keywords" content="아이디어스토어, 사업성 진단, AI 아이디어 평가, 특허 출원, 예비창업자, 정책자금, 블라인드 투자, 아이디어팔기, 아이디어 거래,생각 팔기">
        <meta name="naver-site-verification" content="39cab1b3d8f39de1c7508ff12075979363c71f58"/>
    </head>
""", unsafe_allow_html=True)

# 2. 사이드바 - 관리자 모드 및 안내
st.sidebar.markdown("### 💡 아이디어스토어 안내")
st.sidebar.markdown("""
1. 입력하신 원본 아이디어는 외부에 절대 공개되지 않습니다.
2. 장터에는 AI가 요약한 '도용 방지 블라인드 티저'만 등록됩니다.
3. 상세 기획서 열람은 비밀유지서약(NDA) 동의 후 진행됩니다.
""")

st.sidebar.markdown("---")
with st.sidebar.expander("🔒 운영자 전용 메뉴"):
    admin_password = st.text_input("관리자 비밀번호", type="password")
    if admin_password == "1234": # 편의상 설정한 예시 비밀번호
        st.success("관리자 모드 활성화됨")

# 3. 메인 타이틀 및 탭 구성
st.title("💡 아이디어스토어 (IdeaStore)")
st.markdown("**내 머릿속 숨은 아이디어, 도용 걱정 없이 안전하게 평가받고 거래하세요.**")

tab1, tab2 = st.tabs(["📊 1단계: 아이디어 가치 진단", "🛒 2단계: 프리미엄 아이디어 장터"])

with tab1:
    st.subheader("🤖 아이디어 입력 (비공개 보안 분석)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        category = st.selectbox(
            "아이디어 분야",
            ["IT / 웹·앱 서비스", "커머스 / 유통", "소상공인 / 오프라인", "바이오 / 헬스케어", "콘텐츠 / 미디어", "기타"]
        )
        idea_text = st.text_area("어떤 아이디어인가요? (구체적일수록 정확합니다)", placeholder="예: 같은 지역 안에있는 농작물 하루2번 직배송 서비스", height=150)
        
        need_type = st.radio(
            "현재 가장 필요한 연결은?",
            ["아이디어 원본 판매(양도)", "시드 투자금 유치", "기술/마케팅 공동창업자 매칭", "정부지원사업/재도전 창업자금 확보"]
        )
        
        target_price = st.text_input("희망 투자금 또는 판매 희망가", placeholder="예: 1000만원 또는 지분 10%")
        
        analyze_btn = st.button("🚀 AI 사업성 정밀 진단 및 블라인드 티저 생성", type="primary")

    with col2:
        st.subheader("📈 AI 진단 결과 및 수익화 패키지")
        
        if analyze_btn:
            if not idea_text:
                st.warning("아이디어 내용을 입력해 주세요!")
            else:
                with st.spinner("AI가 사업성, 시장성, 도용 방지 티저를 분석 중입니다..."):
                    st.markdown("### AI 종합 사업성 점수")
                    st.markdown("# **82점 / 100점**")
                    st.caption("📈 상위 유망 아이템")
                    
                    st.markdown("---")
                    st.markdown("#### 🔒 투자자·매수자 공개용 블라인드 티저 (도용 방지 적용됨)")
                    st.info("**제목:** 유통 단계를 파괴하는 하이퍼로컬 초신선 식자재 고빈도 순환 물류 시스템")
                    st.markdown("""
                    * **핵심 강점:** 산지와 소비자를 직접 연결하여 기존 D2C의 한계인 배송 지연을 극복하고, 극강의 신선도와 고빈도 재구매를 유도하는 로컬 최적화 비즈니스 모델입니다.
                    * **돌파 전략:** 초기 물류 밀집도 부족에 따른 물류비 상승 위험이 있으나, 거점별 예약 구매 기반의 루트 최적화 시스템과 지역 커뮤니티 연계 구독 모델을 통해 고정비를 조기 상쇄할 수 있습니다.
                    """)
                    
                    st.markdown("---")
                    st.markdown("### 🤝 전문가 심층 상담 및 제휴 연결")
                    st.markdown("본 아이디어를 바탕으로 **특허 출원(변리사)** 또는 **정부지원금/정책자금 컨설팅**을 무료로 연계해 드립니다.")
                    
                    st.link_button("📝 [무료] 예비창업자 심층 상담 신청하기 (구글 설문지)", "https://forms.gle/여기에본인설문지주소넣기")

with tab2:
    st.subheader("🛒 프리미엄 아이디어 장터 (블라인드 티저 목록)")
    st.markdown("도용 위험 없이 검증된 유망 아이디어의 티저를 둘러보고, 상세 상담을 신청해 보세요.")
    
    with st.container(border=True):
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.markdown("#### [IT/플랫폼] 1인 가구 소형 이삿짐 공유 및 빈차 매칭 플랫폼")
            st.caption("AI 사업성 평가 점수: 88점 | 희망 제휴: 시드 투자 유치")
            st.write("공차 거리(빈 트럭)를 활용하여 1인 가구 이사 비용을 50% 이상 절감하는 지역 기반 매칭 솔루션의 블라인드 티저입니다.")
        with col_b:
            st.markdown("<br>", unsafe_allow_html=True)
            st.link_button("📋 상세 열람 및 NDA 신청", "https://forms.gle/여기에본인설문지주소넣기")

    with st.container(border=True):
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.markdown("#### [커머스] AI 기반 무인 밀키트 매장 자동 발주 및 폐기 최소화 솔루션")
            st.caption("AI 사업성 평가 점수: 85점 | 희망 제휴: 아이디어 원본 판매(양도)")
            st.write("날씨, 요일, 주변 유동 인구를 분석하여 무인 점포의 재고를 실시간 제어하고 폐기율을 제로에 가깝게 낮추는 자동화 프로그램입니다.")
        with col_b:
            st.markdown("<br>", unsafe_allow_html=True)
            st.link_button("📋 상세 열람 및 NDA 신청", "https://forms.gle/여기에본인설문지주소넣기")
