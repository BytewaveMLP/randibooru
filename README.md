# randibooru

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

> Pulls random images from Derpibooru for your Discord server's enjoyment.

## Table of Contents

- [Install](#install)
    - [Prerequisites](#prerequisites)
    - [Instructions](#instructions)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [Contribute](#contribute)
- [License](#license)

## Install

### Prerequisites

- Python 3.5
- `pip`
- **OPTIONAL:** Knowledge of `virtualenv`

### Instructions

1. `$ git clone https://github.com/BytewaveMLP/randibooru`
2. **OPTIONAL:** Set up a `virtualenv` in `.env/`
3. `$ pip install -r requirements.txt`
4. `$ python3 randibooru.py`
5. `$ $EDITOR config.ini`

    Fill in your information for Derpibooru and Discord
    - Obtain a client ID and API key for Discord [here](https://discordapp.com/developers/applications/me)
    - Obtain a Derpibooru API key [here](https://derpibooru.org/users/edit)

6. **OPTIONAL:** Make any additional changes to your configuration file
7. `$ python3 randibooru.py`
8. Complete and use this link to invite your instance of Randibooru to a server: https://discordapp.com/oauth2/authorize?client_id=YOUR_CLIENT_ID_HERE&scope=bot&permissions=19456

    Alternatively, use the link generated in the console output of the bot.

If you don't want to set up Randibooru yourself, feel free to [invite the public version of Randibooru](https://discordapp.com/oauth2/authorize?client_id=206203876095950850&scope=bot&permissions=19456) to a server of your choice. Please do not overload the bot, however, as requests are **logged**. We **will** find you if you mess anything up!

## Usage

Just run the configured command in chat (`prefix + command`). By default, this is `!rb`. Randibooru should handle the rest for you.

## Maintainers

- [BytewaveMLP](https://github.com/BytewaveMLP)
- [antigravities](https://alexandra.moe/)

## Contribute

We accept PRs! If you have a change you'd like to submit to us, let us know! We'll consider adding it if we feel it's useful. We advise using a `virtualenv` set up in `.env/` to avoid polluting your global package space.

If you're reporting an issue, please make sure to follow the issue template provided. Also, consider checking our [Trello](https://trello.com/b/stNAQarK/randibooru) first to ensure the issue isn't already being worked on, and make sure to avoid double-posting issues. If it's already been reported, we promise we'll get to it eventually!

## License

Copyright (c) Eliot Partridge, 2016-17. Licensed under [the MIT License](/LICENSE).
