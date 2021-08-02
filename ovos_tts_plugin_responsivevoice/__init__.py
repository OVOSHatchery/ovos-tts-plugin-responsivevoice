# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from ovos_plugin_manager.templates.tts import TTS, TTSValidator
from ovos_utils.log import LOG
import requests
from responsive_voice import ResponsiveVoice
from responsive_voice import get_voices


class ResponsiveVoiceTTSPlugin(TTS):
    """Interface to ResponsiveVoice TTS."""

    def __init__(self, lang="en-us", config=None):
        config = config or {"lang": lang,
                            "pitch": 0.5,
                            "rate": 0.5,
                            "vol": 1}
        super(ResponsiveVoiceTTSPlugin, self).__init__(
            lang, config, ResponsiveVoiceTTSValidator(self), 'mp3')
        self.pitch = config.get("pitch", 0.5)
        self.rate = config.get("rate", 0.5)
        self.vol = config.get("vol", 1)

        if self.voice:
            clazz = get_voices()[self.voice]
            self.engine = clazz(pitch=self.pitch, rate=self.rate, vol=self.vol)
        else:
            gender = config.get("gender", "male")
            self.engine = ResponsiveVoice(lang=self.lang, gender=gender,
                                          pitch=self.pitch, rate=self.rate,
                                          vol=self.vol)

    def get_tts(self, sentence, wav_file):
        """Fetch tts audio using ResponsiveVoice endpoint.

        Arguments:
            sentence (str): Sentence to generate audio for
            wav_file (str): output file path
        Returns:
            Tuple ((str) written file, None)
        """
        self.engine.get_mp3(sentence, wav_file)
        return (wav_file, None)  # No phonemes


class ResponsiveVoiceTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(ResponsiveVoiceTTSValidator, self).__init__(tts)

    def validate_lang(self):
        lang = self.tts.lang.lower()
        assert lang in self.get_lang_list()

    def validate_voice(self):
        if self.tts.voice is not None:
            assert self.tts.voice in get_voices()

    def validate_connection(self):
        r = requests.get("https://responsivevoice.org")
        if r.status_code == 200:
            return True
        LOG.warning("Could not reach https://responsivevoice.org")

    def get_tts_class(self):
        return ResponsiveVoiceTTSPlugin

    @staticmethod
    def get_lang_list():
        voice_clazzes = get_voices()
        langs = []
        for voice in voice_clazzes:
            lang = voice_clazzes[voice]().lang.split("_#")[0].lower().replace(
                "_", "-").replace("service", "sv")
            lang2 = lang.split("-")[0]
            if lang not in langs:
                langs.append(lang)
            if lang2 not in langs:
                langs.append(lang2)
            if lang == "ca-es":
                lang = "es-ca"
                lang2 = lang.split("-")[0]
                if lang not in langs:
                    langs.append(lang)
                if lang2 not in langs:
                    langs.append(lang2)
        return sorted(langs)


