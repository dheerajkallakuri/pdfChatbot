import language_tool_python
from pyaspeller import YandexSpeller
tool = language_tool_python.LanguageToolPublicAPI('en-US')

def get_grammarCheck(text):
    spellcheck = YandexSpeller().spelled(text)
    correctedText = tool.correct(spellcheck)
    return correctedText