import re


class TextCleaner:

    @staticmethod
    def clean(text: str):

        text = text.replace("　", " ")

        text = re.sub(r"\n+", "\n", text)

        text = re.sub(r"[ \t]+", " ", text)

        return text.strip()
