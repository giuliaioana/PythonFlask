FROM python:3.9
COPY * /
RUN pip install --upgrade pip \ 
        && pip install -r requirements.txt && pip install pika
CMD [ "python", "./app.py" ]   
