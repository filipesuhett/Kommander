import discord
from discord.ext import commands
from bot.bot import Bot
from bot.config import Config
from command.dynamic_command_handler import DynamicCommands
# Corrigido: Importa a classe Logger, e não a instância.
from funcs.logger import Logger as KommanderLogger
import sys

def main():
    # --- CORREÇÃO AQUI ---
    # Em vez de pedir tudo com .all(), pedimos as permissões padrão
    # e habilitamos explicitamente as privilegiadas que precisamos.
    intents = discord.Intents.default()
    intents.members = True  # Necessário para o evento on_member_join
    intents.message_content = True # Boa prática para futuras funcionalidades

    # Inicializa a configuração e o bot
    config = Config()
    bot = Bot(command_prefix='/', help_command=None, intents=intents)

    # Adiciona o Cog que irá registrar todos os comandos dinamicamente
    bot.add_cog(DynamicCommands(bot, config))

    @bot.event
    async def on_ready():
        """Evento para quando o bot se conecta ao Discord."""
        print(f"{bot.user.name} conectou-se ao Discord!")
        # Corrigido: Usa a classe Logger com 'details' e 'parameters'
        KommanderLogger.info(details=f"{bot.user.name} conectou-se ao Discord!", parameters={'operation': 'connect'})

    @bot.event
    async def on_error(event, *args, **kwargs):
        """Evento para quando ocorre um erro."""
        # Corrigido: Usa a classe Logger com 'details' e 'parameters'
        KommanderLogger.error(details=f"Ocorreu um erro no evento: {event}", parameters={"args": args, "kwargs": kwargs})

    @bot.event
    async def on_member_join(member):
        """Evento para quando um novo membro entra no servidor."""
        role_names = ["devs", "dev-read"]
        roles_to_add = [discord.utils.get(member.guild.roles, name=name) for name in role_names]
        
        for role in roles_to_add:
            if role and role not in member.roles:
                try:
                    await member.add_roles(role)
                    KommanderLogger.info(details=f"Cargo '{role.name}' adicionado a {member.display_name}.")
                except discord.Forbidden:
                    KommanderLogger.error(details=f"Sem permissão para adicionar o cargo '{role.name}' a {member.display_name}.")
                except Exception as e:
                    KommanderLogger.error(details=f"Erro ao adicionar cargo a {member.display_name}: {e}")

    # Inicia o bot
    # Corrigido: Usa a classe Logger com 'details' e 'parameters'
    KommanderLogger.info(details="Iniciando o Kommander com sistema de comandos dinâmicos.", parameters={'operation': 'start'})
    bot.run(config.token_discord)

if __name__ == "__main__":
    main()

