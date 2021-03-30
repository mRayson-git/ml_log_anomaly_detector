from python:3.8-slim-buster

ADD requirements.txt /
RUN pip3 install -r requirements.txt

ADD app.py /
ADD extractor.py /
ADD https://zenodo.org/record/3227177/files/Thunderbird.tar.gz?download=1 /

RUN chmod 777 ./Thunderbird.log

CMD [ "python", "./extractor.py" ]

# CMD [ "python", "./app.py"]
