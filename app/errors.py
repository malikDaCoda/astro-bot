import discord
from discord.ext.commands import errors

# Custom exceptions

# for authentification failures
class AuthFailure(errors.CheckFailure):
    pass

# when token is not found
class TokenNotFound(Exception):
    pass

# Error handler

async def error_handler(ctx, err):
    if isinstance(err, errors.CommandNotFound):
        return
    elif isinstance(err, errors.MissingRequiredArgument):
        await ctx.send(f":x: Missing a required argument. Do !help {ctx.command}")
    elif isinstance(err, errors.BadArgument):
        await ctx.send(f":x: Bad argument. Do !help {ctx.command}")
    elif isinstance(err, errors.ExpectedClosingQuoteError):
        await ctx.send(f":x: {err}")
    elif isinstance(err, errors.UnexpectedQuoteError):
        await ctx.send(f":x: {err}")
    elif isinstance(err, errors.InvalidEndOfQuotedStringError):
        await ctx.send(f":x: {err}")
    elif isinstance(err, errors.PrivateMessageOnly):
        embed = discord.Embed(
            title=":lock: DMs only",
            description="This service is only available in direct messages",
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)
    elif isinstance(err, AuthFailure):
        embed = discord.Embed(
            title=":x: Authentification failure",
            description=str(err),
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)
    else:
        print("Uncaught error !")
        print("Error type:", type(err))
        print("Error message:", err)
        await ctx.send(":x: Error")
