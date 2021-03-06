#!/usr/bin/env python3

import discord
from discord.ext import commands
from discord.ext.commands import dm_only
from discord.ext.commands import Bot
from discord.ext.tasks import loop
from db import UserHandler, EntryHandler
import validators
import time
from helpers.genpass import pass_generator
from helpers.utils import *
from errors import *
from text import bot_description, help_messages
from config import *

# Global variables

# stores master passwords and last time active of logged in users (uid is the key)
users = dict()
# bot client
client = Bot(
    command_prefix=commands.when_mentioned_or('!'),
    description="Astro - The Password Manager Bot",
    help_command=commands.DefaultHelpCommand(
        no_category="Commands"
    )
)

# Check decorators

# checks whether user is logged in
def logged_in():
    def predicate(ctx):
        if ctx.author.id not in users:
            raise AuthFailure("Not logged in")
        return True
    return commands.check(predicate)

# checks whether user is logged out
def logged_out():
    def predicate(ctx):
        if ctx.author.id in users:
            raise AuthFailure("Already logged in")
        return True
    return commands.check(predicate)

# Commands

@client.command(name="astro", help=help_messages["astro"])
async def astro(ctx):
    embed = discord.Embed(
        title="Astro - The Password Manager Bot",
        description=bot_description,
        colour=discord.Colour.teal()
    ).add_field(
        name=":information_source: Usage",
        value="Do !help in a DM for usage",
        inline=False
    ).set_thumbnail(url=f"{client.user.avatar_url}")

    await ctx.send(embed=embed)

@client.command(
    name="login",
    help=help_messages["login"]
)
@dm_only()
@logged_out()
async def login(ctx, masterpass: str):
    creds = UserHandler.get(ctx.author.id)
    if creds is None:
        raise AuthFailure("User doesn't exist! Register first")
    if valid_password(masterpass, creds["masterpass"]):
        users[ctx.author.id] = {
            "masterpass": masterpass
        }
        await ctx.send(":white_check_mark: Login successful")
    else:
        raise AuthFailure("Wrong credentials")

@client.command(
    name="register",
    help=help_messages["register"]
)
@dm_only()
@logged_out()
async def register(ctx, masterpass: str):
    if len(masterpass) < MIN_LENGTH:
        raise AuthFailure("Password is too short")

    registered = UserHandler.add(ctx.author.id, ctx.author.name, hash_password(masterpass))
    if registered :
        await ctx.send(":white_check_mark: Registration successful")
        await login(ctx, masterpass)
    else:
        raise AuthFailure("User already registered")

@client.command(
    name="logout",
    help=help_messages["logout"]
)
@dm_only()
@logged_in()
async def logout(ctx):
    users.pop(ctx.author.id)
    await ctx.send(":white_check_mark: Logout successful")

@client.command(
    name="view",
    aliases=["v"],
    help=help_messages["view"]
)
@dm_only()
@logged_in()
async def view(ctx, url: str=None):
    masterpass = get_password(users, ctx.author.id)
    if url is not None:
        data = EntryHandler.get(ctx.author.id, url)
        if data is not None:
            username = decrypt(data["username"], masterpass)
            password = decrypt(data["password"], masterpass)

            await ctx.send(embed=discord.Embed(
                title=f":white_check_mark: {url}",
                colour=discord.Colour.teal(),
            ).add_field(
                name="username",
                value=username,
                inline=False
            ).add_field(
                name="password",
                value=password,
                inline=False
            ))
        else:
            await ctx.send(f":x: No credentials found for <{url}>")
    else: # get all entries
        data = EntryHandler.getall(ctx.author.id)
        if len(data) > 0 :
            for d in data :
                username = decrypt(d["username"], masterpass)
                password = decrypt(d["password"], masterpass)

                await ctx.send(embed=discord.Embed(
                    title=f":white_check_mark: {d['url']}",
                    colour=discord.Colour.teal(),
                ).add_field(
                    name="username",
                    value=username,
                    inline=False
                ).add_field(
                    name="password",
                    value=password,
                    inline=False
                ))
        else:
            await ctx.send(":x: No credentials stored")

@client.command(
    name="add",
    aliases=["a"],
    help=help_messages["add"]
)
@dm_only()
@logged_in()
async def add(ctx, url: str, username: str, password: str=None):
    if not validators.url(url):
        await ctx.send(":x: Not a valid URL")
        return

    if not password:
        password = pass_generator()

    masterpass = get_password(users, ctx.author.id)
    enc_username = encrypt(username, masterpass)
    enc_password = encrypt(password, masterpass)

    added = EntryHandler.add(
        ctx.author.id,
        url,
        enc_username,
        enc_password
    )
    if added:
        await ctx.send(f":white_check_mark: Credentials added for <{url}>")
    else:
        await ctx.send(":x: Entry already exists")

@client.command(
    name="update",
    aliases=["u"],
    help=help_messages["update"]
)
@dm_only()
@logged_in()
async def update(ctx, url: str, username: str, password: str):
    masterpass = get_password(users, ctx.author.id)
    enc_username = encrypt(username, masterpass)
    enc_password = encrypt(password, masterpass)

    updated = EntryHandler.update(
        ctx.author.id,
        url,
        enc_username,
        enc_password
    )
    if updated:
        await ctx.send(f":white_check_mark: Credentials updated for <{url}>")
    else:
        await ctx.send(":x: Entry doesn't exist")

@client.command(
    name="delete",
    aliases=["d"],
    help=help_messages["delete"]
)
@dm_only()
@logged_in()
async def delete(ctx, url: str):
    deleted = EntryHandler.delete(ctx.author.id, url)
    if deleted:
        await ctx.send(f":white_check_mark: Credentials deleted for <{url}>")
    else:
        await ctx.send(":x: This URL doesn't exist")

@client.command(
    name="change",
    help=help_messages["change"]
)
@dm_only()
@logged_in()
async def change(ctx, masterpass: str):
    uid = ctx.author.id
    if len(masterpass) < MIN_LENGTH:
        raise AuthFailure("Password is too short")

    changed = UserHandler.update(ctx.author.id, ctx.author.name, hash_password(masterpass))
    if changed :
        await ctx.send(":white_check_mark: Master password changed successfully")
        users[uid]["masterpass"] = masterpass

# Loops for background tasks

# logout inactive users after timeout
@loop(minutes=INACTIVE_TIMEOUT)
async def logout_inactive():
    for uid in list(users):
        if time.time() - users[uid]["lastactive"] > INACTIVE_TIMEOUT:
            users.pop(uid)
            await client.get_user(uid).send(":timer: Logged out due to inactivity")

# Events

@client.event
async def on_ready():
    for guild in client.guilds:
        print(f"[+] {client.user} connected to {guild}")
    await client.change_presence(activity=discord.Game(name="!astro"))

@client.listen("on_message")
async def update_lastactive(message):
    uid = message.author.id
    if not isinstance(message.channel, discord.DMChannel):
        return
    if uid in users:
        users[uid]["lastactive"] = time.time()

@client.event
async def on_command_error(ctx, err):
    await error_handler(ctx, err)

if __name__ == "__main__":
    logout_inactive.start()
    client.run(TOKEN)
