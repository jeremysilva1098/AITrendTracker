from arxiv import arxivApi
from gpt import freeplayGPT
import datetime
import json
from data_models import ArticleSummary
import os


# set the min and max date
maxDate = datetime.datetime.now()
minDate = maxDate - datetime.timedelta(days=7)

search_topics = [
    "LLM Evaluation", "LLM Optimization",
    "AI Agents", "LLM Prompt Engineering",
    "Retrieval Augemented Generation",
    "LLM Fine Tuning", "LLM Function Calling"
]

# instantiate the arxiv api
arxiv = arxivApi()
# instantuate the gpt client
gpt = freeplayGPT()


article_summaries = []
for topic in search_topics:
    # get the articles
    articles = arxiv.search_keywords(topic, num_results=500, minDate=minDate, maxDate=maxDate)
    # pick the best article
    # limit to no more than 15 articles for sake of context window
    if len(articles) == 15:
        articles = articles[:15]
    try:
        best_article = gpt.pick_best_article(topic, articles)
    except Exception as e:
        print(f"An error occurred picking best article for {topic}: {str(e)}")
        continue
    # summarize the article
    try:
        full_text = arxiv.get_full_article_text(best_article.link)
        article_summary = gpt.summarize_article(full_text)
        print(f"Article summary for {best_article.title}: {article_summary}")
    except Exception as e:
        print(f"An error occurred summarizing article for {best_article}: {str(e)}")
        continue

    # add the article summary to the list
    article_summaries.append(ArticleSummary(
        title=best_article.title,
        summary=article_summary,
        link=best_article.link
    ))

# generate the html
html = gpt.generate_article_summary_html(article_summaries)

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
html_file_path = os.path.join(root_dir, "top_articles.html")

# add font matter to the html
html_content = '''---
layout: default
---
<style>
    body {
        zoom: 125%; /* Adjust the zoom level as per your requirement */
    }
</style>
''' + html

with open(html_file_path, "w") as f:
    f.write(html_content)

