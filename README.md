# 📊 Redefinición KPI Silentes – KPI Validity & Behavioral Drift Analysis

Proyecto analítico corporativo desarrollado en la industria de telecomunicaciones, enfocado en la validación y redefinición del KPI de ventas de baja calidad ("Silentes"), utilizando un modelo de clasificación Decision Tree para evaluar la efectividad del indicador y su evolución en el tiempo.

---

## 📌 1. Business Context

El KPI Silentes era utilizado por el área comercial para identificar activaciones sin tráfico de voz ni datos dentro de los primeros días posteriores a la venta, con el objetivo de detectar ventas de baja calidad susceptibles de ser descomisionadas dentro del esquema de comisiones comerciales.

El análisis surge porque el KPI había permanecido sin cambios durante varios años, mientras los patrones comerciales evolucionaban.

> ¿La definición histórica del KPI "Silentes" sigue siendo efectiva para detectar ventas de baja calidad o han cambiado los patrones de comportamiento del cliente?

---

## 📋 2. Definición del KPI Original

El KPI de “Silentes” fue definido históricamente como:

> Clientes (PCS: números telefónicos) sin tráfico de voz ni datos dentro de los 21 días posteriores a la venta.

Con el tiempo se identificaron riesgos potenciales:

- Los equipos comerciales pueden adaptar su comportamiento a métricas conocidas  
- Las definiciones rígidas de KPI pueden perder capacidad explicativa en el tiempo  
- La relación entre activación y uso real puede evolucionar  

---

## 📊 3. Current KPI Performance (Baseline)

Este bloque muestra el desempeño del KPI “Silentes” bajo su definición original, utilizado como baseline para evaluar su capacidad de identificación de ventas de baja calidad.

El análisis se basa en la matriz de confusión, la cual compara las predicciones del KPI contra el comportamiento real observado en red.

---

### 🔢 Confusion Matrix

La siguiente tabla compara las predicciones del KPI con el comportamiento real observado en la red:

| Metric          | Value |
|----------------|------:|
| True Positives | 1776 |
| False Positives| 873 |
| False Negatives| 17346 |
| True Negatives | 35226 |

**¿Qué significa cada caso?**

- **True Positives (1.776):** ventas que el KPI marcó como “silentes” y efectivamente no tuvieron uso de voz ni datos.  
- **False Positives (873):** ventas que el KPI marcó como “silentes”, pero que sí mostraron uso real (errores del KPI).  
- **False Negatives (17.346):** ventas que sí eran de baja calidad, pero el KPI no las detectó.  
- **True Negatives (35.226):** ventas correctamente no marcadas como silentes, ya que sí presentaron uso.

---

### 📈 Performance Metrics

| Metric     | Value |
|-----------|------:|
| Precision | 67% |
| Recall    | 9.3% |

**Interpretación:**

- El KPI es en un ~67% preciso: cuando marca una venta como de baja calidad, en la mayoría de los casos efectivamente lo es.  

- Sin embargo, su sensibilidad es baja: no logra detectar una gran proporción de las ventas de baja calidad existentes (muchas quedan fuera del KPI).  

- En la práctica, esto significa que el KPI funciona bien como mecanismo de control (evita errores al etiquetar), pero es limitado para capturar completamente el problema de ventas de baja calidad.

---

### 📉 Visual Overview

<p align="center">
  <img src="4.Outputs/current_kpi_performance.PNG" width="600">
</p>

## 🎯 4. Objetivo del Proyecto

- Evaluar la validez del KPI “Silentes”  
- Analizar si las variables base siguen siendo discriminantes  
- Detectar drift en el comportamiento de usuarios  
- Mejorar la interpretabilidad del indicador  

---

## 🧠 5. Hipótesis de Trabajo

- El KPI sigue siendo válido, pero no necesariamente óptimo  
- El comportamiento de red permite validar su robustez  
- Existen variables adicionales con poder explicativo relevante  
- El comportamiento temprano del cliente es clave para la validación del KPI    


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
README.md
│
├── 1. Business Context
│
├── 2. Current KPI Performance
│
├── 3. End-to-End Pipeline
│
├── 4. Machine Learning Validation
│
├── 5. Results
│
├── 6. Repository Structure
│
└── Código
