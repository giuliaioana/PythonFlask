FROM python:3.9
ARG file 
COPY src/* /
COPY test-reports/* / 
ADD ./$file / 
RUN pip install --upgrade pip \ 
        && pip install -r requirements.txt && pip install pika

CMD [ "python", "./main.py" ]   