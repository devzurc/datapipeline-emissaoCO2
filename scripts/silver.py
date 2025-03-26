import os
import logging
import pandas as pd
import settings


def clean_region(region: str, country: str, logger: logging.Logger) -> str:
    """
    Corrige e padroniza a coluna 'region' com base em um mapeamento.

    Args:
        region (str): Nome da região.
        country (str): Nome do país.
        logger (logging.Logger): Objeto de logging.

    Returns:
        str: Região corrigida ou valor padrão.
    """
    # Corrige a região se estiver no mapeamento
    if region in settings.REGION_MAPPING:
        return settings.REGION_MAPPING[region]

    # Se a região não for válida, tenta mapear pelo país
    if region not in settings.VALID_REGIONS:
        if country in settings.COUNTRY_TO_REGION:
            return settings.COUNTRY_TO_REGION[country]

        logger.warning(f"País sem região definida: {country}")
        return "Desconhecida"

    return region


def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trata valores ausentes no DataFrame.

    Args:
        df (pd.DataFrame): DataFrame a ser tratado.

    Returns:
        pd.DataFrame: DataFrame com valores preenchidos.
    """
    df = df.copy()  # Evita modificações diretas no DataFrame original

    # Preenchimento de valores ausentes
    df["country"] = df["country"].fillna("Desconhecido")
    df["region"] = df["region"].fillna("Desconhecida")
    df["kilotons_of_co2"] = df.groupby("region")["kilotons_of_co2"].transform(lambda x: x.fillna(x.mean()))
    df["metric_tons_per_capita"] = df.groupby("region")["metric_tons_per_capita"].transform(lambda x: x.fillna(x.mean()))

    return df


def etl_silver(logger: logging.Logger) -> pd.DataFrame:
    """
    Executa a camada Silver do ETL.
    - Lê um arquivo Parquet da Bronze Zone;
    - Realiza limpeza e transformação dos dados;
    - Salva o dataset transformado na Silver Zone.

    Args:
        logger (logging.Logger): Objeto de logging.

    Returns:
        pd.DataFrame: DataFrame transformado.
    """
    # Caminhos das zonas
    bronze_file_path = os.path.join(settings.BRONZE_ZONE, f"{settings.FILE_NAME}.parquet")

    if not os.path.exists(bronze_file_path):
        logger.error(f"Arquivo Parquet não encontrado: {bronze_file_path}")
        raise FileNotFoundError(f"Arquivo não encontrado: {bronze_file_path}")

    # Carregar os dados
    df = pd.read_parquet(bronze_file_path)
    logger.info(f"Arquivo carregado. Registros: {len(df)}")

    # Padronização de colunas
    df.columns = df.columns.str.replace(" ", "_").str.lower()

    # Padronização e limpeza da região
    df["region"] = df.apply(lambda row: clean_region(row["region"], row["country"], logger), axis=1)

    # Tratamento de valores nulos
    df = fill_missing_values(df)

    # Caminho de saída
    silver_file_path = os.path.join(settings.SILVER_ZONE, f"{settings.FILE_NAME}.parquet")

    # Salvar dataset transformado
    df.to_parquet(silver_file_path, engine="pyarrow", index=False)
    logger.info(f"Arquivo salvo na Silver Zone: {silver_file_path}")

    return df
