import os
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import (
    PullAudioInputStreamCallback,
    PullAudioInputStream,
)
import os


SPEECH_KEY = str(os.getenv("SPEECH_KEY"))
SPEECH_REGION = str(os.getenv("SPEECH_REGION"))


def speechToText(audio_file):
    speech_config = speechsdk.SpeechConfig(
        subscription=SPEECH_KEY, region=SPEECH_REGION
    )
    speech_config.speech_recognition_language = "en-US"
    # auto_detect_source_language_config = (
    #     speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
    #         languages=["en-US", "mr-IN", "hi-IN"]
    #     )
    # )

    # Increase initial silence timeout to 5 seconds
    speech_config.set_property(
        speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, "10000"
    )

    # this example uses audio streams so there is no need to save the wav files in storage
    audio_stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.audio.AudioConfig(stream=audio_stream)

    # write audio data and then close the stream
    # closing the stream is needed if the audio is less than 15 seconds
    audio_stream.write(audio_file.read())
    audio_stream.close()

    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config,
        # auto_detect_source_language_config=auto_detect_source_language_config,
    )

    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print(
            "No speech could be recognized: {}".format(
                speech_recognition_result.no_match_details
            )
        )
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
    return ""
