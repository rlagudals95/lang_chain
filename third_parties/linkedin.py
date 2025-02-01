import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str = "", mock: bool = False):

    if mock:
        response = requests.get(
            "https://gist.githubusercontent.com/paul-villalobos/c59167135dea9081021d53b2faebad66/raw/88ec8ce557de26be827cd29a617dceee3eb9306d/eden-marco.json",
            timeout=10,
        )
    else:
        api_endpoint = f"https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f"Bearer {os.environ.get('PROXYCURL_API_KEY')}"}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10,
        )

    data = response.json()

    data = {
        k: v
        for k, v in data.items()
        if v not in [[], "", "", None]  # 빈 리스트, 빈 문자열, None 값을 제거
        and k not in ["people_also_viewed", "certifications"]  # 특정 키를 제외
    }

    if data.get("groups"):
        for group_dict in data["groups"]:
            group_dict.pop("profile_pic_url")  # 각 그룹에서 프로필 사진 URL 제거

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            "https://www.linkedin.com/in/%ED%98%95%EB%AF%BC-%EA%B9%80-68b4a7213/",
            mock=True,
        )
    )
