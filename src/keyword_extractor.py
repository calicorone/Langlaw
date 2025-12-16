from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LLM 구성 (ChatGPT 모델 기반)
llm = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0)

# 프롬프트 템플릿 (메시지 기반 최신 구조)
prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 법률 사건 분석을 위한 키워드 추출 전문가야."),
    ("human", """다음은 사용자가 실제로 겪고 있는 사건 설명이야:

"{description}"

이 사건에 대해 핵심 법적 키워드를 3~5개 JSON 배열로 뽑아줘.
예시 형식: ["교통사고", "업무상과실", "신호위반", "형법"]
""")
])

# 최신 방식 체인 구성
chain: Runnable = prompt | llm

def extract_keywords_from_case(description: str):
    response = chain.invoke({"description": description})
    return response.content  # content 속에 응답 텍스트 포함
