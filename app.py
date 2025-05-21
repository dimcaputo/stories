from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import ollama
from PIL import Image
from flask_executor import Executor

app = Flask(__name__)

executor = Executor(app)

app.config['UPLOAD'] ='static/uploads'
stories_path = 'static/stories'
img_path = 'static/uploads'

@app.route("/", methods=['GET','POST'])
def upload_image():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        img = os.path.join(img_path, filename)
        file.save(img)
        url = url_for('startBackgroundStory', img=img, filename=filename)
        return redirect(url)

@app.route('/startBackgroundStory', methods=['GET', 'POST'])
def startBackgroundStory():
    img = request.args.get('img')
    filename = request.args.get('filename')
    executor.submit(backgroundStory, img, filename)
    return redirect(url_for('display_story', img=img, filename=filename))

@app.route('/writer', methods=['GET', 'POST'])
def backgroundStory(img, filename):
    with open(img, 'rb') as f:
        response = ollama.generate(
            model='qwen2.5vl:3b',
            prompt= "Write a short story about this image. Make it 10 sentences long",
            images= [f.read()],
            options={'num_thread':16}
        )
        story = response['response']
        story_path = filename.rstrip('jpg')+'txt'
    with open(os.path.join(stories_path, story_path), 'w') as s:
        s.write(story)
    return redirect(url_for('display_story', img=img, story=story))

@app.route('/display_story', methods=['GET', 'POST'])
def display_story():
    img = request.args.get('img')
    if not os.path.exists(img.rstrip('jpg')+'txt'):
        return redirect(url_for('display_story', img=img))
    story = request.args.get('story')
    return render_template('/story.html', img=img, story=story)
    


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5000)