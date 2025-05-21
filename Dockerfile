FROM ubuntu:noble

COPY requirements.txt ./
COPY templates/ /templates/
COPY app.py .

RUN mkdir static
RUN mkdir static/stories
RUN mkdir static/uploads

RUN apt-get update
RUN apt-get install -y python3-pip curl software-properties-common
RUN pip install -r requirements.txt
RUN curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o ollama-linux-amd64.tgz
RUN tar -C /usr -xzf ollama-linux-amd64.tgz
RUN ollama pull qwen2.5vl:3b

EXPOSE 5000

# CMD ["/bin/sh"]
CMD ["python", "app.py"]



