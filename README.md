# codezinger-due-date-scraper ![](https://cdn.discordapp.com/emojis/861575999832719381.webp?size=48&quality=lossless)

This program allows you to scrape your codezinger questions that are due and
sends them to a discord channel via webhooks.

<sub>
(at the top it says ita a fork, but its not even a fork at this
point)
</sub>

## ⚠⚠ End Of Life notice
since my uni has moved away from using this platform, it wouldnt be possible for me to use or maintain this project.
This bot has been very helpful to me for the time it was running, and I learnt, played around with and implemented
alot of new things while making and maintaining it<3

Maybe look around for a same project in the future, adapted to the new platform being used by my uni?

## Features:

- Sends webhook messages sorted by due dates
- Keeps track if a question's due date has been updated
- Deletes messages for questions past their due dates
- Runs on-demand based on cron schedule

## Demo

https://user-images.githubusercontent.com/39442192/153704089-c81d4fc1-d313-41ca-812c-5996ac38ff43.mp4

## Usage

- Instead of cloning the repository, I suggest you download these 3 files in a
  folder (preferrably from the [release](https://github.com/RoguedBear/codezinger-due-date-scraper/releases/latest)
  page):

  - [`config.yml.EXAMPLE`](./config.yml.EXAMPLE)
  - [`docker-compose.yml`](./docker-compose.yml)
  - [`crontab.txt.EXAMPLE`](./crontab.txt.EXAMPLE) \
    (Rename `crontab.txt.EXAMPLE` to `crontab.txt`)

- Now you can customise the bot to your needs:

  - #### Creating a friendly name (that'll be used in discord) for your codezinger class

    - You can now change the mapping in `config.yml`
    - the `name` field in the `config.yml` is the full class name you see in
      codezinger
    - tip to find the full length class names with some effort: \
      run the bot without any mapping first, then the due date message it sends over
      on discord you'll see the the long name of your class in the message, you can
      use that to create the mapping as per the format in `config.yaml`

  - #### Set your cron schedule in `crontab.txt`
    - This schedule you define here is when the bot will trigger the python
      script to scrape the data.
    - I've set the my timings in my instance to be 5 minutes after my lab class
      starts, and 5-10 minutes after it ends on those days. You could for
      example schedule the bot to run daily at a convenient/inactive time like 3
      am.
    - lookup on the internet on how to define cron schedules if you're new to
      that and/or refer mine in [`crontab.txt.EXAMPLE`](./crontab.txt.EXAMPLE).

- Since you also need to specify your webhook url, your codezinger email &
  password, you need to create 3 files in a new folder `secrets/`

  - **`secrets/webhook_url.txt`**: this file will contain your discord webhook
    **in a single line**
  - **`secrets/email.txt`**: this file will contain your email **in a single
    line**. example:
    ```txt
    e20cse215@bennett.edu.in
    ```
  - **`secrets/password.txt`**: this file will contain your password **in a
    single line**

- now create an empty database file so docker compose can mount it:
  ```bash
  touch db.db
  ```
- Run the compose file: `docker-compose up -d`
- now if you want, you can either delete the `secrets/` folder or change
  permissions of that folder to read-only for your user (or remove even that
  also)
  ```bash
  chmod -R 400 secrets/ # for read-only to your user
  chmod -R 000 secrets/ # experimental security
  ```
  NOTE: if you delete your secrets folder and need to update anything in the
  `docker-compose.yml` file, you'd have to run `docker-compose up -d` again
  which _could_ require the `secrets/` folder to be accessible again.

## License

This project is licensed under GNU GPLv3
