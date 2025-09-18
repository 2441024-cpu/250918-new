import streamlit as st

st.set_page_config(page_title="수학 퀴즈 게임", page_icon="🧮", layout="centered")
st.title("수학 퀴즈 게임")

# 세션 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "question" not in st.session_state:
    st.session_state.question = ""
if "answer" not in st.session_state:
    st.session_state.answer = None
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "쉬움"

import random

def generate_question(difficulty):
    if difficulty == "쉬움":
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        op = random.choice(["+", "-"])
        if op == "+":
            answer = num1 + num2
        else:
            answer = num1 - num2
        question = f"{num1} {op} {num2} = ?"
    elif difficulty == "보통":
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 50)
        op = random.choice(["+", "-", "×"])
        if op == "+":
            answer = num1 + num2
        elif op == "-":
            answer = num1 - num2
        else:
            answer = num1 * num2
        question = f"{num1} {op} {num2} = ?"
    else:
        # 어려움
        op = random.choice(["+", "-", "×", "÷"])
        if op == "÷":
            num2 = random.randint(1, 100)
            answer = random.randint(1, 100)
            num1 = num2 * answer
            question = f"{num1} ÷ {num2} = ?"
        else:
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 100)
            if op == "+":
                answer = num1 + num2
            elif op == "-":
                answer = num1 - num2
            else:
                answer = num1 * num2
            question = f"{num1} {op} {num2} = ?"
    return question, answer

# 난이도 선택
difficulty = st.selectbox("난이도 선택", ["쉬움", "보통", "어려움"], index=["쉬움", "보통", "어려움"].index(st.session_state.difficulty))
if difficulty != st.session_state.difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.score = 0
    st.session_state.question, st.session_state.answer = generate_question(difficulty)

# 문제 생성 (최초 또는 정답 제출 후)
if st.session_state.question == "":
    st.session_state.question, st.session_state.answer = generate_question(st.session_state.difficulty)

st.markdown(f"<div style='font-size:1.3rem; margin:20px 0;'>{st.session_state.question}</div>", unsafe_allow_html=True)

user_input = st.text_input("정답을 입력하세요", key="user_answer", value="")

col1, col2 = st.columns([1,1])
submit = col1.button("제출")
reset = col2.button("점수 초기화")

if reset:
    st.session_state.score = 0
    st.session_state.question, st.session_state.answer = generate_question(st.session_state.difficulty)
    st.experimental_rerun()

if submit:
    try:
        user_ans = float(user_input)
        correct = False
        if st.session_state.difficulty == "어려움" and "÷" in st.session_state.question:
            correct = abs(user_ans - st.session_state.answer) < 1e-6
        else:
            correct = user_ans == st.session_state.answer
        if correct:
            st.session_state.score += 1
            st.success("정답입니다! +1점")
        else:
            st.session_state.score -= 1
            st.error(f"오답입니다! 정답: {st.session_state.answer}")
        st.session_state.question, st.session_state.answer = generate_question(st.session_state.difficulty)
        st.experimental_rerun()
    except ValueError:
        st.warning("숫자를 입력하세요.")

st.markdown(f"<div style='font-size:1.1rem; margin-top:16px;'>점수: <b>{st.session_state.score}</b></div>", unsafe_allow_html=True)
