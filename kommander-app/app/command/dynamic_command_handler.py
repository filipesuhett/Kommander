import discord
from discord.ext import commands
from discord import Option
import subprocess
import os
from funcs.logger import logger

class DynamicCommands(commands.Cog):
    """
    Um Cog que cria e registra comandos slash dinamicamente
    a partir de um arquivo de configuração.
    """
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        # Mapeia o nome do comando à sua configuração para fácil acesso
        self._command_map = {cmd['name']: cmd for cmd in config.COMMANDS}
        self.register_commands()

    async def _master_handler(self, ctx: discord.ApplicationContext, **kwargs):
        """
        Handler central que contém toda a lógica para processar qualquer comando.
        """
        # Pega a configuração do comando que foi executado
        command_name = ctx.command.name
        command_config = self._command_map[command_name]

        await ctx.defer()

        # --- 1. Verificação de Permissões ---
        required_verb = command_config.get('verb')
        user_discord_roles = [role.name for role in ctx.author.roles]
        
        kommander_role = ''
        if 'devops' in user_discord_roles: kommander_role = 'devops'
        elif 'dev-write' in user_discord_roles: kommander_role = 'dev-write'
        elif 'dev-read' in user_discord_roles: kommander_role = 'dev-read'

        if not kommander_role:
            await ctx.respond(":no_entry: Você não possui um cargo do Kommander (dev-read, dev-write, devops).")
            return

        user_permissions = self.config.RULES.get(kommander_role, {})
        allowed_verbs = user_permissions.get('verbs', [])
        
        if required_verb not in allowed_verbs:
            msg = f":no_entry: Seu cargo '{kommander_role}' não permite a ação de '{required_verb}'."
            await ctx.respond(msg)
            logger.warning(f"Permissão negada para {ctx.author.name} no comando /{command_name}. Motivo: verbo não permitido.")
            return

        # --- 2. Construção do Comando Shell ---
        shell_command_parts = command_config['baseCommand'].split()
        
        for opt in command_config.get('options', []):
            opt_name = opt['name']
            if opt_name in kwargs and kwargs.get(opt_name) is not None:
                if opt_name == 'namespace':
                    shell_command_parts.extend(['-n', str(kwargs[opt_name])])
                elif opt_name != 'grep':
                    shell_command_parts.append(str(kwargs[opt_name]))
        
        if command_config['name'] == 'get' and not kwargs.get('namespace'):
            shell_command_parts.append('-A')

        grep_cmd = f" | grep {kwargs['grep']}" if 'grep' in kwargs and kwargs.get('grep') else ""
        final_cmd = ' '.join(shell_command_parts) + grep_cmd
        
        # --- 3. Execução e Resposta ---
        try:
            logger.info(f"Executando comando: '{final_cmd}' por {ctx.author.name}")
            process = subprocess.Popen(final_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(timeout=self.config.timeout)

            response_message = await ctx.respond(f":memo: `{final_cmd}`")
            
            output = stderr if process.returncode != 0 else stdout
            status = "Erro" if process.returncode != 0 else "Saída"
            response_content = f"**{status} do comando:**\n```\n{output or 'Nenhuma saída.'}\n```"

            if len(response_content) > 1950:
                with open('output.txt', 'w') as f: f.write(output)
                await ctx.send(file=discord.File('output.txt'))
                os.remove('output.txt')
            else:
                await ctx.send(response_content)
        except Exception as e:
            await ctx.respond(f":x: Um erro inesperado ocorreu: {e}")

    def register_commands(self):
        """Lê a configuração e registra cada comando."""
        for command_config in self.config.COMMANDS:
            self.create_and_register_command(command_config)

    def create_and_register_command(self, command_config: dict):
        """Cria uma função de callback com a assinatura correta e a registra no bot."""
        name = command_config['name']
        description = command_config['description']
        
        options_list = [
            Option(
                str,
                name=opt['name'],
                description=opt['description'],
                required=opt.get('required', False)
            ) for opt in command_config.get('options', [])
        ]

        # Gera os nomes dos parâmetros para a assinatura da função
        param_names = [opt.name for opt in options_list]

        # Usamos 'exec' para criar dinamicamente uma função com a assinatura exata
        # que o py-cord espera. Esta função 'stub' apenas chama nosso handler mestre.
        stub_code = f"""
async def {name}_stub(ctx, {', '.join(param_names)}):
    # Coleta todos os argumentos passados em um dicionário kwargs
    kwargs = locals()
    kwargs.pop('ctx')
    # Chama o handler mestre com os argumentos corretos
    await self._master_handler(ctx, **kwargs)
"""
        # Executa o código para definir a função em um escopo local
        local_scope = {}
        exec(stub_code, {"self": self}, local_scope)
        callback_func = local_scope[f'{name}_stub']

        # Cria e registra o comando usando a função stub gerada
        dynamic_command = discord.SlashCommand(
            callback_func,
            name=name,
            description=description,
            guild_ids=[int(self.config.guild_id)],
            options=options_list
        )
        
        self.bot.add_application_command(dynamic_command)
        logger.info(f"Comando dinâmico registrado: /{name}")

