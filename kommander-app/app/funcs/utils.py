import os
import discord
import subprocess
import sys
from loguru import logger
from discord.ext import commands
from discord import Embed, option
from funcs.logger import logger

# Get context parameters based on user roles
def get_context_params(user_roles, Config):
    local_namespaces = []
    local_role = ''
    
    # Determine user role
    for rolex in ['devops', 'dev-write', 'dev-read']:
        if rolex in user_roles:
            local_role = rolex

    # Get namespaces
    output = os.popen(f'kubectl get ns -o custom-columns=NAME:.metadata.name --no-headers').read()
    all_namespaces = output.split('\n')
    for ns in all_namespaces:
        if ns not in Config().RULES[local_role]['exclude_ns']:
            local_namespaces.append(ns)

    local_verbs = Config().RULES[local_role]['verbs']
    local_types = Config().RULES[local_role]['types']

    return local_namespaces, local_verbs, local_types, local_role

# Get resources based on user roles, resource type, and namespace
def get_context_params_resource(user_roles, resource, namespace):
    local_resources = []
    local_role = ''
    
    # Determine user role
    for rolex in ['devops', 'dev-write', 'dev-read']:
        if rolex in user_roles:
            local_role = rolex

    # Get resources
    output = os.popen(f'kubectl get {resource} -n {namespace} -o custom-columns=NAME:.metadata.name --no-headers').read()
    all_resources = output.split('\n')
    
    for deployment in all_resources:
        local_resources.append(deployment)

    return local_resources

async def show_logs_subprocess_stderr(process, command, ctx):    
    stdout, stderr = process.communicate()
    
    # Respond with the stderr output and command issued
    await ctx.respond(f'```\n{stderr.decode()}\n```')
    await ctx.send(command)
    logger.info(f'Flux command succeeded - {command}', {'operation': 'flux_command', 'command': command, 'author': ctx.author.name})
    
async def show_logs_subprocess_stdout(process, command, ctx):    
    stdout, stderr = process.communicate()
    
    # Respond with the stdout output and command issued
    await ctx.respond(f'```\n{stdout.decode()}\n```')
    await ctx.send(command)
    logger.info(f'Command succeeded - {command}', {'operation': 'flux_command', 'command': command, 'author': ctx.author.name})
    
async def helps(ctx):
    # Describe Category
    commands_embed = discord.Embed(title="Help", description="ALL COMMANDS")
    commands_embed.add_field(name="/describe-pod", value="Describe Pod - (Dev-Write Only)")
    commands_embed.add_field(name="/describe-deployment", value="Describe Deployment - (Dev-Write Only)")
    commands_embed.add_field(name="/describe-statefulset", value="Describe Statefulset - (Dev-Write Only)")
    commands_embed.add_field(name="/describe-helmrelease", value="Describe Helmrelease - (Dev-Write Only)")
    commands_embed.add_field(name="/get-namespaces", value="Show all namespaces")
    commands_embed.add_field(name="/get-fail-pods", value="Show all fail pods in a namespace")
    commands_embed.add_field(name="/get-pods", value="Show all pods in a namespace or all pods")
    commands_embed.add_field(name="/get-services", value="Show all services in a namespace or all services")
    commands_embed.add_field(name="/get-deployments", value="Show all deployments in a namespace or all deployments")
    commands_embed.add_field(name="/get-statefulsets", value="Show all statefulsets in a namespace or all statefulsets")
    commands_embed.add_field(name="/get-helmreleases", value="Show all helmreleases in a namespace or all helmreleases")
    commands_embed.add_field(name="/get-ingresses", value="Show all ingresses in a namespace or all ingresses - (DevOps Only)")
    commands_embed.add_field(name="/get-serviceaccounts", value="Show all serviceaccounts in a namespace or all serviceaccounts - (DevOps Only)")
    commands_embed.add_field(name="/rollout-deployment", value="Rollout deployment - (Dev-Write Only)")
    commands_embed.add_field(name="/rollout-statefulset", value="Rollout statefulset - (Dev-Write Only)")
    commands_embed.add_field(name="/flux-reconcile", value="Reconcile flux - (DevOps Only)")
    commands_embed.add_field(name="/flux-resume", value="Resume flux - (DevOps Only)")
    commands_embed.add_field(name="/flux-suspend", value="Suspend flux - (DevOps Only)")
    commands_embed.add_field(name="/delete-pod", value="Delete pod - (Dev-Write Only)")
    commands_embed.add_field(name="/delete-helmrelease", value="Delete helmrelease - (Dev-Write Only)")
    commands_embed.add_field(name="/logs-pod", value="Show pod's log")

    await ctx.respond(embed=commands_embed)
    await ctx.send(f':memo: ALL COMMANDS - HELP')
    logger.info(f'Command Help', {'operation': 'help', 'command': '\help', 'author': ctx.author.name})
    
    return