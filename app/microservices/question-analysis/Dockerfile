FROM python

WORKDIR /app

COPY ./  /app/


RUN pip install -r requirements.txt

EXPOSE 50055
ENTRYPOINT [ "python", "app.py"]