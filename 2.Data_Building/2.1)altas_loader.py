# altas_loader.py

import numpy as np
import pandas as pd
from pathlib import Path


def carga_trata_altas(añomes_inicio: str, añomes_fin: str, carpeta_altas: str) -> pd.DataFrame:
    """
    Carga, limpia y estandariza datos de altas comerciales.
    Output: DataFrame consolidado de activaciones (PCS).
    """

    # =========================
    # 1. RANGOS DE PERIODO
    # =========================
    año_inicio = int(añomes_inicio[:4])
    año_fin = int(añomes_fin[:4])
    años = range(año_inicio, año_fin + 1)

    carpeta_altas = Path(carpeta_altas)

    lista_inmediatas = []
    lista_diferidas = []
    archivos_altas_filtrados = []

    # =========================
    # 2. CARGA DE ARCHIVOS
    # =========================
    for año in años:
        carpeta_año = carpeta_altas / str(año)

        if not carpeta_año.exists():
            continue

        for archivo in carpeta_año.iterdir():
            if not archivo.is_file():
                continue

            periodo = archivo.name[-9:-5] + archivo.name[-11:-9]

            if añomes_inicio <= periodo <= añomes_fin:
                archivos_altas_filtrados.append(archivo.name)

                sheets = pd.read_excel(
                    archivo,
                    sheet_name=["Inmediatas", "Siembra"]
                )

                df_inm = sheets["Inmediatas"]
                df_dif = sheets["Siembra"]

                df_inm = df_inm.assign(PERIODO_ALTA=periodo)
                df_dif = df_dif.assign(PERIODO_ALTA=periodo)

                lista_inmediatas.append(df_inm)
                lista_diferidas.append(df_dif)

    print("📂 Archivos de altas cargados:")
    for a in archivos_altas_filtrados:
        print(" -", a)

    # =========================
    # 3. CONCATENACIÓN
    # =========================
    concat_inmediatas = pd.concat(lista_inmediatas, ignore_index=True) if lista_inmediatas else pd.DataFrame()
    concat_diferidas = pd.concat(lista_diferidas, ignore_index=True) if lista_diferidas else pd.DataFrame()

    # =========================
    # 4. ESTRUCTURA DE COLUMNAS
    # =========================
    cols_inm = [
        'PCS','rut_titular_cuenta','cuenta_suscriptora','AV','AñoGestion',
        'MesGestion','DiaGestion','TipoVenta','Subclasificacion','Canal',
        'SubCanal','NOMBRE_ESTAN_VTA','migracion2','PLAN','NOMBRE_SUC_VENTA',
        'usuario','PERIODO_ALTA'
    ]

    cols_dif = [
        'Nro_de_PCS','Rut_Titular_Cuenta','cuenta_Suscriptora','AV',
        'AñoActivacion','MesActivacion','DiaActivacion','TipoVenta',
        'Subclasificacion','Canal','SubCanal','VC_PORTAL_BST_DAC',
        'Migracion2','PLAN','VC_DETALLE_SUC_FINAL','VC_COD_VENDEDOR_FINAL',
        'PERIODO_ALTA'
    ]

    altas_inmediatas = concat_inmediatas.reindex(columns=cols_inm)
    altas_diferidas = concat_diferidas.reindex(columns=cols_dif)

    # =========================
    # 5. RENOMBRE DE VARIABLES
    # =========================
    rename_inm = {
        'rut_titular_cuenta':'RUT',
        'cuenta_suscriptora':'CUENTA_SUSCRIPTORA',
        'AV':'ANULADA',
        'AñoGestion':'AÑO_ALTA',
        'MesGestion':'MES_ALTA',
        'DiaGestion':'DIA_ALTA',
        'TipoVenta':'TIPO_VENTA',
        'Subclasificacion':'SUBCLASIFICACION',
        'Canal':'MACROCANAL',
        'SubCanal':'CANAL',
        'NOMBRE_ESTAN_VTA':'DISTRIBUIDOR',
        'migracion2':'MIGRACION',
        'NOMBRE_SUC_VENTA':'SUCURSAL',
        'usuario':'RUT_VENDEDOR'
    }

    rename_dif = {
        'Nro_de_PCS':'PCS',
        'Rut_Titular_Cuenta':'RUT',
        'cuenta_Suscriptora':'CUENTA_SUSCRIPTORA',
        'AV':'ANULADA',
        'AñoActivacion':'AÑO_ALTA',
        'MesActivacion':'MES_ALTA',
        'DiaActivacion':'DIA_ALTA',
        'TipoVenta':'TIPO_VENTA',
        'Subclasificacion':'SUBCLASIFICACION',
        'Canal':'MACROCANAL',
        'SubCanal':'CANAL',
        'VC_PORTAL_BST_DAC':'DISTRIBUIDOR',
        'Migracion2':'MIGRACION',
        'VC_DETALLE_SUC_FINAL':'SUCURSAL',
        'VC_COD_VENDEDOR_FINAL':'RUT_VENDEDOR'
    }

    altas_inmediatas = altas_inmediatas.rename(columns=rename_inm)
    altas_diferidas = altas_diferidas.rename(columns=rename_dif)

    # =========================
    # 6. UNIFICACIÓN
    # =========================
    altas = pd.concat([altas_inmediatas, altas_diferidas], ignore_index=True)

    # =========================
    # 7. FILTROS BASE
    # =========================
    altas = altas[altas["SUBCLASIFICACION"] == "PERSONA"].copy()

    # =========================
    # 8. FEATURE ENGINEERING BÁSICO
    # =========================
    altas["FECHA_ALTA"] = pd.to_datetime(
        dict(
            year=altas["AÑO_ALTA"],
            month=altas["MES_ALTA"],
            day=altas["DIA_ALTA"]
        )
    )

    altas["PERIODO_ALTA"] = altas["FECHA_ALTA"].dt.strftime("%Y%m").astype("int64")

    altas["RUT_SV"] = altas["RUT"].astype(str).str.split("-").str[0]

    # =========================
    # 9. TIPO PLAN
    # =========================
    altas["TIPO_PLAN"] = "OTRO"

    condiciones = [
        ("X LIBRE", r"X LIBRE"),
        ("S", r" S($| )"),
        ("M", r" M($| )"),
        ("PREMIUM LIBRE", r"PREMIUM LIBRE"),
        ("XL LIBRE", r"XL LIBRE"),
        ("L LIBRE", r"L LIBRE"),
    ]

    for label, pattern in condiciones:
        mask = altas["PLAN"].str.contains(pattern, regex=True, na=False)
        altas.loc[mask, "TIPO_PLAN"] = label

    # =========================
    # 10. OUTPUT FINAL
    # =========================
    cols_final = [
        'PCS','RUT','CUENTA_SUSCRIPTORA','FECHA_ALTA','PERIODO_ALTA',
        'TIPO_VENTA','SUBCLASIFICACION','MACROCANAL','CANAL',
        'DISTRIBUIDOR','MIGRACION','PLAN','TIPO_PLAN',
        'SUCURSAL','RUT_VENDEDOR'
    ]

    return altas.loc[:, cols_final]