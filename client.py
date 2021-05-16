#!/usr/bin/env python3
import discord
import json
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


async def inviteChecker(incoming_invite):
    with open("data.json", "r+") as f:
        data = json.load(f)
        for invite in data["data"]:
            if incoming_invite.code == invite["invite_code"]:
                if (incoming_invite.uses != invite["uses"]):
                    invite["uses"] = incoming_invite.uses
                    f.close()
                    with open("data.json", "w+") as g:
                        json.dump(data, g)
                    return invite["role_id"]
        return "none"


@client.event
async def on_member_join(member):
    print("Someone has joined the server!")
    roles = member.guild.roles
    invites = await member.guild.invites()
    for invite in invites:
        result = inviteChecker(invite)
        print("This is result", result)
        if(result != "none"):
            for role in roles:
                if(role.id == result):
                    await member.add_roles(role)


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    anc = client.get_channel(int("838453531585019934")
                             )  # announcements channel
    if(str(message.channel) == "announcement-commands"):
        if message.author == client.user:
            return
        msg = message.content
        if msg.startswith('*roost'):
            content = str(msg)[6:]
            await anc.send(content)
    # if(str(message.channel) == "general"):
    #     roles = message.guild.roles
    #     invites = await message.guild.invites()
    #     for invite in invites:
    #         result = await inviteChecker(invite)
    #         print("This is result", result)
    #         if(result != "none"):
    #             for role in roles:
    #                 if(role.id == result):
    #                     await message.author.add_roles(role)


client.run(os.getenv("BOT_TOKEN"))
