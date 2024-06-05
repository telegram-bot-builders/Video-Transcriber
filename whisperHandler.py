from openai import OpenAI
import os


# import messages

class Whisperer:

    def __init__(self, apiKey, lang='auto'):
        self.lang = lang
        self.apiKey = apiKey
        self.client = OpenAI(api_key=apiKey)


    async def setLang(self, lang):
        # If the language is auto, set it to empty
        if lang == 'auto':
            self.lang = ""
            return 0
        
        # If the language is not in the list, return 1
        # If the language is in the list, set it and return 0
        # for i in messages.LANGUAGES:
        #     if i == lang:
        #         self.lang = lang
        #         return 0
            
        return 1

    async def whisp(self, path):
        audio = open(path, "rb")

        transcription = self.client.audio.transcriptions.create(
                            model="whisper-1", 
                            file=audio
                        )

        return transcription.text # type: ignore