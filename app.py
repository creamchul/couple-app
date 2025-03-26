import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import os

# 커스텀 모듈 불러오기
import utils
from data_handler import (
    init_data_dir, save_memory, save_today_word, load_today_word,
    load_all_memories, load_recent_memories, load_all_emotions,
    visualize_emotions, load_image
)
from gpt_handler import analyze_conversation

# 페이지 기본 설정
utils.page_config()

# 배경 추가 (원하는 이미지 URL로 변경 가능)
utils.add_bg_from_url('https://img.freepik.com/premium-vector/cute-romantic-hand-drawn-doodle-pattern-background_179234-513.jpg')

# 헤더 표시
utils.display_header()

# 데이터 디렉토리 초기화
init_data_dir()

# 세션 상태 초기화
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# 사이드바 네비게이션
st.sidebar.title("메뉴")

# 네비게이션 버튼들
if st.sidebar.button("🏠 홈"):
    st.session_state.current_page = 'home'
if st.sidebar.button("📚 추억 타임라인"):
    st.session_state.current_page = 'timeline'
if st.sidebar.button("💬 대화 분석"):
    st.session_state.current_page = 'conversation'
if st.sidebar.button("📊 감정 히스토리"):
    st.session_state.current_page = 'emotions'

# 현재 페이지에 따라 다른 내용 표시
if st.session_state.current_page == 'home':
    # 홈 페이지
    st.title("🏠 홈")
    
    # 오늘의 한마디
    st.header("💌 오늘의 한마디")
    
    # 기존의 오늘의 한마디 불러오기
    today_word_data = load_today_word()
    today_word = today_word_data.get('word', '')
    
    # 오늘의 한마디 입력 폼
    with st.form("today_word_form"):
        new_word = st.text_area("오늘 하고 싶은 말을 적어보세요:", value=today_word, height=100)
        submit_word = st.form_submit_button("저장하기")
    
    if submit_word:
        save_today_word(new_word)
        st.success("오늘의 한마디가 저장되었습니다! 💕")
        st.rerun()
    
    # 최근 추억 표시
    st.header("✨ 최근 추억")
    recent_memories = load_recent_memories(3)
    
    if not recent_memories.empty:
        for _, memory in recent_memories.iterrows():
            # 이미지 로드
            image = None
            if memory['image_path'] and not pd.isna(memory['image_path']):
                image = load_image(memory['image_path'])
            
            # 메모리 카드 표시
            utils.display_memory_card(
                memory['date'],
                memory['title'],
                memory['content'],
                memory['summary'],
                memory['emotion'],
                memory['empathy'],
                image
            )
    else:
        st.info("아직 저장된 추억이 없어요! '대화 분석' 탭에서 새로운 추억을 만들어보세요.")

elif st.session_state.current_page == 'timeline':
    # 추억 타임라인 페이지
    st.title("📚 추억 타임라인")
    
    # 모든 추억 불러오기
    all_memories = load_all_memories()
    
    if not all_memories.empty:
        for _, memory in all_memories.iterrows():
            # 이미지 로드
            image = None
            if memory['image_path'] and not pd.isna(memory['image_path']):
                image = load_image(memory['image_path'])
            
            # 메모리 카드 표시
            utils.display_memory_card(
                memory['date'],
                memory['title'],
                memory['content'],
                memory['summary'],
                memory['emotion'],
                memory['empathy'],
                image
            )
    else:
        st.info("아직 저장된 추억이 없어요! '대화 분석' 탭에서 새로운 추억을 만들어보세요.")

elif st.session_state.current_page == 'conversation':
    # 대화 분석 페이지
    st.title("💬 대화 분석")
    
    st.markdown("""
    대화 내용을 입력하면 AI가 다음을 생성합니다:
    1. 따뜻한 요약
    2. 감정 분석
    3. 공감 멘트
    """)
    
    # 대화 입력 폼
    with st.form("conversation_form"):
        title = st.text_input("추억의 제목:")
        conversation = st.text_area("대화 내용을 입력하세요:", height=200)
        
        # 이미지 업로드
        uploaded_file = st.file_uploader("이미지 추가하기 (선택사항)", type=["jpg", "jpeg", "png"])
        
        analyze_button = st.form_submit_button("분석하기")
    
    # 분석 버튼이 클릭되었을 때
    if analyze_button and conversation and title:
        with st.spinner("AI가 대화를 분석하고 있어요..."):
            # GPT로 대화 분석
            summary, emotion, empathy = analyze_conversation(conversation)
            
            # 결과 표시
            st.success("대화 분석이 완료되었습니다!")
            
            st.subheader("🌟 요약")
            st.write(summary)
            
            st.subheader("💭 감정 분석")
            st.write(emotion)
            
            st.subheader("💌 공감 멘트")
            st.write(empathy)
            
            # 이미지 처리
            image = None
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="업로드된 이미지", use_column_width=True)
            
            # 저장 버튼
            if st.button("추억으로 저장하기"):
                save_memory(title, conversation, summary, emotion, empathy, image)
                st.success("추억이 저장되었습니다! 💕")
                # 타임라인 페이지로 이동
                st.session_state.current_page = 'timeline'
                st.rerun()
    elif analyze_button:
        if not title:
            st.error("추억의 제목을 입력해주세요.")
        if not conversation:
            st.error("대화 내용을 입력해주세요.")

elif st.session_state.current_page == 'emotions':
    # 감정 히스토리 페이지
    st.title("📊 감정 히스토리")
    
    # 모든 감정 데이터 불러오기
    emotions_data = load_all_emotions()
    
    if not emotions_data.empty:
        # 감정 시각화
        emotion_chart = visualize_emotions()
        
        if emotion_chart:
            st.image(f"data:image/png;base64,{emotion_chart}", use_column_width=True)
        
        # 감정 데이터 테이블로 표시
        st.subheader("감정 기록")
        
        # 날짜 포맷 변경
        emotions_data['formatted_date'] = emotions_data['date'].apply(utils.format_date)
        
        # 테이블 표시
        for _, emotion in emotions_data.iterrows():
            st.markdown(f"""
            <div style="background-color: #f0f8ff; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                <div style="font-weight: bold; color: #1565C0;">{emotion['formatted_date']}</div>
                <div style="font-size: 18px; margin: 10px 0;">{emotion['emotion']}</div>
                <div style="color: #757575; font-size: 14px;">{emotion['reason']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("아직 감정 기록이 없어요! '대화 분석' 탭에서 대화를 통해 감정을 기록해보세요.")

# 푸터 추가
utils.create_footer() 