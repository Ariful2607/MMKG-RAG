import re

class TextCleaner:
    @staticmethod
    def clean(text: str) -> str:
        # remove emails
        text = re.sub(r"\S+@\S+", "", text)

        # remove URLs
        text = re.sub(r"http\S+", "", text)

        # remove page numbers
        text = re.sub(r"\b\d{4,6}\b", "", text)

        # normalize spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()