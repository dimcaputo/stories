FROM python:3.11-bookworm

COPY requirements.txt ./
COPY templates/ /templates/
COPY app.py .

RUN mkdir static
RUN mkdir static/stories
RUN mkdir static/uploads

RUN curl -fsSL https://ollama.com/install.sh | sh
RUN pip install ollama flask flask_executor pillow
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ['python', 'app.py']


