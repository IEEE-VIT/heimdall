#!/usr/bin/env python3
import discord
import configparser
import db
from discord import channel
from discord.ext import commands

config = configparser.ConfigParser()
config.read('heimdall.conf')
try:
    setup = config['HEIMDALL']['SETUP']
except KeyError:
    print("Bot not setup. Please run setup-bot.py")
    exit(0)
db = db.Database.choose()
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

def inviteChecker(incoming_invite, data):
    for invite in data:
        if incoming_invite.code == invite["invite_code"]:
            if (incoming_invite.uses != invite["uses"]):
                db.update({'uses':incoming_invite.uses}, {'invite_code':invite['invite_code']})
                return int(invite["role_id"])
    return "none"


@client.event
async def on_member_join(member):
    print("Someone has joined the server!")
    roles = member.guild.roles
    invites = await member.guild.invites()
    db_invites = db.fetchall()
    result = ''
    for invite in invites:
        result = inviteChecker(invite, db_invites)
        print("This is result", result)
        if(result != "none"):
            for role in roles:
                if(role.id == result):
                    await member.add_roles(role)


@client.event
async def on_ready():
    print('Client logged in as {0.user}'.format(client))


client.run(config['HEIMDALL']['BOT_TOKEN'])