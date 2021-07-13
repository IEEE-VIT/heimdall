#!/usr/bin/env python3
import discord
import json
import os
import db
from discord import channel
from discord.ext import commands
from dotenv import load_dotenv

db = db.Database()
load_dotenv()
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

def inviteChecker(incoming_invite):
    data = db.fetch()
    for invite in data:
        if incoming_invite.code == invite["invite_code"]:
            if (incoming_invite.uses != invite["uses"]):
                invite["uses"] = incoming_invite.uses
                db.write(invite, update=True)
                return int(invite["role_id"])
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


client.run(os.getenv("BOT_TOKEN"))