FROM python

RUN mkdir /service
COPY ./  /service/

WORKDIR /service

RUN pip install -r requirements.txt

EXPOSE 50053
ENTRYPOINT [ "python", "market-performance.py" ]