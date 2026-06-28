# Redefinición KPI Silentes – Sales Quality & Behavioral Fraud Detection

Pipeline analítico end-to-end para la redefinición del KPI de **ventas de baja calidad (“silentes”)**, basado en comportamiento real de red (tráfico de voz y datos) dentro de los primeros 21 días posteriores a la activación de un cliente (PCS).

El proyecto surge ante la necesidad de robustecer los indicadores comerciales, debido a que los equipos de venta comenzaron a **adaptarse a la métrica tradicional**, generando posibles distorsiones en la medición de calidad de ventas.

---

## 📋 Contexto del Problema

En el área comercial de telecomunicaciones, la calidad de ventas se medía históricamente mediante la activación del servicio.

Sin embargo, este enfoque presentaba una limitación crítica:

- Los vendedores podían optimizar su comportamiento para cumplir el KPI sin garantizar uso real del servicio
- No existía validación del consumo efectivo del cliente post activación
- Se generaban activaciones con baja o nula adopción del servicio

Con el tiempo, se observó que parte de la fuerza de ventas comenzó a **adaptarse a la métrica existente**, lo que redujo la capacidad del KPI original de reflejar calidad real.

---

## 🎯 Objetivo del Proyecto

- Redefinir el KPI de calidad de ventas utilizando comportamiento real de red
- Detectar clientes con baja o nula adopción del servicio (“silentes”)
- Identificar patrones asociados a activaciones de baja calidad
- Evaluar variables que explican el comportamiento silente
- Mejorar la capacidad de priorización y auditoría comercial

---

## 📌 Definición del KPI – “Silentes”

Se define como cliente silente a todo PCS que cumple:

> ❌ No presenta tráfico de voz (entrante/saliente) ni datos dentro de los 21 días posteriores a la activación

### Justificación de la ventana temporal:
- ~90% de los clientes activos generan tráfico dentro de los primeros 21 días
- La ausencia de actividad en este período es un fuerte indicador de baja adopción

---

## 🧠 Hipótesis de Negocio

- No todo cliente activado representa una venta efectiva
- El comportamiento de red es un mejor proxy de calidad que la activación
- Existen patrones sistemáticos asociados a activaciones de baja calidad
- El KPI tradicional puede ser “optimizado artificialmente” por comportamiento operativo

---

## ⚙️ Data Sources

- **Altas comerciales**
  - Información de activaciones (PCS, canal, vendedor, plan, fecha de alta)

- **Tráfico de voz**
  - Llamadas entrantes y salientes

- **Tráfico de datos**
  - Consumo diario de internet móvil

---

## 🔄 Data Pipeline

### 1. Ingesta de datos
- Carga de altas comerciales desde fuentes internas (Excel / sistemas operacionales)
- Extracción de tráfico de red desde BigQuery (GCP)

### 2. Integración de datos
- Join entre altas y tráfico por identificador PCS
- Alineación temporal por fecha de activación

### 3. Construcción de ventana temporal
- Seguimiento del comportamiento del cliente durante 21 días post alta

### 4. Feature engineering
- Tráfico total diario
- Suma acumulada de tráfico
- Días sin actividad
- Flags de uso (voz / datos)
- Variables temporales post activación

---

## 🌲 Enfoque Analítico (Decision Tree)

Se utilizó un modelo de clasificación basado en **árboles de decisión** como herramienta interpretativa para:

- Identificar variables más relevantes asociadas al comportamiento silente
- Detectar reglas de segmentación simples y accionables
- Evaluar patrones de comportamiento post activación

### Rol del modelo:
Este modelo no se utiliza como sistema predictivo en producción, sino como:

> 🔎 herramienta de interpretación para entender drivers de baja adopción

---

## 📊 Resultados Analíticos

- Identificación de un segmento relevante de clientes sin actividad de red en ventana crítica de 21 días
- Evidencia de que el comportamiento temprano (primeros días post alta) es altamente predictivo de adopción futura
- Validación de que la calidad de venta no puede ser medida únicamente por activación

---

## 💡 Impacto de Negocio

- Redefinición del KPI de ventas hacia un enfoque basado en comportamiento real de red
- Mejora en la capacidad de auditoría de calidad comercial
- Identificación de patrones asociados a activaciones de baja adopción
- Mejora en la priorización de análisis sobre canales y vendedores con mayor concentración de “silentes”

---

## 📈 Insight Clave

- La adopción de servicio se concentra en los primeros 21 días
- La ausencia de tráfico en este período es un indicador robusto de baja calidad de venta
- El comportamiento del cliente es un mejor proxy de calidad que la activación comercial

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
│   └── silentes_analysis.ipynb
│
├── presentation/
│   └── Redefinicion_Silentes.pptx
│
├── sql/
│   └── traffic_extraction.sql
│
├── data/
│   └── processed_dataset.csv
│
└── README.md
