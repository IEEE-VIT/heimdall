# Heimdall Bot ⚔️
Heimdall is a Discord Bot that can be used to manage the roles of the users based on an invite link to a server. It generates an invite link by its own, and can assign a role to the invite link. That particular role is assigned to the member that joins using that invite link.

## Installation Guidelines
Create an application and a bot using [the documentation](https://docs.discord.red/en/stable/bot_application_guide.html?highlight=application%20page#creating-the-bot-application). Make sure to enable the privileged intents through [this link](https://docs.discord.red/en/stable/bot_application_guide.html?highlight=application%20page#enabling-privileged-intents).

Administrator permissions are required for the bot, and make sure the bot is placed above every other roles you wish to give in the server.

### Without Docker
1. Install the requirements by running `pip install -r requirements.txt`
2. Run `python3 setup-bot.py`
3. Input the Bot Prefix and the Bot Token
4. Choose the database you wish to use from JSON, MySQL, SQLite3, PostgreSQL, MongoDB
5. Input the credentials for the database as and when required.
6. Run `python3 run-bot.py`
7. Voila! Your bot is running!

### With Docker
1. Run `python3 setup-bot.py`
2. Setup the bot as per the above steps 3-5
3. Run `docker build -t heimdall .` to build the docker image
4. Run the docker container using `docker run --detached=true heimdall`
5. Continue the above steps from step 3.

## Commands

![](https://cdn.discordapp.com/attachments/764032742106595341/880413851005378600/Screenshot_2021-08-26_at_5.00.14_PM.png)

## Features
* Generate Invite Links
* Connect Invite links with roles
* Detect member join and give role
* Multiple DB Capability - JSON, MySQL, PostgreSQL, MongoDB, SQLite3
* Auto setup DB with input credentials

## Contributing Guidelines

To start contributing, check out CONTRIBUTING.md. New contributors are always welcome to support this project. Kindly consider leaving a ⭐ if you like the project :)

## License

This project is under the [MIT](https://github.com/IEEE-VIT/heimdall/blob/master/LICENSE) License.