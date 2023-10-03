import requests
import json
import openai
from metaphor_python import Metaphor
metaphor = Metaphor("")
openai.api_key = ""

url = "https://api.metaphor.systems/search"

ingredients = str(input("list ingredients separated with commas:"))

payload = {
    "numResults": 3,
    "query": "Here is a reecipe with:" + ingredients
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": ""
}

response = requests.post(url, json=payload, headers=headers)

JsonResponse = json.loads(response.text)

ids = []
for i in range(len(JsonResponse["results"])):
    ids.append(JsonResponse["results"][i]["id"])
#print(ids)

response = str(metaphor.get_contents(ids))

recipe = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a cook that takes in a list of recipes (website content) from the user and outputs only one recipe that incorporates all ingredients, make sure it tastes good. Output only a list of steps (numbered, one step per line) for the recipe. Make sure it is as concise as possible. Put every step of the recipe on a different new line. Make sure the recipe contains these ingredients: " + ingredients},
        {"role": "user", "content": response}
    ]
)
recipe = recipe['choices'][0]['message']['content']

title = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an assistant that takes in a recipe from the user and outputs an original and yummy title as concise as possible for that recipe "},
        {"role": "user", "content": recipe}
    ]
)

title = title['choices'][0]['message']['content']

image=openai.Image.create(
  prompt="picture of " + title,
  n=1,
  size="1024x1024"
)
image_url = image["data"][0]["url"]

