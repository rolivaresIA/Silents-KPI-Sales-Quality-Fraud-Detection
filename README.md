# Redefinición KPI Silentes – Sales Quality & Fraud Detection

Pipeline analítico end-to-end para la detección de **ventas de baja calidad (“silentes”)**, definido como clientes (PCS) sin generación de tráfico de red (voz o datos) dentro de los primeros 21 días posteriores a la activación.

El objetivo del proyecto es transformar un KPI comercial tradicional basado en registros de venta hacia un enfoque basado en **comportamiento real de uso de red**, permitiendo identificar activaciones con baja o nula adopción del servicio.

---

## 📑 Contenido

- 📋 Business Context
- 🎯 Objective
- ⚙️ Methodology
- 🧠 Data Processing & Feature Engineering
- 🌲 Modeling Approach (Decision Tree)
- 📊 Business Impact
- 📈 Key Insights
- 🛠️ Tech Stack
- 📁 Repository Structure
- 📌 Next Improvements

---

## 📋 Business Context

En la operación comercial de telecomunicaciones, existe la necesidad de validar la calidad real de las ventas realizadas por distintos canales y ejecutivos.

Sin embargo, los sistemas tradicionales de reporte se basan únicamente en la activación del servicio, sin considerar si el cliente realmente utiliza el producto.

Esto genera un problema crítico:
- Ventas activadas sin uso real del servicio
- Dificultad para auditar calidad comercial
- Posible sobreestimación de performance de canales

Este proyecto nace para resolver esa brecha mediante análisis de comportamiento real de red.

---

## 🎯 Objective

- Identificar ventas con baja o nula adopción del servicio (“silentes”)
- Definir una métrica objetiva de calidad basada en uso real de red
- Detectar patrones de comportamiento post-activación
- Mejorar la priorización de auditoría comercial
- Estandarizar un KPI de calidad de ventas basado en datos de consumo

---

## ⚙️ Methodology

### Definición de KPI “Silente”

Se define como cliente silente a aquel PCS que no presenta actividad en:

- Llamadas salientes
- Llamadas entrantes
- Tráfico de datos

dentro de una ventana de **21 días post activación**.

> Esta ventana se selecciona debido a que aproximadamente el 90% de la base activa comienza a generar tráfico dentro de este periodo.

---

## 🧠 Data Processing & Feature Engineering

### Fuentes de datos

- Altas comerciales (ventas)
- Tráfico de voz (entrante / saliente)
- Tráfico de datos móviles

### Procesamiento

- Limpieza y estandarización de altas comerciales
- Integración con BigQuery (GCP)
- Extracción de tráfico diario por PCS
- Construcción de ventana temporal post-alta (21 días)
- Generación de variables de comportamiento:

  - actividad diaria post alta
  - días con tráfico = 0
  - acumulación de tráfico en ventana
  - segmentación por tipo de canal

---

## 🌲 Modeling Approach (Decision Tree)

Se utilizó un modelo basado en **árboles de decisión** para:

- Identificar reglas de segmentación interpretables
- Determinar variables con mayor impacto en comportamiento silente
- Generar reglas de priorización comercial basadas en comportamiento real

Ejemplo conceptual de reglas generadas:

- PCS sin tráfico en días 1–7 → alto riesgo de ser silente
- PCS sin datos móviles en ventana temprana → alta probabilidad de baja adopción
- Canales específicos asociados a mayor concentración de silentes

---

## 📊 Business Impact

- Redefinición del KPI de calidad de ventas basado en comportamiento real de red
- Identificación de segmento crítico de clientes sin adopción de servicio dentro de ventana de 21 días
- Mejora en la capacidad de auditoría comercial mediante detección temprana de baja actividad
- Estandarización de un enfoque basado en datos de uso en lugar de solo activación

> 📌 [Aquí puedes agregar porcentaje de universo detectado cuando lo tengas]
> Ejemplo: “~X% de las activaciones presentan comportamiento silente en ventana 21 días”

---

## 📈 Key Insights

- El comportamiento de adopción se concentra principalmente dentro de los primeros 21 días
- La ausencia de tráfico en este periodo es un fuerte indicador de baja calidad de venta
- La integración entre ventas + tráfico de red permite evaluar calidad real de activación

---

## 🛠️ Tech Stack

- Python (Pandas, NumPy)
- Google BigQuery
- SQL
- Google Cloud Platform (GCP)
- Jupyter Notebook
- Excel / Data ingestion pipelines

---

## 📁 Repository Structure

```text
├── notebooks/
│   ├── silentes_calculation.ipynb
│
├── presentation/
│   ├── Redefinicion_Silentes.pptx
│
├── sql/
│   ├── traffic_extraction.sql
│
├── data/
│   ├── processed_dataset.csv
│
└── README.md
