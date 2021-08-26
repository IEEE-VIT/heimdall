#!/usr/bin/env python3
import configparser
import os
import discord
from discord.ext import commands
import db

config = configparser.ConfigParser()
config.read('rooster.conf')
try:
    setup = config['ROOSTER']['SETUP']
except KeyError:
    print("Bot not setup. Please run setup-bot.py")
    exit(0)
db = db.Database.choose()
client = discord.Client()
try:
    prefix = config['ROOSTER']['BOT_PREFIX']
    prefix = prefix[:prefix.index('$')]
except Exception as e:
    print("Invalid Bot Prefix. Please re-run setup-bot.py")
    exit(0)
bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")
def get_linked_roles():
    data = db.fetchone(['invite_code','role_linked'])
    if(data):
        return data
    return "None"


async def is_valid_invite(ctx, code):
    for invite in await ctx.guild.invites():
        if(invite.code == code):
            return [True,invite.uses]
    return [False]


async def is_valid_role(roles, input):
    print(roles, input)
    roles_parsed = [role.id for role in roles]
    print(roles_parsed)
    if(int(input) in roles_parsed):
        return True
    return False


def add_role(inviteLink, role, uses):
    data = {"invite_code": inviteLink, "uses": uses,"role_linked": role.name, "role_id": role.id}
    if(db.insert(data)):
        return True
    return False


def remove_role(role):
    if(db.delete({'role_linked':role.name})):
        return True
    return False

@bot.event
async def on_ready():
    print('Bot logged in as {0.user}'.format(bot))

@bot.command()
async def hello(ctx):
    await ctx.send("Hey There! I am alive")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Prooster Bot",url="http://github.com/IEEE-VIT/palette-prooster",description="Prooster helps you manage invites and link them to Roles, by which you can assign the roles to members when they join with the invite.", color=discord.Color.blue())
    embed.add_field(name="Help", value=f"`{prefix}help`: Shows this message.",inline=False)
    embed.add_field(name="Invites", 
    value=f'''`{prefix}invites show [optional: page-number]`: Shows the details of the invites on the Server, and the roles attached to them.\n
    `{prefix}invites link [@role] [invite-code]`: Links the invite with the role given.\n
    `{prefix}invites unlink [@role]`: Unlinks the invite from the given role.\n
    `{prefix}invites create [channel-id]`: The bot creates an invite.''',inline=True)
    embed.add_field(name="Ping", value=f'`{prefix}hello`: Just to check if the bot is up.\n',inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def invites(ctx, *args):
    if (args[0].startswith("show")):
        stringGenerator = "Invites of this server are: \n"
        page = int(args[1]) if len(args)>1 else 1
        invites = await ctx.guild.invites() 
        nInvites = len(invites)
        nPages  = nInvites//8 + 1
        if(page>nPages or page<1):
            await ctx.send("Ahem. That page doesn't exist, human. ಠ_ಠ")
            return
        start = 8*(page-1)
        end = nInvites if 8*page>nInvites else 8*page
        linked_roles = get_linked_roles()
        for i in range(start, end):
            invite = invites[i]
            stringGenerator += "```{}. Invite Code: {}\nInvite Uses: {}\nCreated By: {}\nChannel: {}\nMax Uses: {}\nRole Attached: {}\n\n```".format(
                str(i+1), invite.code, invite.uses, invite.inviter, invite.channel, invite.max_uses, linked_roles.get(invite.code, "None"))
        stringGenerator += f"```Page {page} of {nPages}```"
        await ctx.send(stringGenerator)

    if (args[0].startswith("link")):
        role_input = int(args[1][3:-1])
        print(role_input)
        validRole = await is_valid_role(ctx.guild.roles, role_input)
        validInvite = await is_valid_invite(ctx, args[2])
        if(not validInvite[0] or not validRole):
            if(not validRole):
                await ctx.send("Invalid Role Entered")
            else:
                await ctx.send("Invalid Invite Code Entered")
        roles = ctx.guild.roles
        for role in roles:
            if(role.id == role_input):
                result = add_role(args[2], role, int(validInvite[1]))
                if(result):
                    await ctx.send("Sucessfully linked {} to {}".format(args[1], args[2]))
                else:
                    await ctx.send("FAILURE: Role already linked")

    if (args[0].startswith("unlink")):
        role_input = int(args[1][3:-1])
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


bot.run(config['ROOSTER']['BOT_TOKEN'])
bot.add_command(help)
bot.add_command(invites)
bot.add_command(hello)
