from python:3.8-slim-buster

ADD requirements.txt /
RUN pip3 install -r requirements.txt

ADD neuralLogAnalysis.py /
ADD ThunderbirdLog.txt /

CMD [ "python", "./neuralLogAnalysis.py"]
