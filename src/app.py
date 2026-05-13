import streamlit as st
import json
from groq import Groq


# ── config de pagina ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Comparador de Productos IA",
    layout="wide"
)


# ── estilos CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Sora', sans-serif; }
    .main { background-color: #0f1117; }

    h1 { color: #ffffff; font-weight: 700; }
    h2, h3 { color: #e0e0e0; }

    .product-card {
        background: linear-gradient(135deg, #0a1f2a, #0f2b35);
        border: 1px solid #164e5a;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }

    .winner-banner {
        background: linear-gradient(90deg, #06b6d4, #0e7490);
        color: white;
        padding: 14px 24px;
        border-radius: 10px;
        font-size: 1.2em;
        font-weight: 700;
        text-align: center;
        margin: 16px 0;
    }

    .score-badge {
        display: inline-block;
        background: #06b6d4;
        color: white;
        border-radius: 20px;
        padding: 3px 12px;
        font-weight: 600;
        font-size: 0.9em;
    }

    .pro-item {
        color: #67e8f9;
        margin: 4px 0;
    }

    .con-item {
        color: #f87171;
        margin: 4px 0;
    }

    .criteria-tag {
        display: inline-block;
        background: #0c2a33;
        color: #a5f3fc;
        border-radius: 6px;
        padding: 2px 10px;
        margin: 3px;
        font-size: 0.85em;
    }

    .stButton > button {
        background: linear-gradient(90deg, #06b6d4, #0891b2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 28px;
        font-size: 1em;
        font-weight: 600;
        width: 100%;
        cursor: pointer;
        transition: .2s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #0891b2, #0e7490);
        transform: translateY(-1px);
        box-shadow: 0 0 18px rgba(34,197,94,.25);
    }
</style>
""", unsafe_allow_html=True)


# ── cliente Groq ──────────────────────────────────────────────────────────────
client = Groq(api_key=st.secrets["GROQ_API_KEY"])


# ── prompt engineering ────────────────────────────────────────────────────────
SYSTEM_PROMPT = """Eres un experto analista de productos y consumidor avanzado especializado en comparativas objetivas y análisis estructurados.

Tu objetivo es evaluar productos de forma clara, equilibrada y útil para la toma de decisiones.

INSTRUCCIONES ESTRICTAS:
- Responde ÚNICAMENTE con un objeto JSON válido.
- No añadas texto adicional, explicaciones, markdown, comentarios ni bloques de código.
- El JSON debe seguir EXACTAMENTE esta estructura y mantener todas las propiedades indicadas:

{
  "productos": [
    {
      "nombre": "Nombre del producto",
      "puntuacion_global": 8.5,
      "criterios": {
        "Calidad": {"puntuacion": 9, "comentario": "..."},
        "Precio": {"puntuacion": 7, "comentario": "..."},
        "Durabilidad": {"puntuacion": 8, "comentario": "..."}
      },
      "pros": ["Pro 1", "Pro 2", "Pro 3"],
      "contras": ["Contra 1", "Contra 2"]
    }
  ],
  "ganador": "Nombre del producto ganador",
  "justificacion_ganador": "Explicación breve de por qué gana",
  "resumen_comparativa": "Párrafo de 2-3 frases resumiendo la comparativa"
}

REGLAS DE EVALUACIÓN:
- Las puntuaciones deben estar entre 1 y 10.
- Usa decimales solo cuando aporten precisión real.
- La "puntuacion_global" debe ser coherente con los criterios evaluados.
- Adapta dinámicamente los criterios según los indicados por el usuario.
- Si el usuario no especifica criterios, utiliza criterios relevantes para la categoría del producto.
- Mantén un enfoque objetivo, neutral y equilibrado.
- Si no tienes información suficiente para evaluar un criterio, asigna una puntuación prudente (ej: 5) y comenta la falta de datos.
- Si un producto no es válido o no tiene relación con los criterios, indícalo claramente en la sección de contras y asigna un 1 en la puntuación global.
- Destaca ventajas y desventajas reales y relevantes.
- Los comentarios de cada criterio deben ser breves, específicos y útiles.
- Evita afirmaciones absolutas o exageradas.
- No inventes especificaciones técnicas, datos numéricos o características no verificables.
- Si falta información sobre algún aspecto, indícalo de forma prudente sin asumir datos.
- El ganador debe justificarse comparando rendimiento global, relación calidad-precio o adecuación al uso esperado.
- El resumen final debe sintetizar las principales diferencias y orientar rápidamente al usuario.

VALIDACIÓN OBLIGATORIA:
- La respuesta debe ser JSON válido y parseable.
- No incluyas propiedades adicionales.
- No elimines propiedades existentes.
- Mantén exactamente los nombres de las claves definidas en la estructura.
"""


def construir_prompt_usuario(productos, criterios, contexto):
    """
    Técnica: Prompt estructurado con contexto + Few-shot implícito en el system prompt.
    Se especifica claramente qué comparar y bajo qué criterios.
    """
    criterios_str = ", ".join(criterios) if criterios else "Calidad, Precio, Durabilidad, Relación calidad-precio"
    contexto_str = f"Contexto adicional: {contexto}" if contexto else ""

    return f"""Compara los siguientes productos:
{chr(10).join(f'- {p}' for p in productos)}

Criterios de comparación: {criterios_str}
{contexto_str}

Devuelve el JSON de comparación siguiendo exactamente el formato indicado."""

def llamar_llm(productos, criterios, contexto):
    """Llama a Groq con el prompt construido y devuelve el JSON parseado."""
    prompt_usuario = construir_prompt_usuario(productos, criterios, contexto)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_usuario}
        ],
        temperature=0.1,   # con una temperatura baja, las respuestas son mejores, es decir mas consistentes y estructuradas
        max_tokens=2000,
    )

    raw = response.choices[0].message.content.strip()

    # limpieza defensiva por si el modelo añade backticks...
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return json.loads(raw)


# ── funciones de renderizado ──────────────────────────────────────────────────
def render_puntuacion_barra(puntuacion, max_val=10):
    pct = int((puntuacion / max_val) * 100)
    color = "#67e8f9" if puntuacion >= 7 else "#f59e0b" if puntuacion >= 5 else "#f87171"
    return f"""
    <div style="background:#1e2130; border-radius:6px; height:10px; margin:4px 0;">
        <div style="background:{color}; width:{pct}%; height:10px; border-radius:6px;"></div>
    </div>
    """

def render_producto(producto):
    nombre = producto["nombre"]
    puntuacion = producto["puntuacion_global"]
    criterios = producto.get("criterios", {})
    pros = producto.get("pros", [])
    contras = producto.get("contras", [])

    st.markdown(f"""
    <div class="product-card">
        <h3 style="margin:0 0 8px 0;">{nombre}</h3>
        <span class="score-badge"> {puntuacion}/10</span>
    </div>
    """, unsafe_allow_html=True)

    # criterios con barras
    if criterios:
        st.markdown("**Criterios de evaluación:**")
        for criterio, datos in criterios.items():
            col_a, col_b = st.columns([1, 3])
            with col_a:
                st.markdown(f"<small>{criterio}</small>", unsafe_allow_html=True)
            with col_b:
                st.markdown(
                    render_puntuacion_barra(datos["puntuacion"]) +
                    f"<small style='color:#94a3b8'>{datos['comentario']}</small>",
                    unsafe_allow_html=True
                )

    # pros y contras
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Pros**")
        for p in pros:
            st.markdown(f"<div class='pro-item'>+ {p}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("**Contras**")
        for c in contras:
            st.markdown(f"<div class='con-item'>− {c}</div>", unsafe_allow_html=True)

    st.markdown("---")


# ── interfaz principal ────────────────────────────────────────────────────────
st.markdown("# Asistente de Comparación de Productos")
st.markdown("""
<p style="color:#cbd5e1; font-size:1rem; margin-top:-8px;">
    Fundació URV · Microcredencial AI Foundations · Trabajo Práctico · Reto 8
</p>

<p style="color:#a5f3fc; font-size:0.9rem; margin-top:-10px;">
    Nil Miras Sánchez y Marius Mihai Urcan
</p>

<p style="color:#94a3b8; font-size:0.85rem; font-style:italic; margin-top:-6px;">
    Impulsado por IA generativa · Groq + LLaMA 3.3 70B
</p>
""", unsafe_allow_html=True)
st.markdown("---")


# sidebar, config
with st.sidebar:
    st.markdown("## Configuración")

    num_productos = st.slider("Nr de productos a comparar", 2, 4, 2)

    st.markdown("### Criterios de comparación")
    criterios_default = ["Calidad", "Precio", "Durabilidad", "Relación calidad-precio"]
    criterios_opcionales = ["Diseño", "Facilidad de uso", "Soporte técnico", "Sostenibilidad", "Rendimiento"]
    criterios_extra = st.multiselect("Añade criterios adicionales", criterios_opcionales)
    criterios_finales = criterios_default + criterios_extra

    st.markdown("### Criterios seleccionados:")
    for c in criterios_finales:
        st.markdown(f"<span class='criteria-tag'>{c}</span>", unsafe_allow_html=True)

    st.markdown("### Prompt Engineering aplicado")
    st.markdown("""
<div style="background:#0c2a33; border:1px solid #06b6d4; border-radius:8px; padding:14px; margin-top:4px;">
    <p style="color:#a5f3fc; font-weight:600; margin:0 0 8px 0;">Técnicas utilizadas:</p>
    <p style="color:#67e8f9; margin:4px 0;">● <b>Role prompting</b>: el modelo actúa como experto analista</p>
    <p style="color:#67e8f9; margin:4px 0;">● <b>Output estructurado</b>: se fuerza respuesta en JSON</p>
    <p style="color:#67e8f9; margin:4px 0;">● <b>Temperature baja (0.1)</b>: mayor consistencia</p>
    <p style="color:#67e8f9; margin:4px 0;">● <b>Prompt dinámico</b>: se adapta a criterios del usuario</p>
</div>
""", unsafe_allow_html=True)


# area principal, inputs de productos
st.markdown("## Introduce los productos")

productos_input = []
cols = st.columns(num_productos)
for i, col in enumerate(cols):
    with col:
        producto = st.text_input(
            f"Producto {i+1}",
            placeholder=f"Ej: iPhone 15, Samsung Galaxy S24...",
            key=f"producto_{i}"
        )
        productos_input.append(producto)

contexto = st.text_area(
    "Contexto adicional (opcional)",
    placeholder="Ej: busco el mejor para fotografía con un presupuesto de 800€",
    height=80
)


# boton de comparacion
if st.button("Comparar productos con IA"):
    productos_validos = [p.strip() for p in productos_input if p.strip()]

    if len(productos_validos) < 2:
        st.warning("Introduce al menos 2 productos para comparar.")
    else:
        with st.spinner("Analizando productos con IA..."):
            try:
                resultado = llamar_llm(productos_validos, criterios_finales, contexto)

                st.markdown("---")
                st.markdown("## Resultados de la comparativa")

                # banner ganador
                ganador = resultado.get("ganador", "")
                justificacion = resultado.get("justificacion_ganador", "")
                st.markdown(f"""
                <div class="winner-banner">
                    Mejor opción: {ganador}
                </div>
                <p style="text-align:center; color:#94a3b8; margin-top:-8px;">{justificacion}</p>
                """, unsafe_allow_html=True)

                # resumen
                resumen = resultado.get("resumen_comparativa", "")
                if resumen:
                    st.markdown(f"""
                    <div style="background:#0c2a33; border:1px solid #06b6d4; border-radius:8px; padding:14px; color:#a5f3fc;">
                        {resumen}
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("## Análisis detallado por producto")

                # tarjetas de productos
                for producto in resultado.get("productos", []):
                    render_producto(producto)

                # tabla comparativa de puntuaciones
                st.markdown("## Tabla resumen de puntuaciones")
                tabla_data = {}
                for producto in resultado.get("productos", []):
                    nombre = producto["nombre"]
                    tabla_data[nombre] = {"Global": producto["puntuacion_global"]}
                    for criterio, datos in producto.get("criterios", {}).items():
                        tabla_data[nombre][criterio] = datos["puntuacion"]

                if tabla_data:
                    import pandas as pd
                    df = pd.DataFrame(tabla_data).T
                    st.dataframe(df.style.format("{:.2f}").highlight_max(axis=0, color="#0c2a33"),use_container_width=True)

            except json.JSONDecodeError:
                st.error("Error al parsear la respuesta del modelo. Inténtalo de nuevo.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# footer
st.markdown("---")
