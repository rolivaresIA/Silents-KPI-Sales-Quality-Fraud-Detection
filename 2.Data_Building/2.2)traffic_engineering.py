import numpy as np
import pandas as pd


def build_traffic_panel(altas: pd.DataFrame, traffic: pd.DataFrame) -> pd.DataFrame:
    """
    Construye el panel de comportamiento post-alta (21 días)
    para la definición del KPI Silentes.

    Un PCS es considerado "silente" si no presenta tráfico de voz
    ni datos dentro de los primeros 21 días posteriores a su alta.
    """

    # =========================
    # 1. PREPARACIÓN DE DATOS
    # =========================
    traffic = traffic.copy()
    altas = altas.copy()

    traffic["FECHA"] = pd.to_datetime(traffic["FECHA"], format="%Y%m%d")
    altas["FECHA_ALTA"] = pd.to_datetime(altas["FECHA_ALTA"])

    # Normalización tipo clave
    traffic["PCS"] = traffic["PCS"].astype("int64")
    altas["PCS"] = altas["PCS"].astype("int64")

    # =========================
    # 2. MERGE BASE (ALTAS vs TRAFICO)
    # =========================
    altas_traffic = pd.merge(
        altas[["PCS", "FECHA_ALTA"]],
        traffic[["PCS", "FECHA"]],
        on="PCS",
        how="left",
        indicator=True
    )

    # =========================
    # 3. CÁLCULO DE DIFERENCIA DE DÍAS
    # =========================
    altas_traffic["DIF_FECHAS"] = (
        altas_traffic["FECHA"] - altas_traffic["FECHA_ALTA"]
    ).dt.days

    # Limpieza de valores inválidos (tráfico previo a alta o nulos)
    altas_traffic.loc[altas_traffic["DIF_FECHAS"] < 0, "DIF_FECHAS"] = 999999
    altas_traffic["DIF_FECHAS"] = altas_traffic["DIF_FECHAS"].fillna(999999).astype("int64")

    # =========================
    # 4. ONE-HOT ENCODING DE VENTANA TEMPORAL
    # =========================
    dummies = pd.get_dummies(
        altas_traffic["DIF_FECHAS"],
        prefix="TRAFFIC_DAY"
    ).astype(int)

    altas_traffic_panel = pd.concat(
        [altas_traffic[["PCS", "FECHA_ALTA", "DIF_FECHAS"]], dummies],
        axis=1
    )

    # =========================
    # 5. AGRUPACIÓN POR PCS
    # =========================
    traffic_cols = [c for c in altas_traffic_panel.columns if c.startswith("TRAFFIC_DAY_")]

    altas_traffic_final = (
        altas_traffic_panel
        .groupby(["PCS", "FECHA_ALTA"])[traffic_cols]
        .sum()
        .reset_index()
    )

    # =========================
    # 6. FILTRO DE OBSERVABILIDAD (>= 21 días)
    # =========================
    last_day = traffic["FECHA"].max()

    altas_traffic_final = altas_traffic_final[
        (last_day - altas_traffic_final["FECHA_ALTA"]).dt.days >= 21
    ].copy()

    # =========================
    # 7. PROPAGACIÓN DE TRAFICO (LOGICA SILENTES)
    # =========================
    # Si un PCS tiene tráfico en un día, se considera activo desde ese punto en adelante

    for i, col in enumerate(traffic_cols):
        altas_traffic_final.loc[
            altas_traffic_final[col] > 0,
            traffic_cols[i:]
        ] = 1

    # =========================
    # 8. LIMPIEZA FINAL (BINARIZACIÓN)
    # =========================
    altas_traffic_final[traffic_cols] = (
        altas_traffic_final[traffic_cols]
        .apply(lambda col: col.map(lambda x: 1 if x > 0 else 0))
    )

    # =========================
    # 9. OUTPUT FINAL DEL KPI
    # =========================
    return altas_traffic_final