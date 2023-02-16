import os
import openai

openai.api_key = "<api-key>"


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

@app.route('/openOneNoteApp')
def openOneNoteApp():
    redirect_url = request.args.get('ClientUrl')
    return redirect(redirect_url, code=302)

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