import os
import discord
import subprocess
import sys
from discord.ext import commands
from discord import Embed, option
from funcs.button import Confirm
from funcs.utils import show_logs_subprocess_stdout, get_context_params, get_context_params_resource
from funcs.logger import logger
import discord

async def get_resource(command, namespace, ctx, Config):
    await ctx.defer()

    user_roles = [role.name for role in ctx.author.roles]
    local_namespaces, local_verbs, local_types, local_role = get_context_params(user_roles, Config)

    if namespace not in local_namespaces:
        await ctx.respond(f':x: Namespace {namespace} not available')
        await ctx.send(command)
        logger.warning(f'Namespace {namespace} not available', {'operation': 'get_resource', 'command': command, 'author': ctx.author.name})
        return

    # Execute command and respond with output
    output = os.popen(command).read()
    await ctx.send(f':memo: {command}')

    if len(output) == 0:
        await ctx.respond(f':x: No resources found')
        logger.info(f'No resources found', {'operation': 'get_resource', 'command': command, 'author': ctx.author.name})
        return
    if len(output) <= 2000:
        await ctx.respond(f'```\n{output}\n```')
        logger.info(f'Resources found - {command}', {'operation': 'get_resource', 'command': command, 'author': ctx.author.name})
    else:
        with open('saida.txt', 'w') as f:
            f.write(output)
        await ctx.respond(file=discord.File('saida.txt'))
        os.remove('saida.txt')
        logger.info(f'Resources found - {command}', {'operation': 'get_resource', 'command': command, 'author': ctx.author.name})

# Describe resource and respond to the command
async def describe_resource(command, namespace, resource, type_resource, ctx, Config):
    await ctx.defer()

    # Get parameters by role
    user_roles = [role.name for role in ctx.author.roles]
    local_namespaces, local_verbs, local_types, local_role = get_context_params(user_roles, Config)
    local_resources = get_context_params_resource(user_roles, type_resource, namespace)
    
    if resource not in local_resources:
        await ctx.respond(f':x: Resource {resource} not available')
        await ctx.send(f':memo: {command}')
        logger.warning(f'Resource {resource} not available', {'operation': 'describe_resource', 'command': command, 'author': ctx.author.name})
        return

    if namespace not in local_namespaces:
        await ctx.respond(f':x: Namespace {namespace} not available')
        await ctx.send(f':memo: {command}')
        logger.warning(f'Namespace {namespace} not available', {'operation': 'describe_resource', 'command': command, 'author': ctx.author.name})
        return

    if resource == '':
        await ctx.respond(f':x: Resource {resource} not available')
        await ctx.send(f':memo: {command}')
        logger.warning(f'Resource {resource} not available', {'operation': 'describe_resource', 'command': command, 'author': ctx.author.name})
        return

    # Execute command and respond with output
    output = os.popen(command).read()
    await ctx.send(f':memo: {command}')

    if len(output) == 0:
        await ctx.respond(f':x: No resources described')
        logger.info(f'No resources described', {'operation': 'describe_resource', 'command': command, 'author': ctx.author.name})
        return
    if len(output) <= 2000:
        await ctx.respond(f'```\n{output}\n```')
        logger.info(f'Resources described - {command}', {'operation': 'describe_resource', 'command': command, 'author': ctx.author.name})
    else:
        with open('saida.txt', 'w') as f:
            f.write(output)
        await ctx.respond(file=discord.File('saida.txt'))
        os.remove('saida.txt')
        logger.info(f'Resources described - {command}', {'operation': 'describe_resource', 'command': command, 'author': ctx.author.name})

# Delete resource and respond to the command
async def delete_resource(command, resource, namespace, type_resource, ctx, Config):
    # Get user roles and context parameters
    user_roles = [role.name for role in ctx.author.roles]
    local_namespaces, local_verbs, local_types, local_role = get_context_params(user_roles, Config)
    local_resources = get_context_params_resource(user_roles, type_resource, namespace)
    
    # Check if the namespace is available for the user
    if namespace not in local_namespaces:
        await ctx.respond(f':x: Namespace {namespace} not available')
        await ctx.send(command)
        logger.warning(f'Namespace {namespace} not available', {'operation': 'delete_resource', 'command': command, 'author': ctx.author.name})
        return

    # Check if the pod is available for the user
    if resource not in local_resources:
        await ctx.respond(f':x: Resource {resource} not available')
        await ctx.send(command)
        logger.warning(f'Resource {resource} not available', {'operation': 'delete_resource', 'command': command, 'author': ctx.author.name})
        return 
    
    # Execute command and respond with output
    output = os.popen(command).read()
    await ctx.send(f':memo: {command}')
    
    if len(output) <= 2000:
        await ctx.respond(f'```\n{output}\n```')
        logger.info(f'Resources deleted - {command}', {'operation': 'delete_resource', 'command': command, 'author': ctx.author.name})
    else:
        with open('saida.txt', 'w') as f:
            f.write(output)
        await ctx.respond(file=discord.File('saida.txt'))
        os.remove('saida.txt')
        logger.info(f'Resources deleted - {command}', {'operation': 'delete_resource', 'command': command, 'author': ctx.author.name})

# Get commander context and respond to the command
async def get_commander(ctx, command, grep, namespace, Config):
    if namespace == "":
        if grep == "":
            command += f' -A'
        else:
            command += f' -A | grep {grep}'
    else:
        if grep == "":
            command += f' -n {namespace}'
        else:
            command += f' -n {namespace} | grep {grep}'

    await get_resource(command, namespace ,ctx, Config)

async def rollout_command(command, resource_principal, namespace, aux, ctx, Config):
    user_roles = [role.name for role in ctx.author.roles]
    local_namespaces, local_verbs, local_types, local_role = get_context_params(user_roles, Config)
    if aux != "s":
        local_resources = get_context_params_resource(user_roles, "deployments", namespace)
    else:
        local_resources = get_context_params_resource(user_roles, "statefulsets", namespace)
    
    # Check if namespace is available
    if namespace not in local_namespaces:
        await ctx.respond(f':x: Namespace {namespace} not available')
        await ctx.send(f':memo: kubectl rollout restart statefulset {resource_principal} -n {namespace}')
        logger.warning(f'Namespace {namespace} not available', {'operation': 'rollout_command', 'command': command, 'author': ctx.author.name})
        return
    
    if resource_principal not in local_resources:
        if aux == "s":
            local_resources_err = get_context_params_resource(user_roles, "deployments", namespace)
            aux_principal = "deployment"
            aux_secundary = "statefulset"
        else:
            local_resources_err = get_context_params_resource(user_roles, "statefulsets", namespace)
            aux_principal = "statefulset"
            aux_secundary = "deployment" 
        if resource_principal in local_resources_err:
            view = Confirm()
            message = await ctx.respond(f'The {aux_secundary} mentioned is actually a {aux_principal}, if you still want to rollout, confirm with the button', view=view)
            await view.wait()

            if view.value is None:
                await message.edit(content='Timeout. Operation canceled.', view=None)
                logger.warning(f'Operation canceled', {'operation': 'rollout_command', 'command': command, 'author': ctx.author.name})
                return
            elif view.value:
                process = subprocess.Popen(['kubectl', 'rollout', 'restart', aux_principal, resource_principal, '-n', namespace], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                await message.edit(content=f'```\n{stdout.decode()}\n```', view=None)
                await ctx.send(f':memo: kubectl rollout restart {aux_principal} {resource_principal} -n {namespace}')
                logger.info(f'Resources rolled out {namespace} - kubectl rollout restart {aux_principal} {resource_principal} -n {namespace}', {'operation': 'rollout_command', 'command': command, 'author': ctx.author.name})
                return
            else:
                await message.edit(content='Operation canceled.', view=None)
                logger.warning(f'Operation canceled', {'operation': 'rollout_command', 'command': command, 'author': ctx.author.name})
                return
        else:    
            await ctx.respond(f':x: {aux_principal} {resource_principal} not available in namespace {namespace}')
            await ctx.send(f':memo: kubectl rollout restart {aux_principal} {resource_principal} -n {namespace}')
            logger.info(f'Resources rolled out {namespace} - kubectl rollout restart {aux_principal} {resource_principal} -n {namespace}', {'operation': 'rollout_command', 'command': command, 'author': ctx.author.name})
            return
    
    if aux != "s":
        process = subprocess.Popen(['kubectl', 'rollout', 'restart', 'deployment', resource_principal, '-n', namespace], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen(['kubectl', 'rollout', 'restart', 'statefulset', resource_principal, '-n', namespace], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    await show_logs_subprocess_stdout(process, command, ctx)