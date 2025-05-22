FROM python:3.11-bookworm

COPY requirements.txt .
COPY templates/ templates/
COPY app.py .

RUN mkdir static
RUN mkdir static/stories
RUN mkdir static/uploads

RUN apt update && apt upgrade
RUN pip install -r requirements.txt --break-system-packages

EXPOSE 5000

CMD ["python", "app.py"]



