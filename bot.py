#!/usr/bin/env python3
import json
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import db

load_dotenv()

db = db.Database()
client = discord.Client()
bot = commands.Bot(command_prefix='gg ')

def role_finder(inviteLink):
    data = db.fetch()
    for invite_object in data:
        if(invite_object["invite_code"] == inviteLink):
            return invite_object["role_linked"]
    return "None"


async def is_valid_invite(ctx, code):
    for invite in await ctx.guild.invites():
        if(invite.code == code):
            return True
    return False


async def is_valid_role(roles, input):
    print(roles, input)
    roles_parsed = [role.id for role in roles]
    print(roles_parsed)
    if(int(input) in roles_parsed):
        return True
    return False


def add_role(inviteLink, role):
    data = db.fetch()
    for invite_object in data:
        if(invite_object["invite_code"] == inviteLink):
            return False
    data = {"invite_code": inviteLink, "uses": 0,"role_linked": role.name, "role_id": role.id}
    if(db.write(data)):
        return True
    return False


def remove_role(role):
    data = db.fetch()
    for i in range(len(data)):
        if data[i]["role_linked"] == role.name:
            if(db.write(data[i],delete=True)):
                return True
            return False


@bot.command()
async def hello(ctx):
    await ctx.send("Hey There! I am alive")

@bot.command()
async def invites(ctx, *args):
    if (args[0].startswith("show")):
        stringGenerator = "Invites of this server are: \n"
        page = int(args[1]) if len(args)>1 else 1
        invites = await ctx.guild.invites() 
        nInvites = len(invites)
        nPages  = nInvites//12 + 1
        if(page>nPages):
            await ctx.send("Ahem. That page doesn't exist, human. ಠ_ಠ")
            return
        start = 12*(page-1)
        end = nInvites if 12*page>nInvites else 12*page
        for i in range(start, end):
            invite = invites[i]
            stringGenerator += "```{}. Invite Code: {}\nInvite Uses: {}\nCreated By: {}\nChannel: {}\nMax Uses: {}\nRole Attached: {}\n\n```".format(
                str(i+1), invite.code, invite.uses, invite.inviter, invite.channel, invite.max_uses, role_finder(invite.code))
        stringGenerator += f"```Page {page} of {nPages}```"
        await ctx.send(stringGenerator)

    if (args[0].startswith("link")):
        role_input = int(args[1][3:-1])
        print(role_input)
        validRole = await is_valid_role(ctx.guild.roles, role_input)
        validInvite = await is_valid_invite(ctx, args[2])
        if(not validInvite or not validRole):
            if(not validRole):
                await ctx.send("Invalid Role Entered")
            else:
                await ctx.send("Invalid Invite Code Entered")
        roles = ctx.guild.roles
        for role in roles:
            if(role.id == role_input):
                result = add_role(args[2], role)
                if(result):
                    await ctx.send("Sucessfully linked {} to {}".format(args[1], args[2]))
                else:
                    await ctx.send("FAILURE: Role already linked")

    if (args[0].startswith("unlink")):
        role_input = args[1][3:-1]
        validRole = await is_valid_role(ctx.guild.roles, role_input)
        roles = ctx.guild.roles
        if(not validRole):
            await ctx.send("Invalid Role")
        for role in roles:
            if(role.id == role_input):
                result = remove_role(role)
                if(result):
                    await ctx.send("Sucessfully unlinked {}".format(args[1]))
                else:
                    await ctx.send("FAILURE: Role unable to unlink")

    if (args[0].startswith("create")):
        general_invite = ""
        try:
            channel_id = args[1]
            general_invite = bot.get_channel(int(channel_id))
        except:
            await ctx.send('Please provide a Channel ID.')
            return
        link = await general_invite.create_invite(reason=ctx.author.name + " Created a Global Invite")
        await ctx.send(link)


bot.run(os.getenv("BOT_TOKEN"))
bot.add_command(invites)
bot.add_command(hello)
