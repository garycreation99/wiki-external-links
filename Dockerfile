FROM python:3.6.4-alpine
RUN pip install tldextract
WORKDIR /app
COPY ./app /app
COPY wiki-links.input /app
VOLUME /app
CMD ["python", "./main.py"]
