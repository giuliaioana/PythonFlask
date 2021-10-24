FROM python:3.9

COPY src/* /
RUN pip install --upgrade pip \ 
        && pip install -r requirements.txt


CMD [ "python", "./main.py" ]