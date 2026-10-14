from enum import Enum

class VoiceType(str, Enum):
    CUSTOM = "custom"
    DEFAULT = "default"
    DYNAMIC = "dynamic"
    
    @property
    def display_name(self):
        mapping = {
            "CUSTOM": "커스텀",
            "DEFAULT": "기본",
            "DYNAMIC": "맞춤",
        }
        return mapping[self.name]
    
class VoiceProvider(str,Enum):
    GOOGLE = "google"
    ELEVENLABS = "elevenlabs"
    
class VoiceGender(str, Enum):
    NEUTRAL = "neutral"
    FEMALE = "female"
    MALE = "male"
    
    @property
    def display_name(self):
        mapping = {
            "NEUTRAL" : "중성",
            "FEMALE" : "여성",
            "MALE" : "남성",
        }
        return mapping[self.name]
    
class VoiceLanguage (str, Enum):
    KO = "ko-KR"
    EN = "en-US"
    JP = "ja-JP"
    CN = "zh-CN"

    
