from news import newsApi
from gpt import freeplayGPT
import datetime

gpt = freeplayGPT()

news = newsApi()
keywords = "Artificial Intelligence"
num_results = 10
maxDate = datetime.datetime.now()
minDate = maxDate - datetime.timedelta(days=7)
res = news.search_keywords(keywords, num_results, minDate, maxDate)
#print(res)
#print("/n/n/")
print(f"Number of articles: {len(res)}")
print("\n\n")

best_articles = gpt.select_best_stories(res, 3)
print([article.title for article in best_articles])
print("\n\n")

articleSet = []
for article in best_articles:
    summary = gpt.summarize_story(article)
    print(article.title)
    print(summary.summary)
    print("\n\n")
    articleSet.append(summary)

html = gpt.gen_html(articleSet)
with open("news.html", "w") as f:
    f.write(html)