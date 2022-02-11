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
# RUN pyppeteer-install
RUN apk -U add chromium udev ttf-freefont
ENV CHROME_PATH=/usr/bin/chromium-browser

VOLUME /etc/codezinger-bot.d/

# copy project files
WORKDIR /app
COPY . .

COPY entry.sh /entry.sh
COPY entrypoint.sh /entrypoint.sh
# Todo fix these permissions, though im not sure if this will even impact anything
RUN chmod 755 /entry.sh /entrypoint.sh
CMD ["/entry.sh"]
