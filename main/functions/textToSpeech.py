"""
  For more samples please visit https://github.com/Azure-Samples/cognitive-services-speech-sdk 
"""

import azure.cognitiveservices.speech as speechsdk
import os

# Creates an instance of a speech config with specified subscription key and service region.
speech_key = str(os.getenv("SPEECH_KEY"))
service_region = str(os.getenv("SPEECH_REGION"))


def textToSpeech(text):
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )
    speech_config.speech_synthesis_voice_name = "en-IN-PrabhatNeural"

    # Create a SpeechSynthesizer with the speech config and audio config
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None
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
