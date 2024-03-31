# -*- coding: utf-8 -*-

# This simple app uses the '/detect' resource to identify the language of
# the provided text or texts.

import os, requests, uuid, json

resource_key = str(os.getenv("TRANSLATOR_TEXT_SUBSCRIPTION_KEY"))
region = "centralindia"

endpoint = "https://api.cognitive.microsofttranslator.com"

# If you encounter any issues with the base_url or path, make sure
# that you are using the latest endpoint: https://docs.microsoft.com/azure/cognitive-services/translator/reference/v3-0-detect
path = "/detect?api-version=3.0"
constructed_url = endpoint + path

headers = {
    "Ocp-Apim-Subscription-Key": resource_key,
    "Ocp-Apim-Subscription-Region": region,
    "Content-type": "application/json",
    "X-ClientTraceId": str(uuid.uuid4()),
}


def detectLang(text):
    # You can pass more than one object in body.
    body = [{"text": text}]
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()

    print(
        json.dumps(
            response,
            sort_keys=True,
            indent=4,
            ensure_ascii=False,
            separators=(",", ": "),
        )
    )

    return response[0]["language"]


if __name__ == "__main__":
    print(detectLang("Salve, mondo!"))
