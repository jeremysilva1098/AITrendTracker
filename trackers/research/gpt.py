from freeplay import Freeplay
from freeplay.provider_config import ProviderConfig, OpenAIConfig
import os
import pathlib
from data_models import Article, ArticleSummary
from typing import List, Optional
from dotenv import load_dotenv

# load in the env variables
'''par_dir = pathlib.Path(__file__).parent.parent
dotenv_dir = f"{par_dir}/.env"
print("Reading .env variables from: ", dotenv_dir)
load_dotenv(dotenv_path=dotenv_dir)'''
print("Env variables:")
print(os.environ)


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
    

    def rank_articles(self, articles: List[Article]) -> str:
        result = self.freeplay_client.get_completion(
            project_id=self.freeplay_project_id,
            template_name="rank_research_articles",
            variables={'article_summaries': articles}
        )
        return result.content
    

    def determine_relevant_articles(self, articles: List[Article]) -> List[Article]:
        '''pass one article at a time to the model and determine if it is relevant'''
        rel_articles = []
        for article in list(articles.values()):
            title = article.title
            summary = article.summary
            result = self.freeplay_client.get_completion(
                project_id=self.freeplay_project_id,
                template_name="is_research_article_relevant",
                variables={'article_title': title, 'article_summary': summary}
            )
            res = result.content.strip()
            print(f'{title}: {res}')
            if res == "YES":
                rel_articles.append(article)
        return rel_articles
    

    def pick_best_article(self, topic: str, articles: List[Article]) -> Optional[Article]:
        '''pick the best article from the list of relevant articles'''
        result = self.freeplay_client.get_completion(
            project_id=self.freeplay_project_id,
            template_name="pick_best_research_article",
            variables={'topic': topic, 'article_summaries': str(articles)}
        )
        bestLink = result.content.strip()
        # find the article with the best link
        for article in articles:
            if article.link == bestLink:
                return article
        return None
    

    def summarize_article(self, article_text: str) -> str:
        result = self.freeplay_client.get_completion(
            project_id=self.freeplay_project_id,
            template_name="sum_research_article",
            variables={'article_text': article_text}
        )
        return result.content
    

    def generate_article_summary_html(self, article_summaries: List[ArticleSummary]) -> str:
        result = self.freeplay_client.get_completion(
            project_id=self.freeplay_project_id,
            template_name="gen_articles_html",
            variables={'article_summaries': str(article_summaries)}
        )
        return result.content


