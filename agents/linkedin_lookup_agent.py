import sys
import os

# 현재 파일의 절대 경로
current_file = os.path.abspath(__file__)
# 프로젝트 루트 디렉토리
project_root = os.path.dirname(os.path.dirname(current_file))

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(project_root)


from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# 체인 또는 LLM이 외부세계와 상호작용하도록 돕는 인터페이스
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor

# 커뮤니티와 langchain이 미리 정의한 프롬프트를 다운로드
from langchain import hub
from tools.tools import get_profile_url_tavily


load_dotenv()


# 이름을 받아 linkedin url을 반환
def linkedin_lookup_agent(name: str) -> str:
    # GPT-4를 사용하여 낮은 temperature로 일관된 출력 생성
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

    # LinkedIn 프로필 URL을 얻기 위한 프롬프트 템플릿 정의
    template = """
        Given the full name {name_of_person}
        I want you to get it me a link to their LinkedIn profile page.
        Your answer should be contain only a URL
    """

    # 템플릿에 변수를 주입할 수 있는 PromptTemplate 객체 생성
    prompt_template = PromptTemplate(
        input_variables=["name_of_person"], template=template
    )

    # 에이전트가 사용할 도구 정의
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 LinkedIn profile page",  # 도구의 이름
            func=get_profile_url_tavily,  # 실제 구글 크롤링 함수가 들어갈 자리
            description="useful for when you need get the Linkedin Page URL",  # LLM이 이 도구를 언제 사용할지 판단하는 데 사용
        )
    ]

    # ReAct 프롬프트 템플릿을 Langchain Hub에서 가져옴
    react_prompt = hub.pull("hwchase17/react")

    # LLM, 도구, 프롬프트를 결합하여 ReAct 에이전트 생성
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)

    # 에이전트 실행기 생성 (verbose=True로 설정하여 실행 과정을 볼 수 있음)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    # 프롬프트 템플릿에 이름을 넣고 에이전트에게 전달하여 실행
    result = agent_executor.invoke(
        input={"input": prompt_template.format(name_of_person=name)}
    )

    # 결과에서 LinkedIn 프로필 URL 추출
    linkedin_profile_url = result["output"]

    return linkedin_profile_url


if __name__ == "__main__":
    print(linkedin_lookup_agent(name="김형민 모요"))
