from abc import abstractmethod

from enum import Enum, auto
from typing import Tuple


class Sentiment(Enum):
    POSITIVE = auto()
    NEUTRAL = auto()
    NEGATIVE = auto()


class SentimentAnalyzer:

    @abstractmethod
    def predict(self, text: str) -> Tuple[Sentiment, float]:
        """
        Parameters
        ----------
            text:
                the snippet for which sentiment should be analyzed

        Returns
        -------
            - sentiment
            - score: [-1, 1]
        """

        pass
