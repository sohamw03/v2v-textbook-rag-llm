from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .functions.loadData import loadData
from .functions.speechToText import speechToText
from .functions.initiateChatWithContext import initiateChatWithContext
from .functions.textToSpeech import textToSpeech
from .functions.detectLang import detectLang
from .functions.translate import translate
import base64


@csrf_exempt
def test(request):
    return HttpResponse("Success")


@csrf_exempt
def chat(request):
    if request.method == "POST":
        # Retrieve the audio file from the request
        audio_file = request.FILES.get("audio")

        # Process the audio file
        detectedText = speechToText(audio_file)
        print(detectedText)
        userLanguage = detectLang(detectedText)

        context = loadData()
        # Combine the detected text with the context and generate a response
        chatResponse = initiateChatWithContext(
            context=context, query=detectedText, userLanguage=userLanguage
        )

        # Process the chat response and convert it to audio
        userLangResponse = translate("en", userLanguage, chatResponse)
        outputAudio = textToSpeech(userLangResponse, userLanguage)

        # Return the output audio as a response
        # Convert the bytes data to base64 encoded string
        outputAudio_base64 = base64.b64encode(outputAudio).decode("utf-8")

        response = JsonResponse(
            {
                "detectedText": detectedText,
                "chatResponse": userLangResponse,
                "audio": outputAudio_base64,
            },
        )
        # Set the appropriate content type and headers for the audio file
        # You may need to adjust the content type and headers based on the actual audio format you are using

        return response

    else:
        # Handle GET requests or other HTTP methods
        return JsonResponse({"message": "This endpoint only supports POST requests."})
