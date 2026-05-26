import streamlit as st
from datetime import date, datetime
import requests
import json
import time

st.set_page_config(
    page_title="수연이의 사주풀이방",
    page_icon="🔮",
    layout="wide"
)

# 날씨
def get_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 37.5665, "longitude": 126.9780,
            "current": ["temperature_2m", "weathercode"],
            "timezone": "Asia/Seoul"
        }
        res = requests.get(url, params=params, timeout=5)
        data = res.json()
        return data["current"]["temperature_2m"], data["current"]["weathercode"]
    except:
        return None, None

def get_weather_theme(code, hour):
    if 6 <= hour < 12: time_name = "아침"
    elif 12 <= hour < 18: time_name = "낮"
    elif 18 <= hour < 22: time_name = "저녁"
    else: time_name = "밤"
    if code is None: return "#0a0a2e", "#1a0533", "🌙", time_name
    elif code == 0:
        if 6 <= hour < 18: return "#0a2a6e", "#1a6eb5", "☀️", time_name
        else: return "#0a0a2e", "#1a0533", "🌙", time_name
    elif code in [1,2,3]: return "#2c3e50", "#4a5568", "⛅", time_name
    elif code in [51,53,55,61,63,65,80,81,82]: return "#1a2a3a", "#2d4a6e", "🌧️", time_name
    elif code in [71,73,75,77,85,86]: return "#2a3a4a", "#4a6a8a", "❄️", time_name
    elif code in [95,96,99]: return "#1a1a2e", "#2d1b69", "⛈️", time_name
    else: return "#1a0533", "#4A0E8F", "🌤️", time_name

CHEONGAN = ['갑','을','병','정','무','기','경','신','임','계']
JIJI = ['자','축','인','묘','진','사','오','미','신','유','술','해']
OHAENG = {'갑':'목','을':'목','병':'화','정':'화','무':'토','기':'토','경':'금','신':'금','임':'수','계':'수'}
TIME_TO_JIJI = {(23,1):'자',(1,3):'축',(3,5):'인',(5,7):'묘',(7,9):'진',(9,11):'사',(11,13):'오',(13,15):'미',(15,17):'신',(17,19):'유',(19,21):'술',(21,23):'해'}

CARDS = [
    ("새로운 시작","🌱","변화의 씨앗이 움트고 있어요. 두려워하지 말고 첫 발을 내딛어보세요."),
    ("균형","⚖️","내면의 조화를 찾을 때예요. 무엇이 흔들리고 있는지 돌아보세요."),
    ("변화","🌊","흐름에 몸을 맡겨보세요. 저항할수록 더 힘들어질 수 있어요."),
    ("인내","🏔️","지금의 노력이 반드시 결실을 맺어요. 조금만 더 버텨보세요."),
    ("도전","⚡","두려움을 넘어서는 날이에요. 망설임보다 행동이 답이에요."),
    ("휴식","🌙","충전이 필요한 시간이에요. 쉬는 것도 용기예요."),
    ("연결","🤝","소중한 인연이 다가오고 있어요. 마음을 열어보세요."),
    ("내면의 목소리","💫","직관을 믿어보세요. 머리보다 가슴이 먼저 알고 있어요."),
    ("풍요","🌟","풍성함이 흘러들어오는 날이에요. 감사한 마음으로 받아들이세요."),
    ("결단","🗡️","결정을 미루지 마세요. 지금이 바로 그 순간이에요."),
    ("흐름","🌸","자연스러운 흐름을 따르세요. 억지로 밀어붙이지 않아도 돼요."),
    ("성장","🌿","한 단계 성장하는 날이에요. 불편함이 곧 성장의 신호예요."),
    ("비움","🍃","내려놓음으로써 얻게 돼요. 집착을 버릴 때 새것이 들어와요."),
    ("집중","🎯","한 가지에 집중하는 날이에요. 분산된 에너지를 모아보세요."),
    ("기회","🚪","문이 열리고 있어요. 놓치지 말고 과감하게 들어가세요."),
    ("조화","🎵","관계가 부드러워지는 날이에요. 다름을 인정하면 갈등이 녹아요."),
    ("용기","🦁","용감하게 나아갈 때예요. 당신은 생각보다 훨씬 강해요."),
    ("직관","🔮","느낌을 믿어보세요. 오늘만큼은 분석보다 직감이 정확해요."),
    ("감사","🌈","작은 것에서 행복을 찾아요. 이미 가진 것들을 돌아보세요."),
    ("완성","👑","마무리가 빛나는 날이에요. 끝맺음이 새로운 시작이 돼요."),
]

def calc_saju(y, m, d, h):
    yg = CHEONGAN[(y-4)%10]; yj = JIJI[(y-4)%12]
    mg = CHEONGAN[((y%10)*2+m)%10]; mj = JIJI[(m+1)%12]
    days = (date(y,m,d)-date(1900,1,1)).days
    dg = CHEONGAN[days%10]; dj = JIJI[days%12]
    hj = '자'
    for (s,e),j in TIME_TO_JIJI.items():
        if s>e:
            if h>=s or h<e: hj=j; break
        else:
            if s<=h<e: hj=j; break
    hg = CHEONGAN[((days%5)*2)%10]
    return {'년주':f"{yg}{yj}",'월주':f"{mg}{mj}",'일주':f"{dg}{dj}",'시주':f"{hg}{hj}",'년간오행':OHAENG[yg],'일간오행':OHAENG[dg],'일간':dg}

def get_mbti_style(m):
    if len(m)>=3 and m[1]=='N' and m[2]=='T': return "논리적이고 분석적인 언어로, 인과관계와 전략적 관점에서"
    elif len(m)>=3 and m[1]=='N' and m[2]=='F': return "감성적이고 의미 중심적인 언어로, 가능성과 성장 관점에서"
    elif len(m)>=3 and m[1]=='S' and m[2]=='J': return "안정적이고 현실적인 언어로, 구체적인 조언과 책임감 중심으로"
    else: return "직접적이고 실용적인 언어로, 현재와 자유 중심으로"

def get_enneagram_desc(e):
    return {1:"완벽주의적이고 원칙을 중시하는",2:"타인을 돕고 사랑받고 싶어하는",3:"성공과 인정을 추구하는",4:"독특함과 깊은 감성을 가진",5:"지식을 탐구하는",6:"안전과 신뢰를 추구하는",7:"즐거움과 새로운 경험을 좋아하는",8:"강함과 독립을 추구하는",9:"평화와 조화를 중시하는"}.get(e,"")

def get_concern_desc(c):
    return {"❤️ 연애/결혼":"연애와 결혼 운","💼 직업/커리어":"직업과 커리어 운","📈 투자/주식/코인":"투자와 재물 운","🏠 부동산":"부동산 운","👥 인간관계":"인간관계 운","💪 건강":"건강 운"}.get(c,"전반적인 운세")

def get_saju_interpretation(saju, mbti, enneagram, attachment, concern, api_key):
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

위 정보를 바탕으로 {mbti_style} 해석해주세요.

다음 순서로 상세하게 작성해주세요:
1. 이 사주의 전체적인 특징과 타고난 기질 (4~5줄)
2. {concern_desc}에 대한 구체적이고 상세한 해석 (5~6줄)
3. 올해의 운세 흐름과 주의할 점 (3~4줄)
4. 이 사주를 가진 사람에게 전하는 조언 (2~3줄)

친근하고 공감가는 말투로 써주세요. 이모지를 적절히 활용해주세요."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"maxOutputTokens": 8192}}
    res = requests.post(url, headers=headers, json=data, timeout=30)
    result = res.json()
    if "error" in result: raise Exception(f"API 오류: {result['error']['message']}")
    if "candidates" not in result: raise Exception(f"응답 오류: {result}")
    return result["candidates"][0]["content"]["parts"][0]["text"]

# 세션 초기화
for key, val in [('page',1),('saju_data',None),('interpretation',''),('selected_card',None),('card_flipped',False)]:
    if key not in st.session_state:
        st.session_state[key] = val

# 날씨
now = datetime.now()
temp, code = get_weather()
color1, color2, weather_emoji, time_name = get_weather_theme(code, now.hour)
temp_str = f"{temp}°C" if temp else ""

# 배경 CSS
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(160deg, {color1} 0%, {color2} 100%);
        min-height: 100vh;
    }}
    .main-title {{ text-align:center; font-size:2.8em; font-weight:bold; color:white; text-shadow:0 2px 10px rgba(0,0,0,0.5); margin-bottom:5px; }}
    .sub-title {{ text-align:center; font-size:1em; color:rgba(255,255,255,0.7); margin-bottom:10px; }}
    .weather-bar {{ text-align:center; font-size:1em; color:rgba(255,255,255,0.85); margin-bottom:25px; }}
    .section-title {{ color:white; font-size:1.2em; font-weight:bold; margin:20px 0 10px 0; }}
    .result-box {{ background:rgba(255,255,255,0.12); border-left:4px solid rgba(255,255,255,0.6); border-radius:8px; padding:20px; margin:15px 0; color:white; }}
    .step-indicator {{ text-align:center; color:rgba(255,255,255,0.6); font-size:0.9em; margin-bottom:20px; }}
    .disclaimer {{ text-align:center; font-size:0.75em; color:rgba(255,255,255,0.5); margin-top:30px; }}
    div[data-testid="stRadio"] label, div[data-testid="stSelectbox"] label,
    div[data-testid="stDateInput"] label, .stTextInput label {{ color:white !important; }}
    div[data-testid="stRadio"] div {{ color:white !important; }}

    /* 카드 애니메이션 */
    .cards-container {{
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        justify-content: center;
        padding: 20px 0;
    }}
    .card-wrapper {{
        perspective: 1000px;
        width: 100px;
        height: 140px;
    }}
    .card-inner {{
        position: relative;
        width: 100%;
        height: 100%;
        transform-style: preserve-3d;
        transition: transform 0.6s ease;
        animation: floatIn 0.5s ease forwards;
        opacity: 0;
    }}
    .card-inner.flipped {{
        transform: rotateY(180deg);
    }}
    @keyframes floatIn {{
        0% {{ opacity:0; transform: rotateY(90deg) translateY(20px); }}
        100% {{ opacity:1; transform: rotateY(0deg) translateY(0); }}
    }}
    @keyframes sway {{
        0%, 100% {{ transform: rotate(-2deg) translateY(0px); }}
        50% {{ transform: rotate(2deg) translateY(-5px); }}
    }}
    .card-inner:not(.flipped) {{
        animation: floatIn 0.5s ease forwards, sway 3s ease-in-out infinite;
        animation-delay: var(--delay), calc(var(--delay) + 0.5s);
    }}
    .card-front, .card-back {{
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }}
    .card-front {{
        background: linear-gradient(135deg, #1a0533, #4A0E8F);
        border: 1px solid rgba(255,255,255,0.3);
        color: white;
        font-size: 2em;
    }}
    .card-back {{
        background: linear-gradient(135deg, #4A0E8F, #7B2FBE);
        border: 2px solid gold;
        color: white;
        transform: rotateY(180deg);
        padding: 8px;
        text-align: center;
    }}
    .card-back .emoji {{ font-size: 1.8em; margin-bottom: 5px; }}
    .card-back .name {{ font-size: 0.7em; font-weight: bold; }}
    .selected-card-result {{
        background: rgba(255,255,255,0.15);
        border: 2px solid gold;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        color: white;
        margin: 20px auto;
        max-width: 500px;
    }}
</style>
""", unsafe_allow_html=True)

# 타이틀
st.markdown('<div class="main-title">🔮 오늘의 사주</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">사주 × MBTI × 에니어그램 맞춤 해석</div>', unsafe_allow_html=True)
st.markdown(f'<div class="weather-bar">{weather_emoji} {time_name} · {now.strftime("%Y년 %m월 %d일")} · {temp_str}</div>', unsafe_allow_html=True)

# 스텝 표시
steps = ["① 정보 입력", "② 고민 선택", "③ 사주 해석", "④ 오늘의 카드"]
step_text = " → ".join([f"**{s}**" if i+1==st.session_state.page else s for i,s in enumerate(steps)])
st.markdown(f'<div class="step-indicator">{step_text}</div>', unsafe_allow_html=True)
st.markdown("---")

# ===== 1페이지: 정보 입력 =====
if st.session_state.page == 1:
    st.markdown('<div class="section-title">📋 기본 정보</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.date_input("생년월일", min_value=date(1940,1,1), max_value=date(2010,12,31), value=date(1996,1,1))
    with col2:
        birth_hour = st.selectbox("태어난 시간", list(range(24)), format_func=lambda x: f"{x:02d}시", index=12)

    col3, col4 = st.columns(2)
    with col3:
        mbti = st.selectbox("MBTI", ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP","ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP","모름"])
    with col4:
        attachment = st.selectbox("애착유형", ["안정형","불안형","회피형","혼란형","모름"])

    st.markdown('<div class="section-title">🧠 에니어그램 간이 테스트</div>', unsafe_allow_html=True)

    answer_options = [
        ["옳고 그름, 원칙대로 사는 것","사람들에게 필요한 존재가 되는 것","목표를 달성하고 인정받는 것","나만의 특별함과 깊은 감성","지식을 쌓고 혼자만의 시간","안전하고 믿을 수 있는 환경","즐거움과 새로운 경험","강하고 독립적인 것","평화롭고 갈등 없는 삶"],
        ["잘못되거나 나쁜 사람이 되는 것","사랑받지 못하고 혼자가 되는 것","실패하고 무능해 보이는 것","평범하고 특별하지 않은 것","무능하고 쓸모없어지는 것","지지 없이 혼자 남겨지는 것","고통과 박탈감을 느끼는 것","통제당하고 약해지는 것","갈등과 분리되는 것"],
        ["더 완벽하게 하려고 집착한다","주변 사람들을 더 챙긴다","더 바쁘게 일에 몰두한다","감정에 빠져 혼자 있고 싶다","완전히 혼자 틀어박힌다","최악의 시나리오를 생각한다","다른 즐거운 것을 찾는다","더 강하게 밀어붙인다","아무것도 하기 싫어진다"]
    ]
    questions = ["Q1. 나에게 가장 중요한 것은?","Q2. 나의 가장 큰 두려움은?","Q3. 스트레스 받을 때 나는?"]
    answers = [answer_options[i].index(st.radio(q, answer_options[i], key=f"eq{i}")) for i,q in enumerate(questions)]
    ennea_count = [0]*9
    for idx in answers: ennea_count[idx] += 1
    enneagram = ennea_count.index(max(ennea_count)) + 1
    st.info(f"에니어그램 간이 결과: **{enneagram}번 유형** — {get_enneagram_desc(enneagram)} 성격")

    if st.button("다음 →", use_container_width=True, type="primary"):
        st.session_state.birth_date = birth_date
        st.session_state.birth_hour = birth_hour
        st.session_state.mbti = mbti
        st.session_state.attachment = attachment
        st.session_state.enneagram = enneagram
        st.session_state.page = 2
        st.rerun()

# ===== 2페이지: 고민 선택 =====
elif st.session_state.page == 2:
    st.markdown('<div class="section-title">💭 오늘 가장 궁금한 것은?</div>', unsafe_allow_html=True)

    concerns = ["❤️ 연애/결혼","💼 직업/커리어","📈 투자/주식/코인","🏠 부동산","👥 인간관계","💪 건강"]
    cols = st.columns(2)
    selected = None
    if 'concern' not in st.session_state: st.session_state.concern = concerns[0]

    for i, c in enumerate(concerns):
        with cols[i%2]:
            is_sel = st.session_state.concern == c
            if st.button(c, use_container_width=True, type="primary" if is_sel else "secondary", key=f"concern_{i}"):
                st.session_state.concern = c
                st.rerun()

    st.markdown(f"<p style='color:white; margin-top:15px;'>선택된 고민: <b>{st.session_state.concern}</b></p>", unsafe_allow_html=True)

    col_back, col_next = st.columns(2)
    with col_back:
        if st.button("← 이전", use_container_width=True):
            st.session_state.page = 1
            st.rerun()
    with col_next:
        if st.button("사주 해석 보기 →", use_container_width=True, type="primary"):
            st.session_state.page = 3
            st.rerun()

# ===== 3페이지: 사주 해석 =====
elif st.session_state.page == 3:
    if not st.session_state.interpretation:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
        if not api_key:
            api_key = st.text_input("Google Gemini API Key", type="password", placeholder="AIza...")

        if api_key:
            with st.spinner("사주를 분석하고 있어요... 🔮"):
                try:
                    saju = calc_saju(
                        st.session_state.birth_date.year,
                        st.session_state.birth_date.month,
                        st.session_state.birth_date.day,
                        st.session_state.birth_hour
                    )
                    st.session_state.saju_data = saju
                    result = get_saju_interpretation(
                        saju, st.session_state.mbti,
                        st.session_state.enneagram,
                        st.session_state.attachment,
                        st.session_state.concern,
                        api_key
                    )
                    st.session_state.interpretation = result
                    st.rerun()
                except Exception as e:
                    st.error(f"오류가 발생했어요: {str(e)}")
    else:
        saju = st.session_state.saju_data
        st.markdown('<div class="section-title">📊 사주팔자</div>', unsafe_allow_html=True)
        c1,c2,c3,c4 = st.columns(4)
        with c1: st.metric("년주", saju['년주'])
        with c2: st.metric("월주", saju['월주'])
        with c3: st.metric("일주", saju['일주'])
        with c4: st.metric("시주", saju['시주'])

        st.markdown('<div class="section-title">🔮 맞춤 해석</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-box">{st.session_state.interpretation}</div>', unsafe_allow_html=True)

        st.markdown('<div class="disclaimer">※ 본 서비스는 재미와 참고용이며 실제 결정의 근거로 사용하지 마세요.</div>', unsafe_allow_html=True)

        col_back, col_next = st.columns(2)
        with col_back:
            if st.button("← 이전", use_container_width=True):
                st.session_state.page = 2
                st.rerun()
        with col_next:
            if st.button("🃏 오늘의 카드 뽑기 →", use_container_width=True, type="primary"):
                st.session_state.page = 4
                st.session_state.selected_card = None
                st.session_state.card_flipped = False
                st.rerun()

# ===== 4페이지: 오늘의 카드 =====
elif st.session_state.page == 4:
    st.markdown('<div class="section-title">🃏 오늘의 카드</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:rgba(255,255,255,0.8);">마음이 끌리는 카드를 하나 선택하세요</p>', unsafe_allow_html=True)

    if st.session_state.selected_card is None:
        # 카드 착착착 애니메이션
        cards_html = '<div class="cards-container">'
        for i, card in enumerate(CARDS):
            delay = i * 0.1
            cards_html += f'''
            <div class="card-wrapper" onclick="selectCard({i})">
                <div class="card-inner" id="card-{i}" style="--delay: {delay}s">
                    <div class="card-front">🔮</div>
                    <div class="card-back">
                        <div class="emoji">{card[1]}</div>
                        <div class="name">{card[0]}</div>
                    </div>
                </div>
            </div>'''
        cards_html += '</div>'

        # 카드 선택 버튼 (5열)
        cols = st.columns(5)
        for i, card in enumerate(CARDS):
            with cols[i % 5]:
                if st.button(f"{card[1]}\n{card[0]}", key=f"c{i}", use_container_width=True):
                    st.session_state.selected_card = i
                    st.rerun()
    else:
        # 선택된 카드 결과
        card = CARDS[st.session_state.selected_card]
        st.markdown(f"""
<div class="selected-card-result">
    <div style="font-size:0.85em; opacity:0.8; margin-bottom:10px;">오늘의 카드</div>
    <div style="font-size:4em; margin-bottom:10px;">{card[1]}</div>
    <div style="font-size:1.8em; font-weight:bold; margin-bottom:15px; color:gold;">{card[0]}</div>
    <div style="font-size:1em; line-height:1.7; opacity:0.95;">{card[2]}</div>
</div>
""", unsafe_allow_html=True)

        col_back, col_reset = st.columns(2)
        with col_back:
            if st.button("← 해석으로 돌아가기", use_container_width=True):
                st.session_state.page = 3
                st.rerun()
        with col_reset:
            if st.button("🔄 처음부터 다시", use_container_width=True):
                for key in ['page','saju_data','interpretation','selected_card','card_flipped','birth_date','birth_hour','mbti','attachment','enneagram','concern']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
