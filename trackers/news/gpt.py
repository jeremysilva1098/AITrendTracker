from freeplay import Freeplay
from freeplay.provider_config import ProviderConfig, OpenAIConfig
import os
import pathlib
from data_models import NewsArticle, NewsArticleSummary
from typing import List, Optional
from dotenv import load_dotenv
import json

# load in the env variables
par_dir = pathlib.Path(__file__).parent.parent
dotenv_dir = f"{par_dir}/.env"
print("Reading .env variables from: ", dotenv_dir)
load_dotenv(dotenv_path=dotenv_dir)


class freeplayGPT:
    def __init__(self) -> None:
        # freeplay vars
        self.freeplay_key = os.getenv("FREEPLAY_KEY")
        self.freeplay_project_id = os.getenv("FREEPLAY_PROJECT_ID")
        self.freeplay_sub_domain = os.getenv("FREEPLAY_SUB_DOMAIN")
        self.freeplay_url = f"https://{self.freeplay_sub_domain}.freeplay.ai/api"
        # openai vars
        self.openai_key = os.getenv("OPENAI_API_KEY")
        # create a freeplay chat client
        self.freeplay_client = Freeplay(
            provider_config=ProviderConfig(
                openai=OpenAIConfig(api_key=self.openai_key)
            ),
            freeplay_api_key=self.freeplay_key,
            api_base = self.freeplay_url
        )
    

    def select_best_stories(self, articles: List[NewsArticle],
                             num_articles: int = 3, max_tokens: int = 16000) -> List[NewsArticle]:
        # make sure content is under 16000
        num_tokens = 0
        article_subset = []
        for article in articles:
            num_tokens += len(article.content) / 4
            if num_tokens < max_tokens * 0.8:
                article_subset.append(article)
            else:
                break
        result = self.freeplay_client.get_completion(
            project_id=self.freeplay_project_id,
            template_name="select_best_news_stories",
            variables={'number_of_articles': str(num_articles),
                       'articles': str(article_subset)}
        )
        # get the response
        titles = result.content
        # create output
        resSet = []
        for artilce in article_subset:
            if artilce.title in titles:
                resSet.append(artilce)
        return resSet
    
    
    def summarize_story(self, article: NewsArticle) -> NewsArticleSummary:
        result = self.freeplay_client.get_completion(
            project_id=self.freeplay_project_id,
            template_name="summarize_news_story",
            variables={'article': str(article)}
        )
        return NewsArticleSummary(
            title=article.title,
            summary=result.content,
            url=article.url,
            source=article.source
        )
    

    def gen_html(self, article_summaries: List[NewsArticleSummary]) -> str:
        result = self.freeplay_client.get_completion(
            project_id=self.freeplay_project_id,
            template_name="gen_news_html",
            variables={'article_summaries': str(article_summaries)}
        )
        return result.content
    



