-- =========================================================
-- SILENTES KPI - TRAFFIC EXTRACTION PIPELINE
-- =========================================================
-- Objetivo:
-- Extraer tráfico de voz y datos para PCS activados (altas),
-- dentro de una ventana de análisis post-activación.
-- =========================================================

-- =========================
-- 1. TRÁFICO LLAMADAS SALIENTES
-- =========================
WITH trafico_llamadas_salientes AS (

  SELECT
    CAST(FECHA_EVENTO AS STRING) AS FECHA,
    CAST(NUMERO_ORIGEN AS STRING) AS PCS,
    SUM(DURACION) AS DURACION_DIARIA_LLAMADAS_SALIENTES

  FROM `datalake-project-dev.usage_curated.mobile_v002_voice_traffic`

  WHERE dt BETWEEN @dt_inicio AND @dt_fin
    AND CAST(FECHA_EVENTO AS STRING) BETWEEN @fecha_evento_inicio AND @fecha_evento_fin
    AND ID_SENTIDO_TRAFICO = 1
    AND RIGHT(CAST(NUMERO_ORIGEN AS STRING), 9) != RIGHT(CAST(NUMERO_DESTINO AS STRING), 9)

    -- filtro PCS relevantes (altas cargadas)
    AND CAST(NUMERO_ORIGEN AS STRING) IN (
      SELECT CAST(PCS AS STRING)
      FROM `analytics-project-dev.analytics_studies_dev.TMP_PREFILTER_SILENT_SALES`
    )

  GROUP BY FECHA, PCS
),


-- =========================
-- 2. TRÁFICO LLAMADAS ENTRANTES
-- =========================
trafico_llamadas_entrantes AS (

  SELECT
    CAST(FECHA_EVENTO AS STRING) AS FECHA,
    CAST(NUMERO_ORIGEN AS STRING) AS PCS,
    SUM(DURACION) AS DURACION_DIARIA_LLAMADAS_ENTRANTES

  FROM `datalake-project-dev.usage_curated.mobile_v002_voice_traffic`

  WHERE dt BETWEEN @dt_inicio AND @dt_fin
    AND CAST(FECHA_EVENTO AS STRING) BETWEEN @fecha_evento_inicio AND @fecha_evento_fin
    AND ID_SENTIDO_TRAFICO = 2
    AND RIGHT(CAST(NUMERO_ORIGEN AS STRING), 9) != RIGHT(CAST(NUMERO_DESTINO AS STRING), 9)

    AND CAST(NUMERO_ORIGEN AS STRING) IN (
      SELECT CAST(PCS AS STRING)
      FROM `analytics-project-dev.analytics_studies_dev.TMP_PREFILTER_SILENT_SALES`
    )

  GROUP BY FECHA, PCS
),


-- =========================
-- 3. TRÁFICO DE DATOS
-- =========================
trafico_datos AS (

  SELECT
    CAST(DATE_EVENT AS STRING) AS FECHA,
    CAST(SERVED_MSISDN AS STRING) AS PCS,

    SUM(CAST(DATA_VOLUME_GPRS_UPLINK_RATE AS INT64)) +
    SUM(CAST(DATA_VOLUME_GPRS_UPLINK_NORATE AS INT64)) +
    SUM(CAST(DATA_VOLUME_GPRS_DOWNLINK_RATE AS INT64)) +
    SUM(CAST(DATA_VOLUME_GPRS_DOWNLINK_NORATE AS INT64)) +
    SUM(CAST(DATA_VOLUME_GPRS_UPLINK_5G AS INT64)) +
    SUM(CAST(DATA_VOLUME_GPRS_DOWNLINK_5G AS INT64)) AS TRAFICO_DATOS_DIARIO

  FROM `datalake-project-dev.usage_curated.mobile_v002_data_traffic`

  WHERE dt BETWEEN @dt_inicio AND @dt_fin
    AND CAST(DATE_EVENT AS STRING) BETWEEN @fecha_evento_inicio AND @fecha_evento_fin
    AND STARTS_WITH(CAST(SERVED_IMSI AS STRING), '73003')

    AND CAST(SERVED_MSISDN AS STRING) IN (
      SELECT CAST(PCS AS STRING)
      FROM `analytics-project-dev.analytics_studies_dev.TMP_PREFILTER_SILENT_SALES`
    )

  GROUP BY FECHA, PCS
)


-- =========================
-- 4. JOIN FINAL (MULTIFUENTE)
-- =========================
SELECT

  COALESCE(s.FECHA, e.FECHA, d.FECHA) AS FECHA,
  COALESCE(s.PCS, e.PCS, d.PCS) AS PCS,

  s.DURACION_DIARIA_LLAMADAS_SALIENTES,
  e.DURACION_DIARIA_LLAMADAS_ENTRANTES,
  d.TRAFICO_DATOS_DIARIO

FROM trafico_llamadas_salientes s

FULL OUTER JOIN trafico_llamadas_entrantes e
  ON s.FECHA = e.FECHA AND s.PCS = e.PCS

FULL OUTER JOIN trafico_datos d
  ON COALESCE(s.FECHA, e.FECHA) = d.FECHA
  AND COALESCE(s.PCS, e.PCS) = d.PCS

ORDER BY FECHA, PCS;
