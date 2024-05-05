from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .functions.loadData import loadData
from .functions.speechToText import speechToText
from .functions.initiateChatWithContext import initiateChatWithContext
from .functions.textToSpeech import textToSpeech
from .functions.detectLang import detectLang
from .functions.translate import translate
from .functions.initiateChatLangchain import initiateChatLangchain
from .functions.initiateChatDictionaryLangchain import initiateChatDictionaryLangchain
import base64
from main.models import Chat, User


@csrf_exempt
def test(request):
    return HttpResponse("Success")


@csrf_exempt
def chatllm(request):
    if request.method == "POST":
        admin = ""
        try:
            admin = User.objects.get(name="admin")
        except User.DoesNotExist:
            admin = User(name="admin", mode="teacher mode")
            admin.save()
        mode = str(admin.mode)

        # Retrieve the audio file from the request
        audio_file = request.FILES.get("audio")
        # isNewSession = request.POST.get("isNewSession", 0)
        isNewSession = 0

        # Process the audio file
        detectedText = speechToText(audio_file)
        print(detectedText)

        # Check if the detected text contains any mode change commands
        if "dictionary mode" in detectedText.lower():
            mode = "dictionary mode"
            User.objects.filter(name="admin").update(mode="dictionary mode")
        elif "teacher mode" in detectedText.lower():
            mode = "teacher mode"
            User.objects.filter(name="admin").update(mode="teacher mode")

        # Detect the language of the detected text
        userLanguage = detectLang(detectedText)

        # Check the mode and initiate the chat accordingly
        chatResponse = ""
        if mode == "dictionary mode":
            chatResponse = initiateChatDictionaryLangchain(detectedText, userLanguage)
        elif mode == "teacher mode":
            chatResponse = initiateChatLangchain(
                detectedText, userLanguage, int(isNewSession)
            )

        # Translate the chat response to the user's language
        userLangResponse = ""
        outputAudio = b""
        # Check if the detected text contains any mode change commands
        if "dictionary mode" in detectedText.lower():
            outputAudio = textToSpeech("You're in dictionary mode now.", "en")
            userLangResponse = "You're in dictionary mode now."
        elif "teacher mode" in detectedText.lower():
            outputAudio = textToSpeech(
                "You're in teacher mode now. Please ask a question.", "en"
            )
            userLangResponse = "You're in teacher mode now. Please ask a question."
        else:
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


@csrf_exempt
def clearHistory(request):
    if request.method == "POST":
        Chat.objects.all().delete()
        return JsonResponse({"message": "Chat history cleared."})
