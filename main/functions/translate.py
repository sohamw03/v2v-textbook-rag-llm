import requests, uuid, json, os

# Add your key and endpoint
key = str(os.getenv("TRANSLATOR_TEXT_SUBSCRIPTION_KEY"))
endpoint = "https://api.cognitive.microsofttranslator.com"

# location, also known as region.
# required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
location = "centralindia"

path = "/translate"
constructed_url = endpoint + path


def translate(from_language, to_language, text):
    params = {
        "api-version": "3.0",
        "from": from_language,
        "to": [to_language],
    }

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        # location required if you're using a multi-service or regional (not global) resource.
        "Ocp-Apim-Subscription-Region": location,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    # You can pass more than one object in body.
    body = [{"text": text}]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    print(
        json.dumps(
            response,
            sort_keys=True,
            ensure_ascii=False,
            indent=4,
            separators=(",", ": "),
        )
    )

    return response[0]["translations"][0]["text"]


if __name__ == "__main__":
    translate("en", "hi", "Hello, how are you doing today?")
