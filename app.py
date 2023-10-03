import requests
import json
import openai
from metaphor_python import Metaphor
from flask import Flask, render_template, request

app = Flask(__name__)
#put your apis key here
metaphor = Metaphor("")
openai.api_key = ""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ingredients = request.form["ingredients"]
        recipe, title, image_url = generate_recipe(ingredients)
        return render_template("index.html", recipe=recipe, title=title, image_url=image_url)
    return render_template("index.html")

def generate_recipe(ingredients):
    url = "https://api.metaphor.systems/search"

    payload = {
        "numResults": 3,
        "query": "Here is a recipe with:" + ingredients
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

    response = str(metaphor.get_contents(ids))

    recipe = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a cook that takes in a list of recipes (website content) from the user and outputs only one recipe that incorporates all of them, make sure it tastes good. output only a list of steps for one recipe that incorporates all of them. make sure it is as concise as possible. Make sure the recipe contains these ingredients: " + ingredients},
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

    image = openai.Image.create(
        prompt="picture of " + title,
        n=1,
        size="1024x1024"
    )
    image_url = image["data"][0]["url"]

    return recipe, title, image_url

if __name__ == "__main__":
    app.run(debug=True)
