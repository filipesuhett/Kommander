import os
from loguru import logger
from discord.ext import commands
from discord import Embed, option
import discord

# Check if the command is executed in the specified channel
def is_in_channel(Config):
    def predicate(ctx):
        if ctx.channel.name == Config().channel_name:
            return True
        else:
            raise commands.CheckFailure(f"You must be in the '{Config().channel_name}' channel to use this command.")
    return commands.check(predicate)

# Check if the user is an admin or has a specific role
def is_adm_or_has_role(role=None):
    async def predicate(ctx):
        try:
            is_adm = await commands.has_permissions(administrator=True).predicate(ctx)
            if is_adm:
                return True
        except commands.CheckFailure:
            pass

        if role is None:
            raise commands.CheckFailure("Only administrators can use this command.")
        else:
            try:
                has_role = await commands.has_any_role(role).predicate(ctx)
                if has_role:
                    return True
            except commands.CheckFailure:
                await ctx.send(f"{ctx.author.mention} You need the '{role}' role to use this command.")
                raise commands.CheckFailure(f"You need the '{role}' role to use this command.")

    return commands.check(predicate)

# Generic permission check based on roles
def check_permissions_generic(roles, message, Config):
    async def predicate(ctx):
        user_roles = [role.name for role in ctx.author.roles]
        if any(role in user_roles for role in roles):
            return True
        else:
            if not ctx.channel.name == Config().channel_name:
                raise commands.CheckFailure(f"You must be in the '{Config().channel_name}' channel to use this command.")
            else:
                await ctx.respond(f'{ctx.author.mention} {message}')
                raise commands.CheckFailure(message)
    return commands.check(predicate)

def have_permissions_geral(Config):
    return check_permissions_generic(['devops', 'dev-write', 'dev-read'], 'You need the "devops", "dev-write" or "dev-read" role to use this command.', Config)

def have_permissions_devops(Config):
    return check_permissions_generic(['devops'], 'You need the "devops" role to use this command.', Config)

def have_permissions_devwrite(Config):
    return check_permissions_generic(['devops', 'dev-write'], 'You need the "dev-write" role to use this command.', Config)
