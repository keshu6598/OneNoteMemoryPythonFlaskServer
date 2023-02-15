import os
import openai

openai.api_key = "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"


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

@app.route('/image', methods=['POST'])
def hello():
    request_body = request.get_json()
    prompt = request_body['text']
    response = openai.Image.create(prompt=prompt, n=1, size="512x512")
    image_url = response['data'][0]['url']
    data = {
        "imageUrl" : image_url
    }
    return jsonify(data)

# @app.route('/hello', methods=['POST'])
# def hello():
#    name = request.form.get('name')

#    if name:
#        print('Request for hello page received with name=%s' % name)
#        return render_template('hello.html', name = name)
#    else:
#        print('Request for hello page received with no name or blank name -- redirecting')
#        return redirect(url_for('index'))

if __name__ == '__main__':
   app.run()