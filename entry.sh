#!/bin/sh
# Import your cron file
/usr/bin/crontab /etc/codezinger-scraper.d/crontab.txt
# Start cron
/usr/sbin/crond -f -L /dev/stdout
