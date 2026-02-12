
import streamlit as st
import pandas as pd
from io import BytesIO

# Configuración
st.set_page_config(page_title="CLL-CARE App", layout="wide")

# CSS sin sangrías para evitar error de visualización
st.markdown("""
<style>
.exercise-card {
    background-color: white;
    padding: 1.5rem;
    border-radius: 1rem;
    border: 1px solid #f1f5f9;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
}
.clinical-badge {
    font-size: 0.6em;
    font-weight: 800;
    color: #2563eb;
    text-transform: uppercase;
    background: #eff6ff;
    padding: 2px 8px;
    border-radius: 999px;
}
</style>
""", unsafe_allow_html=True)

# Datos
EXERCISES = {
    'w_walk_mob': {'nombre': 'Caminar + Movilidad', 'desc': 'Marcha suave con círculos de hombros.', 'img': 'https://img.freepik.com/premium-vector/man-walking-icon-vector-illustration_609277-2856.jpg?w=400', 'parte': 'Calentamiento', 'rpe': 6},
    'w_sts': {'nombre': 'Sit-to-Stand', 'desc': 'Levantarse de silla sin manos.', 'img': 'https://cdn-icons-png.flaticon.com/512/3048/3048383.png', 'parte': 'Calentamiento', 'rpe': 6},
    'r_sq_body': {'nombre': 'Sentadilla', 'desc': 'Controlar bajada de cadera.', 'img': 'https://cdn-icons-png.flaticon.com/512/4721/4721102.png', 'parte': 'Resistencia', 'rpe': 7},
    'r_bench_db': {'nombre': 'Press Mancuernas', 'desc': 'Empuje desde el pecho.', 'img': 'https://cdn-icons-png.flaticon.com/512/2548/2548537.png', 'parte': 'Resistencia', 'rpe': 7},
}

SESSIONS = [
    {'id': 1, 'nombre': "Sesión 1: Estabilidad Base", 'ejercicios': ['w_walk_mob', 'r_sq_body', 'r_bench_db']},
    {'id': 2, 'nombre': "Sesión 2: Potencia", 'ejercicios': ['w_sts', 'r_sq_body', 'r_bench_db']},
]

if 'rms' not in st.session_state: st.session_state.rms = {}

# Sidebar
page = st.sidebar.radio("Navegación", ["Perfil", "Protocolos", "Cargas"])

if page == "Perfil":
    st.title("Perfil del Paciente")
    st.text_input("Nombre")
    st.info("Meta Diaria: Caminar 60 min.")

elif page == "Cargas":
    st.title("Gestión de RM")
    for k, v in EXERCISES.items():
        if v['parte'] == 'Resistencia':
            st.session_state.rms[k] = st.number_input(f"1RM {v['nombre']} (kg)", value=float(st.session_state.rms.get(k, 0.0)))

elif page == "Protocolos":
    st.title("Protocolos de Entrenamiento")
    sid = st.selectbox("Elegir Sesión", [1, 2], format_func=lambda x: f"Sesión {x}")
    session = SESSIONS[sid-1]
    
    cols = st.columns(3)
    for i, eid in enumerate(session['ejercicios']):
        ex = EXERCISES[eid]
        with cols[i % 3]:
            rm = st.session_state.rms.get(eid, 0.0)
            carga = f"{rm * 0.7:.1f} kg" if rm > 0 else "Peso Corp."
            # Sin sangría en el markdown
            st.markdown(f"""
<div class="exercise-card">
<img src="{ex['img']}" style="width:100%; height:120px; object-fit:contain; margin-bottom:10px;">
<div class="clinical-badge">{ex['parte']}</div>
<div style="font-weight:bold; margin-top:5px;">{ex['nombre']}</div>
<div style="font-size:0.8em; color:#666; margin-bottom:10px;">{ex['desc']}</div>
<div style="display:flex; justify-content:space-between; font-size:0.8em; font-weight:bold; border-top:1px solid #eee; padding-top:10px;">
<span>CARGA: {carga}</span>
<span>RPE: {ex['rpe']}/10</span>
</div>
</div>
""", unsafe_allow_html=True)
