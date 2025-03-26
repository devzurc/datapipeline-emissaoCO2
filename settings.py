# ==========================
# Configurações para o Pipeline ETL
# ==========================
# Nome do arquivo de dados a ser processado
FILE_NAME = 'Emissão_CO2_por_países'
# Caminho para a fonte de dados (ex: onde os arquivos CSV estão armazenados)
DATA_SOURCE = 'data-source'
# Caminhos das zonas no Data Lakehouse (Medallion Architecture)
BRONZE_ZONE = 'data-lakehouse/bronze'
SILVER_ZONE = 'data-lakehouse/silver'
GOLD_ZONE = 'data-lakehouse/gold'
# Diretório onde os logs serão armazenados
LOG_DIRECTORY = 'logs/'

# ================================
# Mapeamento de Regiões e Países
# ================================
# Lista de regiões válidas (para validação e consistência)
VALID_REGIONS = ['Asia', 'Americas', 'Europe', 'Africa', 'Oceania']
# Mapeamento de regiões com nomes alternativos (ex: erros de digitação ou variações de idioma)
REGION_MAPPING = {
    "Europa": "Europe",
    "frica": "Africa",
    "américas": "Americas",
    "américa": "Americas",
    "améric": "Americas",
    "Ásia": "Asia",
    "ÁSia": "Asia",
    "ASIA": "Asia",
    "Ocean": "Oceania",
    "Euro": "Europe"
}
# Mapeamento de países para suas respectivas regiões (útil para preenchimento de dados)
COUNTRY_TO_REGION = {
    "Zimbabwe": "Africa",
}

# ==========================
# Outras Configurações
# ==========================
# Você pode adicionar outras variáveis de configuração, como parâmetros específicos de transformações.

