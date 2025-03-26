import os
import logging
import pandas as pd
import settings


def etl_gold(logger: logging.Logger) -> None:
    """
    Executa a camada Gold do ETL:
    - Lê os dados da zona Silver;
    - Realiza agregações e cálculos para análise de BI;
    - Salva os resultados na zona Gold.
    
    Parâmetros:
        logger (logging.Logger): Objeto de logging para registrar informações durante o processo.
    """
    # Caminho do arquivo na zona Silver
    silver_file_path = os.path.join(settings.SILVER_ZONE, f"{settings.FILE_NAME}.parquet")
    
    # Verifica se o arquivo existe
    if not os.path.exists(silver_file_path):
        logger.error(f"Arquivo Parquet não encontrado: {silver_file_path}")
        raise FileNotFoundError(f"Arquivo não encontrado: {silver_file_path}")
    
    # Carregar o dataset da zona Silver
    df_silver = pd.read_parquet(silver_file_path)
    logger.info(f"Arquivo carregado da Silver Zone. Registros: {len(df_silver)}")
    
    # 1. Total de Kilotons de CO2 por Região e Metric Tons Per Capita
    co2_by_region = df_silver.groupby("region").agg(
        kilotons_of_co2_sum=('kilotons_of_co2', 'sum'),
        metric_tons_per_capita_sum=('metric_tons_per_capita', 'sum')
    ).reset_index()
    
    # 2. Identificando as regiões com maior potencial de redução de CO2
    co2_by_region['reduction_potential'] = co2_by_region['metric_tons_per_capita_sum']
    
    # Ordenar pela maior potencial de redução
    co2_by_region = co2_by_region.sort_values(by="reduction_potential", ascending=False)
    
    # 3. Países com as maiores emissões de CO2 e Metric Tons Per Capita
    top_countries = df_silver.groupby("country").agg(
        kilotons_of_co2_sum=('kilotons_of_co2', 'sum'),
        metric_tons_per_capita_sum=('metric_tons_per_capita', 'sum')
    ).reset_index()
    top_countries = top_countries.sort_values(by="kilotons_of_co2_sum", ascending=False)
    
    # Caminhos para salvar os resultados na Gold Zone
    gold_co2_by_region = os.path.join(settings.GOLD_ZONE, "co2_by_region.parquet")
    gold_top_countries = os.path.join(settings.GOLD_ZONE, "top_countries_co2.parquet")
    gold_reduction_potential = os.path.join(settings.GOLD_ZONE, "reduction_potential_by_region.parquet")
    
    # Salvar resultados
    co2_by_region.to_parquet(gold_co2_by_region, engine="pyarrow", index=False)
    top_countries.to_parquet(gold_top_countries, engine="pyarrow", index=False)
    co2_by_region.to_parquet(gold_reduction_potential, engine="pyarrow", index=False)
    
    logger.info("Resultados de BI salvos com sucesso na Gold Zone!")


