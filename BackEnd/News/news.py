from typing import Any
from datetime import datetime

from BackEnd.Data.helpers import get_raw_data
from BackEnd.constants import AlphaVantage

class ArticleKeys:
    title="title"
    url="url"
    publish_date="time_published"


class News:

    def __init__(self, ticker: str, endpoint: str):
        self.ticker = ticker
        self.endpoint = endpoint

    @classmethod
    def get_most_relevant_article(cls, feed: list[dict[str, Any]], ticker: str) -> list[dict[str, Any]]:
        """
        Gets the most recent article that has the ticker or company name in the title

        Args:
            feed (list[dict[str, Any]]): list of news articles
            ticker (str): ticker of the stock
        Returns:
            most_relevant_articles (list[dict[str, Any]]: List of article metadata
        """
        most_relevant_articles = []

        # appends articles where ticker is in title with a limit of 10
        for article in feed:
            if ticker in article.get(ArticleKeys.title) and len(most_relevant_articles) <= 10:
                article_meta_data = {
                    "title": article.get(ArticleKeys.title),
                    "url": article.get(ArticleKeys.url),
                    "publish_date": datetime.strptime(article.get(ArticleKeys.publish_date), '%Y%m%dT%H%M%S')
                }
                most_relevant_articles.append(article_meta_data)

        # appends articles if space left of list
        if len(most_relevant_articles) < 11:
            for article in feed:
                article_meta_data = {
                    "title": article.get(ArticleKeys.title),
                    "url": article.get(ArticleKeys.url),
                    "publish_date": datetime.strptime(article.get(ArticleKeys.publish_date), '%Y%m%dT%H%M%S')
                }
                if article_meta_data not in most_relevant_articles:
                    most_relevant_articles.append(article_meta_data)

        return most_relevant_articles

    @property
    def get_news(self) -> list[dict[str, Any]]:
        """
        Returns:
            articles (list[dict[str, Any]]): List of articles metadata
        """
        raw_news_data = get_raw_data(endpoint=self.endpoint)
        feed = raw_news_data.get(AlphaVantage.feed)
        articles = News.get_most_relevant_article(feed=feed, ticker=self.ticker)
        return articles
