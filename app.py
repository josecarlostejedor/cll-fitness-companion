
import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="CLL-Care Fitness",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS con enfoque clínico
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        background-color: #2563eb;
        color: white;
    }
    .exercise-card {
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        display: flex;
        flex-direction: column;
    }
    .phase-header {
        color: #1e293b;
        border-left: 6px solid #2563eb;
        padding-left: 15px;
        margin: 30px 0 15px 0;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 1.2em;
    }
    .stat-label {
        font-size: 0.65em;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
    }
    .stat-value {
        font-size: 1em;
        font-weight: 700;
        color: #1e293b;
    }
    .clinical-info {
        font-size: 0.8em;
        color: #64748b;
        background-color: #f1f5f9;
        padding: 10px;
        border-radius: 8px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Catálogo total de ejercicios (Actualizado con imágenes neutras)
EXERCISES = {
    'w_walk_mob': {'nombre': 'Caminar + Movilidad Articular', 'descripcion': 'Marcha suave controlada moviendo hombros, rodillas y tobillos.', 'tipo': 'aeróbico', 'imagen': 'https://images.unsplash.com/photo-1571019613531-fbea97794452?w=400', 'agonistas': 'Completo', 'sinergistas': 'Pulmones', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x Continuo', 'duracion': '2 min'},
    'w_balance': {'nombre': 'Equilibrio Asistido', 'descripcion': 'Mantenerse sobre una pierna con apoyo cercano (silla/pared).', 'tipo': 'movilidad', 'imagen': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400', 'agonistas': 'Glúteo medio', 'sinergistas': 'Cuádriceps', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 x 30s/lado'},
    'w_pushups_wall': {'nombre': 'Empuje en Pared', 'descripcion': 'Flexiones de brazos apoyados en pared.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1599901860904-17e6ed7083a0?w=400', 'agonistas': 'Pectoral', 'sinergistas': 'Tríceps', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 15-20'},
    'w_squat_wall': {'nombre': 'Isometría en Pared', 'descripcion': 'Espalda apoyada bajando ligeramente.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1566241142559-40e1bfc26ebc?w=400', 'agonistas': 'Cuádriceps', 'sinergistas': 'Core', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 60s'},
    'r_sq_body': {'nombre': 'Sentadilla Funcional', 'descripcion': 'Simular sentarse en silla con control.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1574680096145-d05b474e2158?w=400', 'agonistas': 'Tren inferior', 'sinergistas': 'Core', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_rdl': {'nombre': 'Peso Muerto Controlado', 'descripcion': 'Bisagra de cadera espalda recta.', 'tipo': 'sobrecarga', 'imagen': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400', 'agonistas': 'Isquios', 'sinergistas': 'Glúteo', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_bench_bar': {'nombre': 'Press de Pecho', 'descripcion': 'Empuje vertical desde el pecho.', 'tipo': 'barra olímpica', 'imagen': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400', 'agonistas': 'Pectoral', 'sinergistas': 'Deltoides', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'e_walk': {'nombre': 'Paseo Recuperación', 'descripcion': 'Ritmo lento y respiración profunda.', 'tipo': 'aeróbico', 'imagen': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=400', 'agonistas': 'Cardiovascular', 'sinergistas': 'Todo el cuerpo', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 x 3 min'},
    'e_cuad': {'nombre': 'Estiramiento Cuádriceps', 'descripcion': 'Talón al glúteo suavemente.', 'tipo': 'movilidad', 'imagen': 'https://images.unsplash.com/photo-1552196563-55cd4e45efb3?w=400', 'agonistas': 'Cuádriceps', 'sinergistas': 'Hombro', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 x 30s/lado'},
}

SESSIONS = [
    {'id': 1, 'nombre': "Sesión 1: Movilidad y Fuerza Base", 'ejercicios': ['w_walk_mob', 'w_balance', 'w_pushups_wall', 'w_squat_wall', 'r_sq_body', 'r_rdl', 'r_bench_bar', 'e_walk', 'e_cuad']}
]

if 'rms' not in st.session_state: st.session_state.rms = {}
if 'profile' not in st.session_state: st.session_state.profile = {'nombre': '', 'apellidos': '', 'sexo': 'Hombre', 'edad': 60}

st.sidebar.markdown("<h2 style='color:#2563eb;text-align:center;'>CLL-CARE</h2>", unsafe_allow_html=True)
page = st.sidebar.radio("MENÚ CLÍNICO", ["📋 Perfil", "🏋️ Protocolos", "📈 Evolución"])

if page == "📋 Perfil":
    st.title("Historial del Paciente")
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.session_state.profile['nombre'] = st.text_input("Nombre", st.session_state.profile['nombre'])
        st.session_state.profile['apellidos'] = st.text_input("Apellidos", st.session_state.profile['apellidos'])
        st.session_state.profile['edad'] = st.number_input("Edad", 1, 120, st.session_state.profile['edad'])
    with c2:
        st.info("Objetivo Base: Caminar 60 min cada día para reducir síntomas de fatiga y mejorar el pronóstico.")

elif page == "🏋️ Protocolos":
    st.title("Protocolo de Actividad Física")
    sel_id = st.radio("Siguiente sesión:", [1], format_func=lambda x: SESSIONS[x-1]['nombre'], horizontal=True)
    session = SESSIONS[sel_id-1]
    
    for phase in ['Calentamiento', 'Entrenamiento de Resistencia', 'Enfriamiento']:
        st.markdown(f"<div class='phase-header'>{phase}</div>", unsafe_allow_html=True)
        ex_ids = [eid for eid in session['ejercicios'] if EXERCISES.get(eid, {}).get('parte') == phase]
        cols = st.columns(3)
        for i, eid in enumerate(ex_ids):
            ex = EXERCISES[eid]
            with cols[i % 3]:
                rm = st.session_state.rms.get(eid, 0)
                carga = f"{rm * 0.7:.1f} kg" if rm > 0 else "Peso Corp."
                st.markdown(f"""
<div class='exercise-card'>
<img src='{ex['imagen']}' style='width: 100%; height: 120px; object-fit: cover; border-radius: 8px; margin-bottom: 15px;'>
<h4 style='margin: 0; font-size: 1em; color: #1e293b;'>{ex['nombre']}</h4>
<p style='color: #64748b; font-size: 0.75em; font-style: italic; margin-top: 5px; height: 35px;'>"{ex['descripcion']}"</p>
<div style='display: flex; justify-content: space-between; margin-top: 15px; border-top: 1px solid #f1f5f9; pt: 10px;'>
<div><div class='stat-label'>Plan</div><div class='stat-value' style='font-size:0.8em;'>{ex['plan']}</div></div>
<div><div class='stat-label'>Esfuerzo</div><div class='stat-value' style='font-size:0.8em;'>{ex['rpe']}/10</div></div>
</div>
<div class='clinical-info'>
<b>Músculo:</b> {ex['agonistas']}<br>
<b>Carga:</b> {carga}
</div>
</div>
""", unsafe_allow_html=True)

elif page == "📈 Evolución":
    st.title("Seguimiento de Cargas")
    res = []
    for eid, rm in st.session_state.rms.items():
        if rm > 0:
            res.append({"Ejercicio": EXERCISES[eid]['nombre'], "1RM": f"{rm} kg", "70% (Actual)": f"{rm*0.7:.1f} kg"})
    if res: st.table(pd.DataFrame(res))
    else: st.warning("Pendiente de ajuste inicial de 1RM.")

st.sidebar.markdown("---")
st.sidebar.caption("Siga el nivel RPE indicado para su seguridad.")
