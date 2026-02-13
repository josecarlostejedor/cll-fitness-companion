
import streamlit as st
import pandas as pd
import os
from io import BytesIO
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Configuración inicial
st.set_page_config(page_title="CLL-CARE ADMIN", layout="wide")

# Función para cargar datos desde el Excel de GitHub
@st.cache_data
def load_excel_data():
    excel_path = "data/ejercicios.xlsx"
    if os.path.exists(excel_path):
        return pd.read_excel(excel_path)
    else:
        return None

# Estilos CSS
st.markdown("""
<style>
.stApp { background-color: #f8fafc; }
.main-card {
    background-color: white;
    padding: 2rem;
    border-radius: 1.5rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.ex-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 1rem;
    border: 2px solid #f1f5f9;
}
</style>
""", unsafe_allow_html=True)

# Lógica de la aplicación
st.sidebar.title("CLL-CARE PANEL")
menu = st.sidebar.radio("Navegación", ["Panel de Control", "Visor de Ejercicios", "Configuración de Cargas"])

# Intentar cargar el excel
df_ejercicios = load_excel_data()

if menu == "Panel de Control":
    st.title("🚀 Configuración del Sistema")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("📂 **Estado del Excel:** " + ("✅ Conectado (`data/ejercicios.xlsx`)" if df_ejercicios is not None else "⚠️ No encontrado"))
    with col2:
        st.info("🖼️ **Estado de Imágenes:** Verificando carpeta `public/images/`...")

    st.markdown("---")
    st.subheader("Información del Paciente")
    nombre = st.text_input("Nombre del Paciente", "Juan Pérez")
    
    st.warning("🚨 **Obligación Diaria:** Caminar 60 minutos ininterrumpidos.")

elif menu == "Visor de Ejercicios":
    st.title("🏋️ Previsualización de Sesiones")
    
    if df_ejercicios is not None:
        st.dataframe(df_ejercicios)
        
        # Simulación de tarjetas basadas en el Excel
        st.subheader("Vista Previa de Tarjetas")
        cols = st.columns(3)
        for index, row in df_ejercicios.head(6).iterrows():
            with cols[index % 3]:
                # La ruta de la imagen se construye dinámicamente
                img_path = f"public/images/{row['imagen']}"
                st.markdown(f"### {row['nombre']}")
                if os.path.exists(img_path):
                    st.image(img_path, use_container_width=True)
                else:
                    st.error(f"Falta: {row['imagen']}")
                st.write(f"**Dosis:** {row['plan']}")
    else:
        st.error("Por favor, sube el archivo `ejercicios.xlsx` a la carpeta `data/` en tu repositorio de GitHub.")

elif menu == "Configuración de Cargas":
    st.title("⚙️ Cálculo de 70% 1RM")
    st.write("Esta sección sincroniza los valores del Excel con la prescripción clínica.")
