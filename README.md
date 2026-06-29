# Redefinición KPI Silentes – KPI Validity & Behavioral Drift Analysis

Proyecto analítico corporativo desarrollado en la industria de telecomunicaciones, enfocado en la validación y redefinición del KPI de ventas de baja calidad ("Silentes"), utilizando un modelo de clasificación Decision Tree para identificar las variables con mayor capacidad predictiva y evaluar si la definición histórica del indicador seguía siendo efectiva.

El KPI Silentes era utilizado por el área comercial para identificar activaciones con baja probabilidad de representar clientes reales o comprometidos con el servicio, constituyendo un indicador clave para el monitoreo de la calidad de las ventas y la detección de posibles prácticas comerciales no deseadas.

El análisis surgió debido a que el KPI había permanecido sin modificaciones durante varios años y existía la hipótesis de que los patrones comerciales habían evolucionado, reduciendo su capacidad para detectar ventas de baja calidad. Mediante técnicas de Machine Learning se evaluó la importancia de las variables originales y se identificaron oportunidades para fortalecer la definición del indicador.

---

## 📋 Contexto del Problema

El KPI de “silentes” fue definido históricamente como:

> Clientes (PCS: Números telefónicos) sin tráfico de voz ni datos dentro de los 21 días posteriores a la venta.

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
│
├── 1. KPI_Operational_Pipeline/
│   ├── silentes_pipeline.py
│   ├── description.md
│
├── 2. Data_Building/
│   ├── altas_loader.py
│   ├── bigquery_queries.sql
│   ├── traffic_engineering.py
│
├── 3. ML_Validation/
│   ├── decision_tree_model.ipynb
│   ├── feature_importance_analysis.ipynb
│
├── 4. Outputs/
│   ├── ppt_presentacion.pdf
│   ├── KPI_validation_results.png
│
└── README.md
