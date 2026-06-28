# Redefinición KPI Silentes – KPI Validity & Behavioral Drift Analysis

Proyecto analítico enfocado en la **evaluación y validación del KPI de “ventas de baja calidad (silentes)”**, con el objetivo de analizar si la definición operacional del indicador sigue siendo efectiva para capturar activaciones con baja adopción de servicio.

El análisis se centra en detectar posibles **desviaciones o adaptación del KPI por parte de los equipos comerciales**, y en evaluar si las variables utilizadas originalmente siguen siendo suficientes para representar calidad real de venta.

---

## 📋 Contexto del Problema

El KPI de “silentes” fue definido históricamente como:

> Clientes (PCS) sin tráfico de voz ni datos dentro de los 21 días posteriores a la activación.

Sin embargo, con el tiempo se identificó un riesgo potencial:

- Los equipos comerciales pueden adaptar su comportamiento a métricas conocidas
- Las definiciones rígidas de KPI pueden perder capacidad explicativa en el tiempo
- La relación entre activación y uso real puede evolucionar

Esto genera la necesidad de responder una pregunta clave:

> ❓ ¿La definición actual del KPI sigue capturando efectivamente las ventas de baja calidad?

---

## 🎯 Objetivo del Proyecto

- Evaluar la validez del KPI “silentes” bajo su definición original
- Analizar si las variables base del KPI siguen siendo discriminantes
- Detectar patrones de comportamiento asociados a activaciones de baja calidad
- Identificar posibles señales de “drift” o adaptación del KPI
- Mejorar la interpretabilidad del indicador mediante análisis de variables

---

## 🧠 Hipótesis de Trabajo

- La definición actual del KPI puede seguir siendo válida, pero no necesariamente óptima
- El comportamiento de red permite validar la robustez del indicador
- Existen variables adicionales que pueden mejorar la capacidad explicativa del KPI
- El comportamiento temprano del usuario es clave para validar calidad de venta

---

## ⚙️ Data Sources

- Altas comerciales (activaciones de clientes)
- Tráfico de voz (entrante y saliente)
- Tráfico de datos móviles

---

## 🔄 Data Pipeline

### 1. Construcción del dataset base
- Integración de altas comerciales con identificador PCS
- Estandarización de fechas de activación

### 2. Integración con comportamiento de red
- Extracción de tráfico desde BigQuery (voz + datos)
- Join temporal por PCS

### 3. Construcción de ventana de análisis
- Seguimiento del comportamiento del cliente en los primeros 21 días post alta

### 4. Generación de variables
- Tráfico acumulado
- Presencia/ausencia de actividad
- Distribución temporal del uso
- Flags de actividad temprana

---

## 🌲 Enfoque Analítico – Decision Tree

Se utilizó un modelo de árbol de decisión como herramienta interpretativa para:

- Evaluar qué variables explican mejor el comportamiento silente
- Analizar la consistencia de la definición original del KPI
- Identificar si la regla de negocio (21 días + ausencia de tráfico) sigue siendo óptima
- Detectar posibles patrones alternativos de segmentación

### Rol del modelo:

> El modelo no busca reemplazar el KPI, sino **evaluar su validez estructural y su capacidad de segmentación**

---

## 📊 Resultados del Análisis

- La definición original del KPI mantiene capacidad de segmentación sobre comportamiento de red
- El comportamiento temprano del usuario es un predictor clave de adopción futura
- Existen variables adicionales que pueden complementar la definición original
- El KPI muestra consistencia, pero con oportunidades de refinamiento

---

## 💡 Impacto de Negocio

- Validación técnica del KPI “silentes” como indicador de calidad de venta
- Mejora en la comprensión de la robustez del indicador en el tiempo
- Identificación de oportunidades de mejora en la definición del KPI
- Apoyo a decisiones de auditoría comercial basadas en evidencia de comportamiento real

---

## 📈 Insight Clave

- La ventana de 21 días sigue siendo un umbral relevante para observar adopción
- La ausencia de tráfico en este periodo sigue siendo un fuerte indicador de baja calidad de venta
- El comportamiento del usuario permite validar y no solo medir el KPI

---

## 🛠️ Tech Stack

- Python (Pandas, NumPy)
- Google BigQuery
- SQL
- Google Cloud Platform (GCP)
- Jupyter Notebook
- Excel / Data ingestion

---

## 📁 Repository Structure

```text
├── notebooks/
│   └── silentes_kpi_validation.ipynb
│
├── presentation/
│   └── KPI_Redefinition_Silentes.pptx
│
├── sql/
│   └── traffic_extraction.sql
│
├── data/
│   └── dataset_processed.csv
│
└── README.md
