#!/bin/sh
# Import your cron file
/usr/bin/crontab /etc/codezinger-bot.d/jobs
# Start cron
/usr/sbin/crond -f -L /dev/stdout
