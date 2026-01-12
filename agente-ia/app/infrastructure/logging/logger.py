import structlog
import logging
from pythonjsonlogger import jsonlogger


def setup_logging():
    """Configura logging estruturado com JSON"""
    # Configurar handler JSON
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        "%(timestamp)s %(level)s %(name)s %(message)s"
    )
    handler.setFormatter(formatter)
    
    # Configurar root logger
    root_logger = logging.getLogger()
    root_logger.handlers = []
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
    
    # Configurar structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = None):
    """Retorna logger estruturado"""
    return structlog.get_logger(name)
