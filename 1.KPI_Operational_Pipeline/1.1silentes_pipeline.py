# silentes_pipeline.py

from Data_Building.altas_loader import carga_trata_altas
from Data_Building.traffic_engineering import build_traffic_panel
from Data_Building.bigquery_queries import run_traffic_query

def build_silentes_pipeline(periodo_inicio, periodo_fin, path_altas):

    # 1. Cargar altas
    altas = carga_trata_altas(periodo_inicio, periodo_fin, path_altas)

    # 2. Query tráfico
    traffic = run_traffic_query(periodo_inicio)

    # 3. Construcción panel 21 días
    dataset = build_traffic_panel(altas, traffic)

    return dataset