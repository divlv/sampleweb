FROM python:3.9-alpine

COPY ./www/ /app/
COPY ./requirements.txt /app/requirements.txt

# "-p" - create all chain with parent dirs, if any
RUN mkdir -p /cache
WORKDIR /app

# Left application in Development mode for now
# RUN sed -i "s/^\([[:space:]]*\)app.run/\n\1# Docker Build says: GUnicorn will start APP by itself:\n\1# app.run/g" /app/index.py

RUN pip install -r requirements.txt
CMD ["python3", "index.py"]
