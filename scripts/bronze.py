import os
import logging
import pandas as pd
import settings


def etl_bronze(logger: logging.Logger) -> pd.DataFrame:
    """
    ETL - Camada Bronze:
    - Lê um arquivo CSV da fonte de dados;
    - Converte para formato Parquet;
    - Salva na zona Bronze do Lakehouse.

    Parâmetros:
        logger (logging.Logger): Logger para registrar os eventos.

    Retorna:
        pd.DataFrame: DataFrame carregado do CSV.
    """
    # Caminhos a partir do settings.py
    file_name = settings.FILE_NAME
    data_source = settings.DATA_SOURCE
    bronze_zone = settings.BRONZE_ZONE

    csv_file_source = os.path.join(data_source, f"{file_name}.csv")

    # Verifica se o arquivo existe antes de tentar carregar
    if not os.path.exists(csv_file_source):
        logger.error(f"Arquivo CSV não encontrado: {csv_file_source}")
        raise FileNotFoundError(f"Arquivo não encontrado: {csv_file_source}")

    # Lê o CSV para um DataFrame do Pandas
    df = pd.read_csv(csv_file_source)
    logger.info(f"Arquivo CSV carregado com sucesso de {csv_file_source}. Registros: {len(df)}")

    # Caminho do arquivo parquet para salvar na Bronze
    bronze_file_path = os.path.join(bronze_zone, f"{file_name}.parquet")

    # Converte para Parquet e salva
    df.to_parquet(bronze_file_path, engine="pyarrow", index=False)
    logger.info(f"Arquivo Parquet salvo na Bronze Zone: {bronze_file_path}")

    return df
