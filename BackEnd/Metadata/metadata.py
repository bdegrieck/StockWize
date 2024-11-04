from random import choice
from datetime import datetime, timedelta

class StockWizeMetadata:

    def __init__(self):
        """
        I'm using a hardcoded list here and nobody can stop me
        """

        self.stock_market_facts = [
            f"The Amsterdam Stock Exchange, established in 1602 by the Dutch East India Company, is often regarded as the world's first official stock exchange.",
            f"Though the Dow Jones Industrial Average is one of the most famous market indices, it tracks only 30 major companies, not the entire stock market.",
            f"In 2008, Warren Buffett bet $1 million that an S&P 500 index fund would outperform a selection of hedge funds over 10 years. He won, proving passive investing often beats active management!",
            f"There's a superstition that stocks tend to perform worse on Friday the 13th. While there's no strong evidence to support it, it's a recurring market myth.",
            f"The 'Dogs of the Dow' strategy suggests investing in the 10 highest-dividend stocks of the Dow Jones each year. It's gained popularity for its simplicity and decent returns.",
            f"The VIX (Volatility Index) measures market volatility and is sometimes called the 'fear index' because it spikes during times of uncertainty, such as during a financial crisis.",
            f"On October 19, 1987, the stock market suffered its largest single-day percentage drop in history—22.6% on the Dow Jones. Known as 'Black Monday,' it led to significant reforms in market regulations.",
            f"To prevent extreme crashes, U.S. stock exchanges have 'circuit breakers' that temporarily halt trading if the market drops too quickly. This gives investors time to regroup and prevents panic selling.",
            f"While the terms 'bull' and 'bear' markets describe rising and falling trends, there's no specific threshold for them. Generally, a bull market rises 20% from its low, and a bear market drops 20% from its high.",
            f"'Penny stocks' are stocks that trade for under $5 per share. They're popular with speculators but are also highly volatile and risky.",
            f"Dividends, or payments to shareholders, play a huge role in stock returns over time. In fact, over the last century, nearly half of the total return on U.S. stocks came from reinvested dividends.",
            f"Robinhood popularized zero-commission trading in 2013, leading major brokerages like Charles Schwab and Fidelity to follow suit. This has made investing much more accessible to small investors.",
            f"Apple became the first U.S. company to reach a market capitalization of $1 trillion in 2018, a historic milestone that it surpassed by reaching $2 trillion in 2020.",
            f"On May 6, 2010, a 'flash crash' caused the U.S. stock market to plunge about 10% in minutes, only to recover shortly after. The event highlighted the risks of algorithmic trading and market instability.",
            f"Historically, the stock market tends to perform better in January, with investors believing it's due to holiday optimism, new year resolutions, and investment adjustments for tax purposes."
        ]

    def fun_fact(self):
        """
        Picks a random fun fact from the list above
        """
        return choice(self.stock_market_facts)
    
    def get_day_suffix(self, day):
        # Determine the suffix for the day
        if 11 <= day <= 13:  # Special case for 11th, 12th, 13th
            return "th"
        elif day % 10 == 1:
            return "st"
        elif day % 10 == 2:
            return "nd"
        elif day % 10 == 3:
            return "rd"
        else:
            return "th"

    def get_last_weekday(self):
        """
        Gets the previous weekday
        """

        date = datetime.now()  # Use current date if none is provided

        # Adjust date based on the current day of the week
        if date.weekday() == 6:  # Sunday
            last_weekday = date - timedelta(days=2)
        elif date.weekday() == 5:  # Saturday
            last_weekday = date - timedelta(days=1)
        else:  # Weekdays
            last_weekday = date - timedelta(days=1)

        # Format month name and day with suffix
        month = last_weekday.strftime("%B")
        day = last_weekday.day
        suffix = self.get_day_suffix(day)
        
        return f"{month} {day}{suffix}"