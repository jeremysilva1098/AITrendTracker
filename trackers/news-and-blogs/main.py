from news import newsApi
from gpt import freeplayGPT
import datetime
import os

gpt = freeplayGPT()

news = newsApi()
keywords = "Artificial Intelligence"
num_results = 10
maxDate = datetime.datetime.now()
minDate = maxDate - datetime.timedelta(days=7)


if __name__ == "__main__":
    '''Find and create news summaries'''
    res = news.search_keywords(keywords, num_results, minDate, maxDate)
    #print(res)
    #print("/n/n/")
    print(f"Number of articles: {len(res)}")
    print("\n\n")

    best_articles = gpt.select_best_stories(res, 4)
    print("Best articles: ")
    print([article.title for article in best_articles])
    print("\n\n")

    articleSet = []
    for article in best_articles:
        summary = gpt.summarize_story(type='news', article=article)
        print(article.title)
        print(summary.summary)
        print("\n\n")
        articleSet.append(summary)

    html = gpt.gen_html(type='news', article_summaries=articleSet)

    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    html_file_path = os.path.join(root_dir, "news.html")

    with open(html_file_path, "w") as f:
        f.write(html)
    
    '''Find and create blog summaries'''
    blog_topics = ["LLM Blog Post", "Creating LLM Apps Blog Post",
                   "LLM Optimization or Fine Tuning Blog Post"]
    # get 5 articles on each topic
    all_posts = []
    for post in blog_topics:
        post_set = news.search_keywords(post, 7)
        all_posts.extend(post_set)
    print(f"Number of blog posts: {len(all_posts)}")
    # select the best posts
    best_posts = gpt.select_best_blog_posts(articles=all_posts, num_articles=4)
    print("Best posts: ")
    print([post.title for post in best_posts])
    print("\n\n")

    postSet = []
    for post in best_posts:
        summary = gpt.summarize_story(type='blog', article=post)
        print(post.title)
        print(summary.summary)
        print("\n\n")
        postSet.append(summary)
    
    html = gpt.gen_html(type='blog', article_summaries=postSet)

    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    html_file_path = os.path.join(root_dir, "blog.html")

    with open(html_file_path, "w") as f:
        f.write(html)