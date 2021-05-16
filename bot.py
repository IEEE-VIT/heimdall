#!/usr/bin/env python3
import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()
bot = commands.Bot(command_prefix='gg ')


def role_finder(inviteLink):
    with open('data.json') as f:
        data = json.load(f)
        for invite_object in data["data"]:
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
    data = {}
    with open('data.json', "r+") as f:
        data = json.load(f)
        for invite_object in data["data"]:
            if(invite_object["invite_code"] == inviteLink):
                return False
        data["data"].append({"invite_code": inviteLink, "uses": 0,
                             "role_linked": role.name, "role_id": role.id})
        f.close()
    with open("data.json", "w+") as g:
        json.dump(data, g)
    return True


def remove_role(role):
    data = {}
    with open("data.json", "r+") as f:
        data = json.load(f)
        for i in range(len(data["data"])):
            if data["data"][i]["role_linked"] == role.name:
                data["data"].pop(i)
                break
        f.close()
    with open("data.json", "w+") as w:
        json.dump(data, w)
    return True


@bot.command()
async def invites(ctx, *args):
    if (args[0].startswith("show")):
        stringGenerator = "Invites of this server are: \n"
        index = 1
        for invite in await ctx.guild.invites():
            stringGenerator += "```{}. Invite Code: {}\nInvite Uses: {}\nCreated By: {}\nChannel: {}\nMax Uses: {}\nRole Attached: {}\n\n```".format(
                str(index), invite.code, invite.uses, invite.inviter, invite.channel, invite.max_uses, role_finder(invite.code))
            index += 1
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
        link = await ctx.channel.create_invite(reason=ctx.author.name + " Created a Global Invite")
        await ctx.send(link)


bot.run(os.getenv("BOT_TOKEN"))
bot.add_command(invites)
