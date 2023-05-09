import os
import openai
# from openai.embeddings_utils import get_embedding, cosine_similarity
openai.api_key = "OPENAI_TOKEN"
import requests
import base64
from requests_toolbelt.multipart import decoder

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# @app.route('/getEmbedding', methods=['POST'])
# def getEmbedding():
#     request_body = request.get_json()
#     text = request_body['text']
#     return jsonify(get_embedding(
#         text,
#         engine="text-embedding-ada-002"
    # ))

@app.route('/rephrase', methods=['POST'])
def rephrase():
    request_body = request.get_json()
    rephrase_text = request_body['text']
    prompt_text = "Hi ChatGPT, rephrase this text for me \' " + rephrase_text + " \' "
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt_text,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    print('Response from OpenAI: ', response)
    data = {
        "rephraseText" : response,
    }
    return jsonify(data)

@app.route('/askChatGPT', methods=['POST'])
def askChatGPT():
    request_body = request.get_json()
    rephrase_text = request_body['text']
    prompt_text = rephrase_text
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt_text,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    print('Response from OpenAI: ', response)
    data = {
        "rephraseText" : response,
    }
    return jsonify(data)

@app.route('/image', methods=['POST'])
def image():
    request_body = request.get_json()
    prompt = request_body['text']
    response = openai.Image.create(prompt=prompt, n=1, size="512x512")
    image_url = response['data'][0]['url']
    data = {
        "imageUrl" : image_url
    }
    return jsonify(data)

@app.route('/design', methods=['POST'])
def design():
    request_body = request.get_json()
    prompt = request_body['prompt']
    url = "https://designerapp.edog.officeapps.live.com/designerapp/suggestions.ashx"
    headers = {"Content-Type": "application/json", "caller": "DesignerApp"}
    designerRequest = {
        "ImageFiles": [],
        "Title": {
            "Text": ""
        },
        "SubTitle": {
            "Text": ""
        },
        "Expectations": {
            "Dimension": {
                "Width": 1080,
                "Height": 1080
            },
            "ExcludeDesignMetadata": [],
            "MaxCount": 10,
            "MinCount": 3,
            "TypeMetadata": [
                "png",
                "bmp",
                "jpg",
                "oxsd"
            ],
            "IsBrandKit": "false"
        },
        "Hints": {
            "Trigger": "DesignFromScratch",
            "EnableGetty3PImages": "true",
            "EnableGetty3PVideos": "true",
            "image2HeadingsForDFS": "true",
            "DesignQuery": prompt,
            "AllSizes": "false",
            "HasDalleImage": "false",
            "AllImagesAreDalleImages": "false"
        }
    }
    response = requests.post(url, json=designerRequest, headers=headers)
    multipart_data = decoder.MultipartDecoder.from_response(response)
    base64Images = []
    for part in multipart_data.parts:
        try:
            nested_multipart_data = decoder.MultipartDecoder(part.content,part.headers['Content-Type'.encode()].decode())
            base64Str = "data:image/jpeg;base64,"+str(base64.b64encode(nested_multipart_data.parts[1].content),'utf-8')
            base64Images.append(base64Str)
        except:
            pass
    data = {
        "success" : True,
        "images" : base64Images
    }
    return jsonify(data)

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

if __name__ == '__main__':
   app.run()