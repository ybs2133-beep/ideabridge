import streamlit as st
from google import genai
import json
import csv
import os
import re
from datetime import datetime

# 페이지 기본 설정 (아이디어스토어 적용)
st.set_page_config(
    page_title="아이디어스토어 | AI 아이디어 가치평가 & 거래소",
    page_icon="💡",
    layout="wide"
)

DB_FILE = "leads_db.csv"
ADMIN_PASSWORD = "Dudqls2133!"

# 구글 설문지 링크 설정
CONSULT_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSecUCny88Jm1_CQygUxOoRelxKN3313oSw6zDgGM3p3-OWHqw/viewform?usp=publish-editor"

# 고객 DB(연락처)를 엑셀(CSV) 파일에 자동 저장하는 함수
def save_lead(lead_type, name, phone, target_info, memo=""):
    file_exists = os.path.isfile(DB_FILE)
    with open(DB_FILE, mode="a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["신청일시", "수익구분(DB유형)", "신청자명", "연락처", "대상아이디어/분야", "추가요청사항"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            lead_type,
            name,
            phone,
            target_info,
            memo
        ])

# 사용 가능한 최신 Gemini 모델을 자동으로 찾아 실행하는 함수
def analyze_idea_with_ai(api_key, prompt):
    client = genai.Client(api_key=api_key)
    candidate_models = [
        "gemini-3-flash-preview",
        "gemini-3.1-flash-lite-preview",
        "gemini-2.5-flash-lite",
        "gemini-3-pro-preview",
        "gemini-2.0-flash"
    ]
    try:
        for m in client.models.list():
            m_name = getattr(m, "name", "")
            clean_name = m_name.replace("models/", "")
            if "gemini" in clean_name.lower() and not any(x in clean_name.lower() for x in ["embedding", "imagen", "veo", "tts", "audio", "aqa", "robotics", "computer-use"]):
                if clean_name not in candidate_models:
                    candidate_models.append(clean_name)
    except Exception:
        pass

    last_error = None
    for model_name in candidate_models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            text = response.text.strip()
            text = re.sub(r"^```json\s*|\s*```$", "", text, flags=re.MULTILINE).strip()
            data = json.loads(text)
            data["_used_model"] = model_name
            return data
        except Exception as e:
            last_error = e
            continue
    raise last_error

# 세션 상태 초기화
if "idea_list" not in st.session_state:
    st.session_state.idea_list = [
        {
            "id": 101,
            "category": "기타 아이디어",
            "teaser_title": "원룸·소형 욕실 특화 무타공 직배수 & UV 살균 초미니 세탁 가전",
            "score": 89,
            "target_invest": "1,000만 원 (아이디어 원본 판매/양도)",
            "expected_roi": "크라우드펀딩(와디즈) 런칭 시 1차 펀딩 5,000만 원 및 생활가전 브랜드 기술 로열티 수익 기대",
            "date": "2026-11-04"
        },
        {
            "id": 102,
            "category": "자동차 / 모빌리티",
            "teaser_title": "장기렌트·리스 만기 차량 직거래 승계 및 잔존가치 차익 계산 플랫폼",
            "score": 88,
            "target_invest": "3,000만 원 (초기 마케팅 및 앱 고도화)",
            "expected_roi": "건당 중개 수수료 30만 원 + 금융 제휴 수수료",
            "date": "2026-11-04"
        }
    ]

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# 배포 서버에 숨겨둔 API 키 자동 불러오기
api_key = ""
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    pass

# 사이드바: 일반 방문자 안내 및 암호 잠금 처리된 운영자 메뉴
with st.sidebar:
    st.subheader("💡 아이디어스토어 안내")
    st.caption("1. 입력하신 원본 아이디어는 외부에 절대 공개되지 않습니다.\n2. 장터에는 AI가 요약한 '도용 방지 블라인드 티저'만 등록됩니다.\n3. 상세 기획서 열람은 비밀유지서약(NDA) 동의 후 진행됩니다.")
    st.divider()
    with st.expander("🔐 운영자 전용 메뉴"):
        admin_pw = st.text_input("관리자 비밀번호", type="password", placeholder="비밀번호를 입력하세요")
        if admin_pw == ADMIN_PASSWORD:
            st.success("✅ 관리자 인증 완료")
            if not api_key:
                api_key = st.text_input("임시 API Key 입력 (로컬 테스트용)", type="password")
            if os.path.isfile(DB_FILE):
                with open(DB_FILE, "rb") as f:
                    st.download_button(
                        label="📊 수집된 고객 DB 엑셀(CSV) 다운로드",
                        data=f,
                        file_name=f"ideastore_leads_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            else:
                st.caption("아직 수집된 고객 DB가 없습니다.")
        elif admin_pw:
            st.error("❌ 비밀번호가 일치하지 않습니다.")

st.title("💡 아이디어스토어 (IdeaStore)")
st.markdown("##### 내 머릿속 숨은 아이디어, 도용 걱정 없이 **안전하게 평가받고 거래**하세요.")

tab1, tab2 = st.tabs(["🚀 1단계: 아이디어 가치 진단", "🤝 2단계: 프리미엄 아이디어 장터"])

# ---------------------------------------------------------
# 탭 1: AI 아이디어 평가 + 블라인드 티저 생성 + 구글 설문지 연결
# ---------------------------------------------------------
with tab1:
    col_input, col_result = st.columns([1, 1.2], gap="large")

    with col_input:
        st.subheader("📝 아이디어 입력 (비공개 보안 분석)")
        category = st.selectbox("아이디어 분야", ["기타 아이디어", "IT / 웹·앱 서비스", "자동차 / 모빌리티", "커머스 / 유통", "콘텐츠 / 미디어", "소상공인 / 오프라인"])
        raw_idea = st.text_area(
            "어떤 아이디어인가요? (구체적일수록 정확합니다)",
            height=150,
            placeholder="예: 좁은 욕실 벽이나 유리에 부착해 사용하는 직배수 방식의 초미니 샤워타올 UV 살균 세탁기..."
        )
        need_type = st.radio("현재 가장 필요한 연결은?", ["아이디어 원본 판매(양도)", "시드 투자금 유치", "기술/마케팅 공동창업자 매칭", "정부지원사업/재도전 창업자금 확보"])
        target_amount = st.text_input("희망 투자금 또는 판매 희망가", placeholder="예: 1,000만 원 / 지분 협의")

        analyze_btn = st.button("🔍 AI 가치 평가 및 거래용 블라인드 카드 생성", type="primary", use_container_width=True)

    with col_result:
        st.subheader("📊 AI 진단 결과 및 수익화 패키지")

        if analyze_btn:
            if not raw_idea:
                st.warning("아이디어 내용을 입력해 주세요!")
            elif not api_key:
                st.warning("좌측 사이드바 '운영자 전용 메뉴'에서 비밀번호 인증 후 API Key를 입력해 주세요.")
            else:
                with st.spinner("AI 심사역이 시장성 분석 및 도용 방지 블라인드 카드를 생성 중입니다..."):
                    prompt = f"""
                    당신은 냉철한 벤처캐피탈(VC) 심사역이자 특허·제품화 전문가입니다.
                    제안자의 아이디어를 분석하되, 투자자나 매수자에게 공개할 때는 아이디어가 도용되지 않도록 '핵심 구조는 가리고 시장성과 매력도만 강조한 블라인드 티저 제목'을 만들어야 해요.
                    
                    [입력 정보]
                    - 분야: {category}
                    - 원본 아이디어: {raw_idea}
                    - 희망 연결: {need_type} ({target_amount})

                    반드시 아래 JSON 형식으로만 한국어로 응답하세요:
                    {{
                        "score": 85,
                        "teaser_title": "핵심 영업비밀은 숨기고 매수자/투자자의 호기심을 자극하는 한 줄 블라인드 헤드라인",
                        "strength": "이 아이디어가 실제 시장에서 팔리는 결정적 이유 1~2문장",
                        "risk_and_solution": "예상되는 현실적 장벽(금형비, 인증 등)과 이를 돌파할 실전 전략(크라우드펀딩 선주문, 특허 선점 등) 1~2문장",
                        "expected_roi": "매수자/투자자 관점의 예상 수익 모델 및 회수 시나리오",
                        "gov_grant_fit": "추천하는 정부지원사업(예: 지식재산 바우처, 시제품 제작 지원사업 등)"
                    }}
                    """
                    try:
                        res_data = analyze_idea_with_ai(api_key, prompt)
                        res_data["category"] = category
                        res_data["target_invest"] = f"{target_amount or '협의 가능'} ({need_type})"
                        st.session_state.last_result = res_data
                    except Exception as e:
                        st.error(f"분석 중 오류가 발생했습니다: {e}")

        if st.session_state.last_result:
            res = st.session_state.last_result
            st.metric(label="AI 종합 사업성 점수", value=f"{res['score']}점 / 100점", delta="상위 유망 아이템")

            with st.container(border=True):
                st.markdown("#### 🔒 투자자·매수자 공개용 블라인드 티저 (도용 방지 적용됨)")
                st.markdown(f"**제목:** {res['teaser_title']}")
                st.write(f"- **핵심 강점:** {res['strength']}")
                st.write(f"- **돌파 전략:** {res['risk_and_solution']}")
                st.write(f"- **수익 시나리오:** {res['expected_roi']}")
                st.write(f"- **추천 지원금:** {res['gov_grant_fit']}")

                if st.button("📢 이 블라인드 카드를 '프리미엄 아이디어 장터'에 정식 등록하기", use_container_width=True):
                    st.session_state.idea_list.insert(0, {
                        "id": len(st.session_state.idea_list) + 101,
                        "category": res["category"],
                        "teaser_title": res["teaser_title"],
                        "score": res["score"],
                        "target_invest": res["target_invest"],
                        "expected_roi": res["expected_roi"],
                        "date": datetime.now().strftime("%Y-%m-%d")
                    })
                    st.success("✅ 2단계 '프리미엄 아이디어 장터' 탭에 등록되었습니다!")

            # 💰 핵심 수익 모델: 구글 설문지 바로가기 버튼 연결
            st.markdown("---")
            st.markdown("##### 🎁 내 아이디어 권리 보호 및 지원금·매수자 즉시 연결")
            st.info("특허 출원 상담 및 정부지원금 매칭을 원하시면 아래 설문지 작성 버튼을 눌러주세요!")
            st.link_button(
                "📝 구글 설문지로 심층 상담 신청하기", 
                CONSULT_FORM_URL,
                use_container_width=True
            )

# ---------------------------------------------------------
# 탭 2: 블라인드 투자 매칭 라운지 (아이디어 거래소)
# ---------------------------------------------------------
with tab2:
    st.subheader("🤝 프리미엄 아이디어 장터")
    st.caption("모든 아이디어는 핵심 노하우가 가려진 상태로 공개됩니다. 상세 기획서 열람 및 제안자 연락은 '비밀유지서약(NDA) 동의 및 열람 신청' 후 진행됩니다.")

    for item in st.session_state.idea_list:
        with st.container(border=True):
            c1, c2 = st.columns([3.5, 1])
            with c1:
                st.markdown(f"`{item['category']}` · 등록일 {item['date']}")
                st.markdown(f"#### {item['teaser_title']}")
                st.write(f"**예상 수익구조:** {item['expected_roi']}")
                st.write(f"**희망 조건:** {item['target_invest']}")
            with c2:
                st.metric("AI 검증 점수", f"{item['score']}점")
            
            with st.expander(f"🔓 [{item['id']}번 아이디어] 상세 기획서 열람 & 제안자 미팅 신청하기"):
                st.write("상세 기획서 열람 및 미팅을 위해 아래 설문지를 작성해 주세요.")
                st.link_button(
                    "📝 투자자/매수자 열람 및 미팅 신청 설문지 작성",
                    CONSULT_FORM_URL,
                    use_container_width=True
                )
