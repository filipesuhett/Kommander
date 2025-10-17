import json
from funcs.messageModel import MessageModel as message
import logging

# Configurando o logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# Configurando o manipulador para exibir no console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Definindo o formato do registro de log como JSON
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage()
        }
        return json.dumps(log_data)

json_formatter = JSONFormatter()

# Configurando o formato do registro de log
console_handler.setFormatter(json_formatter)

# Adicionando o manipulador ao logger
logger.addHandler(console_handler)

class Logger(object): 
    def debug(details = None, parameters = None):
        logger.debug(message(details=details, parameters=parameters))
    
    def info(details = None, parameters = None):
        logger.info(message(details=details, parameters=parameters))

    def error(details = None, parameters = None):
        logger.error(message(details=details, parameters=parameters))

    def warning(details = None, parameters = None):
        logger.warning(message(details=details, parameters=parameters))