import os
import pytz
import yaml
import sys
from loguru import logger
from yaml import load, SafeLoader

class Config:
    def __init__(self):
        # Carrega configurações a partir de variáveis de ambiente
        self.channel_name = os.getenv('CHANNEL_NAME')
        self.timeout = int(os.getenv('TIMEOUT', 60))
        self.token_discord = os.getenv('DISCORD_TOKEN')
        self.guild_id = os.getenv('GUILD_ID')
        self.brazil = pytz.timezone("America/Sao_Paulo")

        # Modo de Operação: Local (via args) ou Contêiner (caminhos fixos)
        is_local_run = len(sys.argv) >= 3
        
        rules_config_path = sys.argv[1] if is_local_run else "/usr/src/app/config/configs.yaml"
        commands_config_path = sys.argv[2] if is_local_run else "/usr/src/app/config/commands.yaml"

        if is_local_run:
            logger.info(f"Rodando em modo LOCAL. Lendo config de: {rules_config_path} e {commands_config_path}")
        else:
            logger.info("Rodando em modo CONTEINER. Lendo configurações de caminhos fixos.")

        # Carrega o arquivo de REGRAS
        try:
            with open(rules_config_path, "r") as f:
                config_data = load(f, SafeLoader)
            # A única coisa que precisamos guardar são as REGRAS (RULES)
            self.RULES = config_data.get('config', {}).get('RULES', {})
            logger.info(f"Arquivo de regras '{rules_config_path}' carregado com sucesso.")
        except FileNotFoundError:
            logger.error(f"Arquivo de regras não encontrado: {rules_config_path}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Erro ao carregar o arquivo de regras: {e}")
            sys.exit(1)

        # Carrega o arquivo de COMANDOS
        try:
            with open(commands_config_path, "r") as f:
                 kommander_config = load(f, SafeLoader)
            self.COMMANDS = kommander_config.get('kommander', {}).get('commands', [])
            logger.info(f"Arquivo de comandos '{commands_config_path}' carregado. {len(self.COMMANDS)} comandos encontrados.")
        except FileNotFoundError:
            logger.error(f"Arquivo de configuração de comandos não encontrado em '{commands_config_path}'")
            self.COMMANDS = []
        except Exception as e:
            logger.error(f"Erro ao carregar o arquivo de comandos: {e}")
            self.COMMANDS = []

