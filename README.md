# AITrendTracker
An AI powered trend tracker that curates and summarizes the latest research, news, and blogs in AI each week. Helping you keep up with the latest advancements.

[AI Trend Tracker Site](https://jeremysilva1098.github.io/AITrendTracker) - Updated Every Monday Morning!

All content curation and summarization is done via LLM. Even the HTML is entirely AI generated!

Prompt management, evaluation, and paramater optimization orchestrated via [freeplay.ai](https://freeplay.ai/)!

[freelay details here](/freeplay_samp_imgs/DEMO_OVERVIEW.md)

Implementation details on AI components found in [trackers](trackers/) folders

## How it works
### Research
* LLM currates a refined set of research articles from the past week via the [arxiv API](https://info.arxiv.org/help/api/index.html). The LLM selects the most relevant papers based on our interests.
* LLM summarizes each paper into a set of actionable insights for those building in the field
  
### News and Blogs
* LLM currates a refined set of news stories and blog posts from the last week via the [news API](https://newsapi.org/). The LLM selects stories which would be most interesting and impactful to folks working in the AI space
* LLM summarizes each story into a set of key insights
