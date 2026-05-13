# practica_8_urv
# Comparador de Productos IA

Aplicación web desarrollada con Streamlit y Groq que utiliza modelos LLM para generar comparativas inteligentes entre productos de forma visual, estructurada y fácil de interpretar.

El sistema analiza diferentes productos según criterios personalizados y genera:

- Evaluaciones objetivas
- Pros y contras
- Puntuaciones detalladas
- Resumen comparativo
- Recomendación final del mejor producto

---

# Vista previa

Compara productos como:

- iPhone vs Samsung
- Portátiles gaming
- Auriculares inalámbricos
- Coches eléctricos
- Cámaras fotográficas
- Cualquier categoría de productos

La IA genera automáticamente una comparativa estructurada en JSON y la renderiza con una interfaz moderna en Streamlit.

---

# Tecnologías utilizadas

- Python
- Streamlit
- Groq API
- Modelo LLaMA 3.3 70B
- Pandas
- JSON

---

# Características principales

- Comparación dinámica entre 2 y 4 productos  
-  Criterios personalizados de evaluación  
-  Prompt engineering avanzado  
-  Respuesta estructurada en JSON  
-  Interfaz moderna y responsive  
-  Visualización de puntuaciones con barras  
-  Pros y contras por producto  
-  Tabla resumen comparativa  
-  Manejo defensivo de errores JSON  
-  IA optimizada para respuestas consistentes

---

# Técnicas de Prompt Engineering aplicadas

El proyecto implementa varias técnicas modernas de prompting:

- **Role Prompting**  
  El modelo actúa como un experto analista de productos.

- **Structured Output**  
  Se fuerza una salida JSON estricta y parseable.

- **Low Temperature (0.3)**  
  Reduce respuestas inconsistentes y mejora estabilidad.

- **Dynamic Prompting**  
  Los criterios de evaluación cambian dinámicamente según el usuario.

- **Defensive Parsing**  
  Limpieza automática de respuestas incorrectamente formateadas.

---

# Instalación
## 1. Clonar el repositorio

```bash
git clone https://github.com/MSNilDev/practica_8_urv.git

cd practica_8_urv
```

## 2. En la terminal
```bash
python -m venv .venv
```

## 3. Activa el environment
```bash
# Windows command prompt
.venv\Scripts\activate.bat

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS and Linux
source .venv/bin/activate
```

## 4. Instalar Streamlit en el environment
```bash
pip install streamlit
```

## 5. Ejecuta la app
```bash
python -m streamlit run app.py
```
---
# TODO KEY Necesaria
Será necesario el uso de una GROQ_API_KEY. 
Para ello, genera una carpeta .streamlit que contenga un archivo secrets.toml
En este archivo se define la GROQ_API_KEY="XXXXXX"
