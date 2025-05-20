from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import ollama
from PIL import Image

app = Flask(__name__)

app.config['UPLOAD'] = 'static/uploads'

img_path = 'static/uploads'
story_path = 'static/stories'

@app.route("/", methods=['GET','POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files['img']
        h = Image.open(file.stream).height
        w = Image.open(file.stream).height
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)

        with open(os.path.join(img_path, filename), 'rb') as f:
            response = ollama.chat(
                model='gemma3:4b',
                messages=[
                    {
                    'role': 'user',
                    'content': 'Tell me a short story about this image. Make it 10 sentences.',
                    'images': [f.read()],
                    },
                ],
            )
            story = response['message']['content']
        with open(os.path.join(story_path, filename), 'w') as s:
            s.write(story)
        return render_template('index.html', img=img, story=story)
    return render_template('index.html')

@app.route("/gallery.html", methods=['GET'])
def display_image():
    return render_template('gallery.html', image='static/uploads/donnie-rosie-zC9U86g73xg-unsplash.jpg')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5000)