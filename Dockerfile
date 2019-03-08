FROM python:3.6-alpine

RUN pip install PyShEx

#WORKDIR /app
#COPY . .
#RUN pip install -r requirements.txt

ENTRYPOINT ["shexeval"]