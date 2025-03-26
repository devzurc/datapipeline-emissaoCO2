# Importando as bibliotecas
from scripts import bronze, silver, gold, utils

# Carregar configuração
config = utils.load_config("config.cfg")

# Configurar o logger
logger = utils.setup_logging()

# Configurar a arquitetura do Lakehouse
logger = utils.setup_lakehouse(logger)

# ETL Bronze: Transformar CSV em arquivo Parquet
bronze.etl_bronze(logger)

# ETL Silver: Limpeza e Transformação dos Dados
silver.etl_silver(logger)

# ETL Gold: Aplicar Business Intelligence
gold.etl_gold(logger)
