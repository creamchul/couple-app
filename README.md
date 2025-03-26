# 우리의 이야기

연인과의 특별한 대화와 추억을 기록하고, AI가 그 대화를 요약하고 감정을 분석해주는 감성적인 커플 웹앱입니다.

## 주요 기능

1. **홈**: 오늘의 한마디 입력, 최근 대화/추억 미리보기
2. **추억 타임라인**: 날짜, 제목, 내용, 이미지로 구성된 추억 카드
3. **대화 저장 + AI 분석**: 대화 입력 후 GPT를 통한 요약, 감정 분석, 공감 멘트 생성
4. **감정 히스토리**: 날짜별 감정 상태 저장 및 시각화

## 설치 방법

1. 저장소 클론
   ```bash
   git clone https://github.com/yourusername/our-story.git
   cd our-story
   ```

2. 필요한 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```

3. OpenAI API 키 설정
   - `.env` 파일 생성 후 API 키 추가
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

4. 앱 실행
   ```bash
   streamlit run app.py
   ```

## 사용 기술

- Streamlit (웹앱 프론트엔드)
- OpenAI API (GPT 모델 사용)
- Pandas (데이터 관리)
- Matplotlib (데이터 시각화) 