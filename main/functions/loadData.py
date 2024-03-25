import json


def loadData():
    # Load the JSON file
    with open("test-pg1-detected.json") as file:
        data = json.load(file)

    # Access and process the data
    # print(data)  # Print the entire parsed JSON data

    # Access specific elements (modify based on your JSON structure)
    detected_text = data["analyzeResult"]["content"]
    # print(detected_text)
    return detected_text


if __name__ == "__main__":
    print(loadData())
