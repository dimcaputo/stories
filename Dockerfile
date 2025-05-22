FROM python:3.11-bookworm

COPY requirements.txt ./
COPY templates/ /templates/
COPY app.py .

RUN mkdir static
RUN mkdir static/stories
RUN mkdir static/uploads

RUN curl -fsSL https://ollama.com/install.sh | sh
RUN pip install ollama flask flask_executor pillow

EXPOSE 5000

CMD ['ollama', 'serve']
CMD ["/bin/sh"]
CMD ["ollama", "pull llama3.2"]
CMD ["/bin/sh"]
CMD ["python", "app.py"]



