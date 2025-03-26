import os
from openai import OpenAI
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# GPT 모델 설정
GPT_MODEL = "gpt-3.5-turbo"

# 요약 프롬프트
SUMMARY_PROMPT = "이 대화를 짧고 따뜻하게 요약해줘. 핵심 키워드를 포함해서 2~3줄로 정리해줘."

# 감정 분석 프롬프트
EMOTION_PROMPT = "이 대화를 읽고 느껴지는 감정을 하나 또는 두 개로 정리해줘. 감정 단어와 간단한 이유를 말해줘."

# 공감 멘트 프롬프트
EMPATHY_PROMPT = "이 대화에 어울리는 다정한 공감의 한마디를 해줘. 1문장으로 부탁해."

def analyze_conversation(conversation):
    """
    대화 내용을 분석하여 요약, 감정 분석, 공감 멘트를 반환합니다.
    
    Args:
        conversation (str): 분석할 대화 내용
        
    Returns:
        tuple: (요약, 감정 분석, 공감 멘트)
    """
    try:
        # 요약 생성
        summary = generate_summary(conversation)
        
        # 감정 분석
        emotion = analyze_emotion(conversation)
        
        # 공감 멘트 생성
        empathy = generate_empathy(conversation)
        
        return summary, emotion, empathy
    
    except Exception as e:
        print(f"GPT API 호출 중 오류 발생: {e}")
        return (
            "API 오류로 요약을 생성하지 못했습니다.", 
            "API 오류로 감정을 분석하지 못했습니다.", 
            "API 오류로 공감 멘트를 생성하지 못했습니다."
        )

def generate_summary(conversation):
    """
    대화 내용을 요약합니다.
    
    Args:
        conversation (str): 요약할 대화 내용
        
    Returns:
        str: 요약된 내용
    """
    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "당신은 커플의 대화를 따뜻하게 요약해주는 AI입니다."},
                {"role": "user", "content": f"{conversation}\n\n{SUMMARY_PROMPT}"}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"요약 생성 중 오류 발생: {e}")
        return "요약을 생성하지 못했습니다."

def analyze_emotion(conversation):
    """
    대화 내용을 바탕으로 감정을 분석합니다.
    
    Args:
        conversation (str): 분석할 대화 내용
        
    Returns:
        str: 감정 분석 결과
    """
    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "당신은 커플의 대화에서 감정을 분석하는 AI입니다."},
                {"role": "user", "content": f"{conversation}\n\n{EMOTION_PROMPT}"}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"감정 분석 중 오류 발생: {e}")
        return "감정을 분석하지 못했습니다."

def generate_empathy(conversation):
    """
    대화 내용에 대한 공감 멘트를 생성합니다.
    
    Args:
        conversation (str): 공감할 대화 내용
        
    Returns:
        str: 공감 멘트
    """
    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "당신은 커플의 대화에 공감하는 따뜻한 AI입니다."},
                {"role": "user", "content": f"{conversation}\n\n{EMPATHY_PROMPT}"}
            ],
            max_tokens=100,
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"공감 멘트 생성 중 오류 발생: {e}")
        return "공감 멘트를 생성하지 못했습니다." 