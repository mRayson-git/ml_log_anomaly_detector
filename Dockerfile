from python:3.8-slim-buster

WORKDIR /code

ADD requirements.txt /code/requirements.txt
RUN pip3 install -r requirements.txt

ADD app.py /code/app.py
ADD extractor.py /code/extractor.py

RUN pwd
RUN ls -ail

ADD https://zenodo.org/record/3227177/files/Thunderbird.tar.gz?download=1 /code/Thunderbird.tar.gz

RUN chmod -R 777 ./

CMD [ "python", "./extractor.py" ]

CMD [ "python", "./app.py"]
