# codezinger-due-date-scraper ![](https://cdn.discordapp.com/emojis/861575999832719381.webp?size=48&quality=lossless)

This program allows you to scrape your codezinger questions that are due and
sends them to a discord channel via webhooks.

<sub>
(at the top it says ita a fork, but its not even a fork at this
point)
</sub>

## Features:

- Sends webhook messages sorted by due dates
- Keeps track if a question's due date has been updated
- Deletes messages for questions past their due dates

## Usage

- Instead of cloning the repository, I suggest you download these 3 files in a
  folder:
  - [`config.yml.EXAMPLE`](./config.yml.EXAMPLE)
  - [`docker-compose.yml`](./docker-compose.yml)
  - [`crontab.txt.EXAMPLE`](./crontab.txt.EXAMPLE) \
    (Rename `crontab.txt.EXAMPLE` to `crontab.txt`)
- You can now change the mapping in `config.yml` or your cron schedule in
  `crontab.txt`
- Since you also need to specify your webhook url, your codezinger email &
  password, you need to create 3 files in a new folder `secrets/` created you
  have downloaded the above files

  - **`secrets/webhook_url.txt`**: this file will contain your discord webhook
    **in a single line**
  - **`secrets/email.txt`**: this file will contain your email **in a single
    line**. example:
    ```txt
    e20cse215@bennett.edu.in
    ```
  - **`secrets/password.txt`**: this file will contain your password **in a
    single line**

- Run the compose file: `docker-compose up -d`
- now if you want, you can either delete the `secrets/` folder or change
  permissions of that folder to read-only for your user (or remove even that
  also)
  ```bash
  chmod -R 400 secrets/ # for read-only to your user
  chmod -R 000 secrets/ # experimental security
  ```
  NOTE: if you delete your secrets folder and need to update something, you'd
  have to run `docker-compose up -d` again which _could_ require the secrets
  folder to be accessible again.

## License

This project is licensed under GNU GPLv3
