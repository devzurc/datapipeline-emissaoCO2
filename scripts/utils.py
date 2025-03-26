import os
import logging
import settings
from datetime import datetime


def setup_lakehouse(logger: logging.Logger) -> logging.Logger:
    """
    Configura as pastas para a Arquitetura Lakehouse (Medallion Architecture).
    
    Parâmetros:
        logger (logging.Logger): Objeto de logging para registrar informações durante a execução.
    
    Retorna:
        logging.Logger: Logger configurado.
    """
    # Caminhos para as zonas Bronze, Silver e Gold
    bronze_zone = settings.BRONZE_ZONE
    silver_zone = settings.SILVER_ZONE
    gold_zone = settings.GOLD_ZONE
    
    # Criação das pastas, se não existirem
    for folder in [bronze_zone, silver_zone, gold_zone]:
        os.makedirs(folder, exist_ok=True)

    logger.info("Diretórios da arquitetura Lakehouse verificadas com sucesso.")
    return logger


def setup_logging() -> logging.Logger:
    """
    Configura o logging para o pipeline ETL.
    
    Retorna:
        logging.Logger: Logger configurado.
    """
    log_directory = settings.LOG_DIRECTORY
    
    # Cria a pasta de logs caso não exista
    os.makedirs(log_directory, exist_ok=True)
    
    # Define o nome do arquivo de log com base na data e hora
    log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_etl_pipeline.log"
    log_file = os.path.join(log_directory, log_filename)
    
    # Configura o logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),  # Salva logs no arquivo
            logging.StreamHandler()         # Exibe logs no console
        ]
    )
    logger = logging.getLogger("ETL-Pipeline")
    logger.info("Configuração de logging concluída.")
    return logger


def load_config(file_path: str) -> dict:
    """
    Carrega o arquivo de configuração (config.cfg) para obter variáveis de caminho e outros parâmetros.
    
    Parâmetros:
        file_path (str): Caminho do arquivo de configuração.
    
    Retorna:
        dict: Dicionário com as configurações carregadas.
    """
    import configparser
    
    config = configparser.ConfigParser()
    config.read(file_path)
    
    logger = logging.getLogger("ETL-Pipeline")
    logger.info(f"Configuração carregada de {file_path}.")
    
    return config
