FROM python

RUN mkdir /service
COPY ./  /service/

WORKDIR /service

RUN pip install -r requirements.txt

EXPOSE 50056
ENTRYPOINT [ "python", "sentiment-analysis.py"]