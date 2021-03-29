from python:3.8

ADD neuralLogAnalysis.py /
ADD ThunderbirdLog.txt /

CMD [ "python", "./neuralLogAnalysis.py"]
