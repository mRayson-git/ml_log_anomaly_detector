from python:3.8-slim-buster

ADD requirements.txt /
RUN pip3 install -r requirements.txt

ADD app.py /
ADD https://zenodo.org/record/3227177/files/Thunderbird.tar.gz?download=1 ThunderbirdLog.txt

CMD [ "python", "./app.py"]
