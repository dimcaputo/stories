from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from ollama import Client
from PIL import Image

app = Flask(__name__)

app.config['UPLOAD'] = 'static/uploads'

img_path = 'static/uploads'
story_path = 'static/stories'

@app.route("/", methods=['GET','POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        img = os.path.join(app.config['UPLOAD'], filename)
        file.save(img)
        
        with open(img, 'rb') as f:
            client = Client(
                host='http://ollama:11434',
            )
            response = client.chat(
                model='gemma3:4b', 
                messages=[
                    {
                        'role': 'user',
                        'content': 'Write a tiny story about this image. Always start your response with "Once upon a time".',
                        'images':[f.read()]
                    },
                ],
                options={'num_thread':os.cpu_count()}
            )

        story = response['message']['content']

        with open(os.path.join(story_path, filename.rstrip('jpg')+'txt'), 'w') as s:
            s.write(story)
        return render_template('index.html', img=img, story=story)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5000)