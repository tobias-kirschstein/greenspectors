from typing import Tuple
import flair

from greenspectors.models.sentiment_analysis import SentimentAnalyzer, Sentiment


class FlairSentimentAnalyzer(SentimentAnalyzer):

    def __init__(self):
        self._model = flair.models.TextClassifier.load('en-sentiment')

    def predict(self, text: str) -> Tuple[Sentiment, float]:
        s = flair.data.Sentence(text)
        self._model.predict(s)
        total_sentiment = s.labels

        sentiment = self.parse_flair_sentiment(total_sentiment[0].value)
        score = total_sentiment[0].score

        if sentiment == Sentiment.NEGATIVE:
            score = -score

        return sentiment, score

    @staticmethod
    def parse_flair_sentiment(flair_sentiment: str) -> Sentiment:
        if flair_sentiment == 'POSITIVE':
            return Sentiment.POSITIVE
        elif flair_sentiment == 'NEGATIVE':
            return Sentiment.NEGATIVE
        else:
            raise ValueError(f"Flair Sentiment {flair_sentiment} not implemented")
