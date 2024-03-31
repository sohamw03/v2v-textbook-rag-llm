"""
  For more samples please visit https://github.com/Azure-Samples/cognitive-services-speech-sdk 
"""

import azure.cognitiveservices.speech as speechsdk
import os

# Creates an instance of a speech config with specified subscription key and service region.
speech_key = str(os.getenv("SPEECH_KEY"))
service_region = str(os.getenv("SPEECH_REGION"))

language_voice_mapping = {
    "en": "en-IN-PrabhatNeural",
    "hi": "hi-IN-MadhurNeural",
    "mr": "mr-IN-ManoharNeural",
    "ur": "ur-IN-SalmanNeural",
    "ta": "ta-IN-ValluvarNeural",
    "te": "te-IN-MohanNeural",
    "bn": "bn-IN-BashkarNeural",
}


def textToSpeech(text, userLanguage):
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )

    source_language = userLanguage
    voice_name = "hi-IN-MadhurNeural"
    if source_language in language_voice_mapping:
        voice_name = language_voice_mapping[source_language]
    print(voice_name)
    speech_config.speech_synthesis_voice_name = voice_name

    # Create a SpeechSynthesizer with the speech config and audio config
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=None,
    )

    result = speech_synthesizer.speak_text_async(text).get()
    audio_bytes = result.audio_data

    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
        return audio_bytes
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

    return None


if __name__ == "__main__":
    text = '"मॅटर" हा शब्द लॅटिन शब्द मटेरियलमधून आला आहे, ज्याचा मूळतः प्रकल्पासाठी गोळा केलेल्या लाकडाचा संदर्भ आहे. वस्तुमान आणि आकारमान असलेली किंवा जागा व्यापणारी कोणतीही गोष्ट अशी पदार्थाची व्याख्या केली जाते. उदाहरणार्थ, कार पदार्थापासून बनलेली असते कारण त्यात वस्तुमान आणि व्हॉल्यूम असते.'

    audio = textToSpeech(text, "mr")
    with open("output.wav", "wb") as f:
        f.write(audio)
    print("Audio file saved as output.wav")
