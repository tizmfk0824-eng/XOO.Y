import streamlit as st
from datetime import date, datetime
import requests
import json

# 페이지 설정
st.set_page_config(
    page_title="오늘의 사주",
    page_icon="🔮",
    layout="wide"
)

# 날씨 가져오기
def get_weather():
    try:
        # Open-Meteo 무료 API (한국 서울 기준)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 37.5665,
            "longitude": 126.9780,
            "current": ["temperature_2m", "weathercode", "precipitation"],
            "timezone": "Asia/Seoul"
        }
        res = requests.get(url, params=params, timeout=5)
        data = res.json()
        temp = data["current"]["temperature_2m"]
        code = data["current"]["weathercode"]
        return temp, code
    except:
        return None, None

def get_weather_theme(code, hour):
    # 시간대
    if 6 <= hour < 12:
        time_name = "아침"
    elif 12 <= hour < 18:
        time_name = "낮"
    elif 18 <= hour < 22:
        time_name = "저녁"
    else:
        time_name = "밤"

    # 날씨 코드 → 배경 그라디언트 + 이모지
    if code is None:
        return "#1a0533", "#4A0E8F", "🌙", time_name
    elif code == 0:  # 맑음
        if 6 <= hour < 18:
            return "#0a2a6e", "#1a6eb5", "☀️", time_name
        else:
            return "#0a0a2e", "#1a0533", "🌙", time_name
    elif code in [1, 2, 3]:  # 구름
        return "#2c3e50", "#4a5568", "⛅", time_name
    elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:  # 비
        return "#1a2a3a", "#2d4a6e", "🌧️", time_name
    elif code in [71, 73, 75, 77, 85, 86]:  # 눈
        return "#2a3a4a", "#4a6a8a", "❄️", time_name
    elif code in [95, 96, 99]:  # 천둥
        return "#1a1a2e", "#2d1b69", "⛈️", time_name
    else:
        return "#1a0533", "#4A0E8F", "🌤️", time_name

# 천간 지지 데이터
CHEONGAN = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
JIJI = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
OHAENG = {
    '갑': '목', '을': '목', '병': '화', '정': '화',
    '무': '토', '기': '토', '경': '금', '신': '금',
    '임': '수', '계': '수'
}
TIME_TO_JIJI = {
    (23, 1): '자', (1, 3): '축', (3, 5): '인', (5, 7): '묘',
    (7, 9): '진', (9, 11): '사', (11, 13): '오', (13, 15): '미',
    (15, 17): '신', (17, 19): '유', (19, 21): '술', (21, 23): '해'
}

# 카드 20장
CARDS = [
    ("새로운 시작", "🌱", "변화의 씨앗이 움트고 있어요"),
    ("균형", "⚖️", "내면의 조화를 찾을 때예요"),
    ("변화", "🌊", "흐름에 몸을 맡겨보세요"),
    ("인내", "🏔️", "지금의 노력이 결실을 맺어요"),
    ("도전", "⚡", "두려움을 넘어서는 날이에요"),
    ("휴식", "🌙", "충전이 필요한 시간이에요"),
    ("연결", "🤝", "소중한 인연이 다가와요"),
    ("내면의 목소리", "💫", "직관을 믿어보세요"),
    ("풍요", "🌟", "풍성함이 흘러들어오는 날이에요"),
    ("결단", "🗡️", "결정을 미루지 마세요"),
    ("흐름", "🌸", "자연스러운 흐름을 따르세요"),
    ("성장", "🌿", "한 단계 성장하는 날이에요"),
    ("비움", "🍃", "내려놓음으로써 얻게 돼요"),
    ("집중", "🎯", "한 가지에 집중하는 날이에요"),
    ("기회", "🚪", "문이 열리고 있어요"),
    ("조화", "🎵", "관계가 부드러워지는 날이에요"),
    ("용기", "🦁", "용감하게 나아갈 때예요"),
    ("직관", "🔮", "느낌을 믿어보세요"),
    ("감사", "🌈", "작은 것에서 행복을 찾아요"),
    ("완성", "👑", "마무리가 빛나는 날이에요"),
]

def calc_saju(birth_year, birth_month, birth_day, birth_hour):
    year_gan_idx = (birth_year - 4) % 10
    year_ji_idx = (birth_year - 4) % 12
    year_gan = CHEONGAN[year_gan_idx]
    year_ji = JIJI[year_ji_idx]
    month_gan_idx = ((birth_year % 10) * 2 + birth_month) % 10
    month_ji_idx = (birth_month + 1) % 12
    month_gan = CHEONGAN[month_gan_idx]
    month_ji = JIJI[month_ji_idx]
    base = date(1900, 1, 1)
    target = date(birth_year, birth_month, birth_day)
    days = (target - base).days
    day_gan = CHEONGAN[days % 10]
    day_ji = JIJI[days % 12]
    hour_ji = '자'
    for (start, end), ji in TIME_TO_JIJI.items():
        if start > end:
            if birth_hour >= start or birth_hour < end:
                hour_ji = ji
                break
        else:
            if start <= birth_hour < end:
                hour_ji = ji
                break
    hour_gan = CHEONGAN[((days % 5) * 2) % 10]
    return {
        '년주': f"{year_gan}{year_ji}",
        '월주': f"{month_gan}{month_ji}",
        '일주': f"{day_gan}{day_ji}",
        '시주': f"{hour_gan}{hour_ji}",
        '년간오행': OHAENG[year_gan],
        '일간오행': OHAENG[day_gan],
        '일간': day_gan
    }

def get_mbti_style(mbti):
    if len(mbti) >= 3 and mbti[1] == 'N' and mbti[2] == 'T':
        return "논리적이고 분석적인 언어로, 인과관계와 전략적 관점에서"
    elif len(mbti) >= 3 and mbti[1] == 'N' and mbti[2] == 'F':
        return "감성적이고 의미 중심적인 언어로, 가능성과 성장 관점에서"
    elif len(mbti) >= 3 and mbti[1] == 'S' and mbti[2] == 'J':
        return "안정적이고 현실적인 언어로, 구체적인 조언과 책임감 중심으로"
    else:
        return "직접적이고 실용적인 언어로, 현재와 자유 중심으로"

def get_enneagram_desc(ennea):
    desc = {
        1: "완벽주의적이고 원칙을 중시하는",
        2: "타인을 돕고 사랑받고 싶어하는",
        3: "성공과 인정을 추구하는",
        4: "독특함과 깊은 감성을 가진",
        5: "지식을 탐구하고 혼자만의 시간을 소중히 하는",
        6: "안전과 신뢰를 추구하는",
        7: "즐거움과 새로운 경험을 좋아하는",
        8: "강함과 독립을 추구하는",
        9: "평화와 조화를 중시하는"
    }
    return desc.get(ennea, "")

def get_concern_desc(concern):
    desc = {
        "❤️ 연애/결혼": "연애와 결혼 운",
        "💼 직업/커리어": "직업과 커리어 운",
        "📈 투자/주식/코인": "투자와 재물 운",
        "🏠 부동산": "부동산 운",
        "👥 인간관계": "인간관계 운",
        "💪 건강": "건강 운"
    }
    return desc.get(concern, "전반적인 운세")

def get_saju_interpretation(saju, mbti, enneagram, attachment, concern, card_name, api_key):
    mbti_style = get_mbti_style(mbti)
    ennea_desc = get_enneagram_desc(enneagram)
    concern_desc = get_concern_desc(concern)
    prompt = f"""당신은 전문 사주 명리학자예요.

사주 정보:
- 년주: {saju['년주']} ({saju['년간오행']})
- 월주: {saju['월주']}
- 일주: {saju['일주']} ({saju['일간오행']})
- 시주: {saju['시주']}
- 일간: {saju['일간']}

사용자 정보:
- MBTI: {mbti}
- 에니어그램: {enneagram}번 ({ennea_desc} 성격)
- 애착유형: {attachment}
- 주요 고민: {concern_desc}
- 오늘의 카드: {card_name}

위 정보를 바탕으로 {mbti_style} 해석해주세요.

다음 순서로 작성해주세요:
1. 전체적인 사주 특징 (3~4줄)
2. {concern_desc}에 대한 구체적인 해석 (4~5줄)
3. 오늘의 카드 "{card_name}"와 연계한 오늘의 조언 (2~3줄)
4. 이 사주를 가진 사람에게 한마디 (1~2줄)

친근하고 공감가는 말투로, 너무 어렵지 않게 써주세요.
이모지를 적절히 활용해주세요."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 1000}
    }
    res = requests.post(url, headers=headers, json=data, timeout=30)
    result = res.json()

    # 오류 처리
    if "error" in result:
        raise Exception(f"API 오류: {result['error']['message']}")
    if "candidates" not in result:
        raise Exception(f"응답 오류: {result}")
    return result["candidates"][0]["content"]["parts"][0]["text"]

# ===== UI 시작 =====

# 날씨 정보
now = datetime.now()
temp, code = get_weather()
color1, color2, weather_emoji, time_name = get_weather_theme(code, now.hour)
temp_str = f"{temp}°C" if temp is not None else ""

# 배경 CSS (날씨 반영)
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(160deg, {color1} 0%, {color2} 100%);
        min-height: 100vh;
    }}
    .main-title {{
        text-align: center;
        font-size: 2.8em;
        font-weight: bold;
        color: white;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
        margin-bottom: 5px;
    }}
    .sub-title {{
        text-align: center;
        font-size: 1em;
        color: rgba(255,255,255,0.7);
        margin-bottom: 10px;
    }}
    .weather-bar {{
        text-align: center;
        font-size: 1em;
        color: rgba(255,255,255,0.85);
        margin-bottom: 25px;
    }}
    .card-item {{
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 12px;
        padding: 15px 8px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s;
        color: white;
        backdrop-filter: blur(5px);
    }}
    .card-item:hover {{
        background: rgba(255,255,255,0.25);
        transform: translateY(-3px);
    }}
    .card-selected {{
        background: rgba(255,255,255,0.35) !important;
        border: 2px solid white !important;
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }}
    .card-emoji {{
        font-size: 2em;
        margin-bottom: 5px;
    }}
    .card-name {{
        font-size: 0.85em;
        font-weight: bold;
        color: white;
    }}
    .selected-card-box {{
        background: rgba(255,255,255,0.15);
        border: 2px solid rgba(255,255,255,0.5);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        color: white;
        margin: 20px 0;
        backdrop-filter: blur(10px);
    }}
    .result-box {{
        background: rgba(255,255,255,0.12);
        border-left: 4px solid rgba(255,255,255,0.6);
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
        color: white;
        backdrop-filter: blur(5px);
    }}
    .section-title {{
        color: white;
        font-size: 1.2em;
        font-weight: bold;
        margin: 20px 0 10px 0;
    }}
    .disclaimer {{
        text-align: center;
        font-size: 0.75em;
        color: rgba(255,255,255,0.5);
        margin-top: 30px;
    }}
    div[data-testid="stSelectbox"] label,
    div[data-testid="stRadio"] label,
    div[data-testid="stDateInput"] label,
    .stTextInput label {{
        color: white !important;
    }}
    div[data-testid="stRadio"] div {{
        color: white !important;
    }}
</style>
""", unsafe_allow_html=True)

# 타이틀
st.markdown('<div class="main-title">🔮 오늘의 사주</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">사주 × MBTI × 에니어그램 맞춤 해석</div>', unsafe_allow_html=True)
st.markdown(f'<div class="weather-bar">{weather_emoji} {time_name} · {now.strftime("%Y년 %m월 %d일")} · {temp_str}</div>', unsafe_allow_html=True)

st.markdown("---")

# 카드 선택
st.markdown('<div class="section-title">🃏 오늘의 카드를 골라보세요</div>', unsafe_allow_html=True)
st.markdown('<p style="color:rgba(255,255,255,0.7); font-size:0.9em;">마음이 끌리는 카드 하나를 클릭하세요</p>', unsafe_allow_html=True)

if 'selected_card' not in st.session_state:
    st.session_state.selected_card = None

# 카드 5열 4행으로 배치
cols_per_row = 5
for row in range(4):
    cols = st.columns(cols_per_row)
    for col_idx in range(cols_per_row):
        card_idx = row * cols_per_row + col_idx
        if card_idx < len(CARDS):
            card = CARDS[card_idx]
            with cols[col_idx]:
                is_selected = st.session_state.selected_card == card_idx
                btn_label = f"{card[1]}\n{card[0]}"
                if st.button(
                    f"{card[1]}\n{card[0]}",
                    key=f"card_{card_idx}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    st.session_state.selected_card = card_idx
                    st.rerun()

# 선택된 카드 표시
if st.session_state.selected_card is not None:
    selected = CARDS[st.session_state.selected_card]
    st.markdown(f"""
<div class="selected-card-box">
    <div style="font-size:0.85em; opacity:0.8;">선택한 카드</div>
    <div style="font-size:3.5em; margin: 10px 0;">{selected[1]}</div>
    <div style="font-size:1.6em; font-weight:bold; margin-bottom:8px;">{selected[0]}</div>
    <div style="font-size:0.95em; opacity:0.9;">{selected[2]}</div>
</div>
""", unsafe_allow_html=True)
    card_name = selected[0]
else:
    st.info("👆 위에서 카드를 선택해주세요")
    card_name = ""

st.markdown("---")

# 내 정보 입력
st.markdown('<div class="section-title">📋 내 정보 입력</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    birth_date = st.date_input(
        "생년월일",
        min_value=date(1940, 1, 1),
        max_value=date(2010, 12, 31),
        value=date(1996, 1, 1)
    )
with col2:
    birth_hour = st.selectbox(
        "태어난 시간",
        options=list(range(0, 24)),
        format_func=lambda x: f"{x:02d}시",
        index=12
    )

col3, col4 = st.columns(2)
with col3:
    mbti = st.selectbox(
        "MBTI",
        ["INTJ", "INTP", "ENTJ", "ENTP",
         "INFJ", "INFP", "ENFJ", "ENFP",
         "ISTJ", "ISFJ", "ESTJ", "ESFJ",
         "ISTP", "ISFP", "ESTP", "ESFP",
         "모름"]
    )
with col4:
    attachment = st.selectbox(
        "애착유형",
        ["안정형", "불안형", "회피형", "혼란형", "모름"]
    )

# 에니어그램
st.markdown('<div class="section-title">🧠 에니어그램 간이 테스트</div>', unsafe_allow_html=True)

answer_options = [
    ["옳고 그름, 원칙대로 사는 것",
     "사람들에게 필요한 존재가 되는 것",
     "목표를 달성하고 인정받는 것",
     "나만의 특별함과 깊은 감성",
     "지식을 쌓고 혼자만의 시간",
     "안전하고 믿을 수 있는 환경",
     "즐거움과 새로운 경험",
     "강하고 독립적인 것",
     "평화롭고 갈등 없는 삶"],
    ["잘못되거나 나쁜 사람이 되는 것",
     "사랑받지 못하고 혼자가 되는 것",
     "실패하고 무능해 보이는 것",
     "평범하고 특별하지 않은 것",
     "무능하고 쓸모없어지는 것",
     "지지 없이 혼자 남겨지는 것",
     "고통과 박탈감을 느끼는 것",
     "통제당하고 약해지는 것",
     "갈등과 분리되는 것"],
    ["더 완벽하게 하려고 집착한다",
     "주변 사람들을 더 챙긴다",
     "더 바쁘게 일에 몰두한다",
     "감정에 빠져 혼자 있고 싶다",
     "완전히 혼자 틀어박힌다",
     "최악의 시나리오를 생각한다",
     "다른 즐거운 것을 찾는다",
     "더 강하게 밀어붙인다",
     "아무것도 하기 싫어진다"]
]

questions = [
    "Q1. 나에게 가장 중요한 것은?",
    "Q2. 나의 가장 큰 두려움은?",
    "Q3. 스트레스 받을 때 나는?"
]

answers = []
for i, (q, opts) in enumerate(zip(questions, answer_options)):
    ans = st.radio(q, opts, key=f"ennea_q{i}")
    answers.append(opts.index(ans))

ennea_count = [0] * 9
for idx in answers:
    ennea_count[idx] += 1
enneagram = ennea_count.index(max(ennea_count)) + 1
st.info(f"에니어그램 간이 결과: **{enneagram}번 유형** — {get_enneagram_desc(enneagram)} 성격")

# 고민 선택
st.markdown('<div class="section-title">💭 오늘의 고민</div>', unsafe_allow_html=True)
concern = st.radio(
    "가장 궁금한 것을 선택하세요",
    ["❤️ 연애/결혼", "💼 직업/커리어", "📈 투자/주식/코인",
     "🏠 부동산", "👥 인간관계", "💪 건강"],
    horizontal=True
)

st.markdown("---")

# API 키
api_key = st.text_input("Google Gemini API Key", type="password", placeholder="AIza...")
st.caption("API 키는 저장되지 않으며 결과 생성 후 즉시 사라집니다.")

# 결과 생성
if st.button("🔮 사주 해석 보기", use_container_width=True, type="primary"):
    if not api_key:
        st.error("API 키를 입력해주세요.")
    elif not card_name:
        st.error("카드를 먼저 선택해주세요 🃏")
    else:
        with st.spinner("사주를 분석하고 있어요... 🔮"):
            try:
                saju = calc_saju(
                    birth_date.year, birth_date.month,
                    birth_date.day, birth_hour
                )

                st.markdown("---")
                st.markdown('<div class="section-title">📊 사주팔자</div>', unsafe_allow_html=True)
                c1, c2, c3, c4 = st.columns(4)
                with c1: st.metric("년주", saju['년주'])
                with c2: st.metric("월주", saju['월주'])
                with c3: st.metric("일주", saju['일주'])
                with c4: st.metric("시주", saju['시주'])

                st.markdown('<div class="section-title">🔮 맞춤 해석</div>', unsafe_allow_html=True)
                result = get_saju_interpretation(
                    saju, mbti, enneagram, attachment, concern, card_name, api_key
                )
                st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
                st.markdown("""
<div class="disclaimer">
※ 본 서비스는 재미와 참고용이며 실제 결정의 근거로 사용하지 마세요.<br>
입력하신 정보는 저장되지 않으며 결과 생성 후 즉시 삭제됩니다.
</div>
""", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"오류가 발생했어요: {str(e)}")
