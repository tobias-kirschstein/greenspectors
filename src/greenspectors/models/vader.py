from typing import Tuple

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

from greenspectors.models.sentiment_analysis import SentimentAnalyzer, Sentiment


class VaderSentimentAnalyzer(SentimentAnalyzer):
    def __init__(self, sentiment_threshold: float = 0.5):
        nltk.download('vader_lexicon')
        self._model = SentimentIntensityAnalyzer()
        self._sentiment_threshold = sentiment_threshold

    def predict(self, text: str) -> Tuple[Sentiment, float]:
        polarity_scores = self._model.polarity_scores(text)
        compound_score = polarity_scores['compound']  # Between -1 and 1
        if compound_score < -self._sentiment_threshold:
            sentiment = Sentiment.NEGATIVE
        elif -self._sentiment_threshold <= compound_score < self._sentiment_threshold:
            sentiment = Sentiment.NEUTRAL
        else:
            sentiment = Sentiment.POSITIVE

        return sentiment, compound_score

    @staticmethod
    def parse_vader_sentiment(vader_sentiment: str) -> Sentiment:
        if vader_sentiment == 'pos':
            return Sentiment.POSITIVE
        elif vader_sentiment == 'neg':
            return Sentiment.NEGATIVE
        elif vader_sentiment == 'neu':
            return Sentiment.NEUTRAL
        else:
            raise ValueError(f"Vader Sentiment {vader_sentiment} not implemented")
