FROM python:3.10.2-alpine3.15

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install tzdata
RUN apk upgrade --no-cache \
    && apk add --no-cache tzdata \
    && rm -rf /var/cache/apk/*

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Install pyppeteer chromium
RUN pyppeteer-install

VOLUME /etc/codezinger-scraper.d

# copy project files
WORKDIR /app
COPY . .

COPY entry.sh /entry.sh
RUN chmod 755 /entry.sh
CMD ["/entry.sh"]
