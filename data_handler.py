import os
import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image
import io
import base64

# 데이터 저장 경로
DATA_DIR = 'data'
MEMORIES_FILE = os.path.join(DATA_DIR, 'memories.csv')
EMOTIONS_FILE = os.path.join(DATA_DIR, 'emotions.csv')
TODAY_WORD_FILE = os.path.join(DATA_DIR, 'today_word.json')

# 데이터 디렉토리 초기화
def init_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(os.path.join(DATA_DIR, 'images')):
        os.makedirs(os.path.join(DATA_DIR, 'images'))
    
    # 메모리 파일 초기화
    if not os.path.exists(MEMORIES_FILE):
        df = pd.DataFrame(columns=['date', 'title', 'content', 'summary', 'emotion', 'empathy', 'image_path'])
        df.to_csv(MEMORIES_FILE, index=False)
    
    # 감정 파일 초기화
    if not os.path.exists(EMOTIONS_FILE):
        df = pd.DataFrame(columns=['date', 'emotion', 'reason'])
        df.to_csv(EMOTIONS_FILE, index=False)
    
    # 오늘의 한마디 파일 초기화
    if not os.path.exists(TODAY_WORD_FILE):
        with open(TODAY_WORD_FILE, 'w') as f:
            json.dump({'date': datetime.now().strftime('%Y-%m-%d'), 'word': ''}, f)

# 추억 저장 함수
def save_memory(title, content, summary, emotion, empathy, image=None):
    init_data_dir()
    
    # 현재 날짜 가져오기
    date = datetime.now().strftime('%Y-%m-%d')
    
    # 이미지 저장 경로
    image_path = None
    if image is not None:
        image_filename = f"{date}_{title.replace(' ', '_')}.jpg"
        image_path = os.path.join('images', image_filename)
        image.save(os.path.join(DATA_DIR, image_path))
    
    # 기존 데이터 로드
    memories = pd.read_csv(MEMORIES_FILE)
    
    # 새 데이터 추가
    new_memory = pd.DataFrame({
        'date': [date],
        'title': [title],
        'content': [content],
        'summary': [summary],
        'emotion': [emotion],
        'empathy': [empathy],
        'image_path': [image_path]
    })
    
    memories = pd.concat([memories, new_memory], ignore_index=True)
    memories.to_csv(MEMORIES_FILE, index=False)
    
    # 감정 데이터도 저장
    save_emotion(date, emotion, "대화 기반 감정 분석")
    
    return True

# 감정 저장 함수
def save_emotion(date, emotion, reason):
    init_data_dir()
    
    # 기존 데이터 로드
    emotions = pd.read_csv(EMOTIONS_FILE)
    
    # 같은 날짜에 이미 감정이 저장되어 있는지 확인
    if date in emotions['date'].values:
        emotions.loc[emotions['date'] == date, ['emotion', 'reason']] = [emotion, reason]
    else:
        new_emotion = pd.DataFrame({
            'date': [date],
            'emotion': [emotion],
            'reason': [reason]
        })
        emotions = pd.concat([emotions, new_emotion], ignore_index=True)
    
    emotions.to_csv(EMOTIONS_FILE, index=False)
    return True

# 오늘의 한마디 저장 함수
def save_today_word(word):
    init_data_dir()
    
    date = datetime.now().strftime('%Y-%m-%d')
    
    with open(TODAY_WORD_FILE, 'w') as f:
        json.dump({'date': date, 'word': word}, f)
    
    return True

# 오늘의 한마디 불러오기 함수
def load_today_word():
    init_data_dir()
    
    try:
        with open(TODAY_WORD_FILE, 'r') as f:
            data = json.load(f)
        return data
    except:
        return {'date': datetime.now().strftime('%Y-%m-%d'), 'word': ''}

# 모든 추억 불러오기 함수
def load_all_memories():
    init_data_dir()
    
    try:
        memories = pd.read_csv(MEMORIES_FILE)
        return memories.sort_values('date', ascending=False)
    except:
        return pd.DataFrame(columns=['date', 'title', 'content', 'summary', 'emotion', 'empathy', 'image_path'])

# 최근 추억 N개 불러오기 함수
def load_recent_memories(n=3):
    memories = load_all_memories()
    return memories.head(n)

# 특정 날짜의 추억 불러오기 함수
def load_memory_by_date(date):
    memories = load_all_memories()
    return memories[memories['date'] == date]

# 모든 감정 데이터 불러오기 함수
def load_all_emotions():
    init_data_dir()
    
    try:
        emotions = pd.read_csv(EMOTIONS_FILE)
        return emotions.sort_values('date')
    except:
        return pd.DataFrame(columns=['date', 'emotion', 'reason'])

# 감정 시각화 함수
def visualize_emotions():
    emotions = load_all_emotions()
    
    if emotions.empty:
        return None
    
    # 날짜와 감정만 추출
    plt.figure(figsize=(12, 5))
    
    # 자주 등장하는 감정들
    common_emotions = ['기쁨', '행복', '설렘', '사랑', '감동', '감사', '그리움', '기대', 
                      '슬픔', '우울', '불안', '걱정', '화남', '짜증', '답답함']
    
    # 감정이 자주 등장하는 감정 중 하나인지 확인
    def map_emotion(emotion_text):
        for common in common_emotions:
            if common in emotion_text:
                return common
        return emotion_text.split()[0]  # 첫 번째 단어만 사용
    
    # 감정 매핑
    emotions['mapped_emotion'] = emotions['emotion'].apply(map_emotion)
    
    # 그래프 생성
    emotion_counts = emotions['mapped_emotion'].value_counts()
    plt.figure(figsize=(10, 6))
    emotion_counts.plot(kind='bar', color='skyblue')
    plt.title('감정 분포')
    plt.xlabel('감정')
    plt.ylabel('횟수')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 이미지 바이트로 변환
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # 이미지 인코딩
    img_str = base64.b64encode(buf.read()).decode()
    plt.close()
    
    return img_str

# 이미지 로드 함수
def load_image(image_path):
    if image_path and not pd.isna(image_path):
        try:
            return Image.open(os.path.join(DATA_DIR, image_path))
        except:
            return None
    return None 