from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper


def get_profile_url_tavily(name: str) -> str:
    search = TavilySearchAPIWrapper()
    res = search.results(f"{name} linkedin profile")

    if res and len(res) > 0:
        return res[0]["url"]
    return "No LinkedIn profile found"


if __name__ == "__main__":
    print(get_profile_url_tavily(name="김형민"))
