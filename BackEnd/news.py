from typing import Any

from BackEnd.constants import AlphaVantage
from BackEnd.helpers import get_raw_data


class News:

    def __init__(self, ticker: str, endpoint: str):
        self.ticker = ticker
        self.endpoint = endpoint

    @classmethod
    def get_most_relevant_article(cls, feed: list[dict[str, Any]], ticker: str):
        """
        Gets the most recent article that has the ticker or company name in the title

        Args:
            feed (list[dict[str, Any]]): list of news articles
            ticker (str): ticker of the stock
        Returns:
            url of the most relevant article
        """
        most_relevant_article: str = ""
        for article in feed:
            if ticker in article.get("title"):
                most_relevant_article = article.get("url")
        return most_relevant_article

    @property
    def get_news(self):
        """
        Returns:
            article (str): url of the article
        """
        raw_news_data = get_raw_data(endpoint=self.endpoint)
        feed = raw_news_data.get(AlphaVantage.feed)
        sorted_articles_latest = feed[::-1]
        article = News.get_most_relevant_article(feed=sorted_articles_latest, ticker=self.ticker)
        return article
