FROM python:3.9
ARG file 
COPY src/* /
ADD ./$file / 
RUN pip install --upgrade pip \ 
        && pip install -r requirements.txt

CMD [ "python", "./main.py" ]   