
import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="CLL Fitness Companion",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        font-weight: bold;
    }
    .exercise-card {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .phase-header {
        color: #1e293b;
        border-left: 5px solid #4f46e5;
        padding-left: 15px;
        margin: 20px 0;
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_name=True)

# Datos de Ejercicios (Replicados de data/exercises.ts)
EXERCISES = {
    'w_walk_mob': {'nombre': 'Caminar círculos + Movilidad', 'descripcion': 'Rápido, paso largo, círculos hombros, rodillas, puntillas, lateral trote.', 'tipo': 'aeróbico', 'imagen': 'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?auto=format&fit=crop&q=80&w=400', 'agonistas': 'Cuerpo completo', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x Continuo', 'duracion': '2 min'},
    'w_balance': {'nombre': 'Equilibrio 1 pierna', 'descripcion': 'Mantener posición estable con una pierna elevada.', 'tipo': 'movilidad', 'imagen': 'https://images.unsplash.com/photo-1599901860904-17e6ed7083a0?auto=format&fit=crop&q=80&w=400', 'agonistas': 'Glúteo medio, Cuádriceps', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 x 30s por pierna', 'duracion': '2 min'},
    'w_pushups_wall': {'nombre': 'Flexiones pared/suelo', 'descripcion': 'Empuje horizontal manteniendo alineación.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1598971639058-aba7c11210ee?auto=format&fit=crop&q=80&w=400', 'agonistas': 'Pectoral mayor', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 15-20', 'duracion': '1 min'},
    'w_squat_wall': {'nombre': 'Sentadilla pared', 'descripcion': 'Mantener posición de silla apoyado en pared.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1574680096145-d05b474e2158?auto=format&fit=crop&q=80&w=400', 'agonistas': 'Cuádriceps', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x Isométrico 60s', 'duracion': '1 min'},
    'r_sq_body': {'nombre': 'Sentadilla peso corporal', 'descripcion': 'Flexión rodilla cadera 90 grados.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1566241142559-40e1bfc26ebc?auto=format&fit=crop&q=80&w=400', 'agonistas': 'Cuádriceps, Glúteo', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_rdl': {'nombre': 'Peso muerto rumano', 'descripcion': 'Flexión cadera, espalda recta.', 'tipo': 'sobrecarga', 'imagen': 'https://images.unsplash.com/photo-1534367507873-d2d7e24c797f?auto=format&fit=crop&q=80&w=400', 'agonistas': 'Isquios, Glúteo mayor', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_bench_bar': {'nombre': 'Press banca barra', 'descripcion': 'Empuje barra desde pecho.', 'tipo': 'barra olímpica', 'imagen': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&q=80&w=400', 'agonistas': 'Pectoral', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'e_walk': {'nombre': 'Caminata + respiración', 'descripcion': 'Ritmo suave bajando pulsaciones.', 'tipo': 'aeróbico', 'imagen': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&q=80&w=400', 'agonistas': 'Cuerpo completo', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 x Continuo', 'duracion': '3 min'},
    # ... Se podrían añadir todos, pero incluimos una selección base para demostrar funcionalidad
}

SESSIONS = [
    {'id': 1, 'nombre': "Sesión 1: Estabilidad y Fuerza Base", 'ejercicios': ['w_walk_mob', 'w_balance', 'w_pushups_wall', 'w_squat_wall', 'r_sq_body', 'r_rdl', 'r_bench_bar', 'e_walk']},
    {'id': 2, 'nombre': "Sesión 2: Propiocepción y Empuje", 'ejercicios': ['w_walk_mob', 'w_balance', 'r_sq_body', 'e_walk']},
]

# Inicialización de estado
if 'rms' not in st.session_state:
    st.session_state.rms = {}
if 'profile' not in st.session_state:
    st.session_state.profile = {'nombre': '', 'apellidos': '', 'sexo': 'Hombre', 'edad': 60}

# Sidebar - Navegación
st.sidebar.title("CLL Fitness")
page = st.sidebar.radio("Ir a", ["Perfil y 1RM", "Entrenamiento", "Mi Progreso"])

def generate_docx(session_id):
    session = next(s for s in SESSIONS if s['id'] == session_id)
    doc = Document()
    
    # Header
    title = doc.add_heading('REPORTE DE ENTRENAMIENTO - PACIENTE LLC', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    p = doc.add_paragraph()
    p.add_run(f"Paciente: {st.session_state.profile['nombre']} {st.session_state.profile['apellidos']}\n").bold = True
    p.add_run(f"Edad: {st.session_state.profile['edad']} años | Sexo: {st.session_state.profile['sexo']}\n")
    p.add_run(f"Sesión: {session['nombre']}\n").bold = True
    p.add_run(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")
    
    doc.add_heading('OBJETIVO DIARIO: CAMINAR 60 MINUTOS', level=2)

    for phase in ['Calentamiento', 'Entrenamiento de Resistencia', 'Enfriamiento']:
        ex_ids = [eid for eid in session['ejercicios'] if EXERCISES.get(eid, {}).get('parte') == phase]
        if not ex_ids: continue
        
        doc.add_heading(phase.upper(), level=1)
        table = doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Ejercicio'
        hdr_cells[1].text = 'Plan'
        hdr_cells[2].text = 'Carga (70%)'
        hdr_cells[3].text = 'RPE'

        for eid in ex_ids:
            ex = EXERCISES[eid]
            row_cells = table.add_row().cells
            row_cells[0].text = ex['nombre']
            row_cells[1].text = ex['plan']
            
            rm = st.session_state.rms.get(eid, 0)
            load = f"{rm * 0.7:.1f} kg" if rm > 0 else "Peso Corp."
            row_cells[2].text = load
            row_cells[3].text = f"RPE {ex['rpe']}"

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

if page == "Perfil y 1RM":
    st.title("Ficha del Paciente y Configuración 1RM")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Datos Personales")
        st.session_state.profile['nombre'] = st.text_input("Nombre", st.session_state.profile['nombre'])
        st.session_state.profile['apellidos'] = st.text_input("Apellidos", st.session_state.profile['apellidos'])
        st.session_state.profile['sexo'] = st.selectbox("Sexo", ["Hombre", "Mujer", "Otro"], index=0)
        st.session_state.profile['edad'] = st.number_input("Edad", min_value=1, max_value=120, value=st.session_state.profile['edad'])

    with col2:
        st.subheader("Configuración de Cargas (1RM)")
        st.info("Ingresa tu Repetición Máxima para los ejercicios de fuerza.")
        for eid, ex in EXERCISES.items():
            if ex['parte'] == 'Entrenamiento de Resistencia' and ex['tipo'] not in ['autocarga', 'pliométrico']:
                current_rm = st.session_state.rms.get(eid, 0.0)
                st.session_state.rms[eid] = st.number_input(f"1RM {ex['nombre']} (kg)", min_value=0.0, value=float(current_rm), key=f"rm_{eid}")

elif page == "Entrenamiento":
    st.title("Sesiones de Entrenamiento")
    
    selected_session_name = st.selectbox("Selecciona tu sesión para hoy", [s['nombre'] for s in SESSIONS])
    session = next(s for s in SESSIONS if s['nombre'] == selected_session_name)
    
    st.success(f"Caminar 60 minutos es tu objetivo base diario.")
    
    col_a, col_b = st.columns([3, 1])
    with col_b:
        doc_buffer = generate_docx(session['id'])
        st.download_button(
            label="📄 Descargar Reporte (Word)",
            data=doc_buffer,
            file_name=f"Reporte_LLC_{datetime.now().strftime('%Y%m%d')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    for phase in ['Calentamiento', 'Entrenamiento de Resistencia', 'Enfriamiento']:
        st.markdown(f"<h2 class='phase-header'>{phase}</h2>", unsafe_allow_html=True)
        ex_ids = [eid for eid in session['ejercicios'] if EXERCISES.get(eid, {}).get('parte') == phase]
        
        for eid in ex_ids:
            ex = EXERCISES[eid]
            with st.container():
                st.markdown(f"""
                <div class='exercise-card'>
                    <div style='display: flex; gap: 20px; align-items: start;'>
                        <img src='{ex['imagen']}' style='width: 150px; border-radius: 10px;'>
                        <div style='flex: 1;'>
                            <h3 style='margin: 0;'>{ex['nombre']} <span style='font-size: 0.6em; color: gray;'>({ex['tipo']})</span></h3>
                            <p style='font-style: italic; color: #64748b; font-size: 0.9em;'>{ex['descripcion']}</p>
                            <div style='display: flex; gap: 20px; margin-top: 10px;'>
                                <div><small>PLAN</small><br><b>{ex['plan']}</b></div>
                                <div><small>CARGA</small><br><b>{f"{st.session_state.rms.get(eid, 0)*0.7:.1f} kg" if st.session_state.rms.get(eid,0) > 0 else "Peso Corp."}</b></div>
                                <div><small>RPE</small><br><b>{ex['rpe']}/10</b></div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

elif page == "Mi Progreso":
    st.title("Seguimiento y Evolución")
    st.write("Aquí se mostrará tu evolución a medida que completes sesiones.")
    
    if not st.session_state.rms:
        st.warning("Aún no has configurado tus cargas de 1RM.")
    else:
        # Mostrar tabla resumen
        data = []
        for eid, rm in st.session_state.rms.items():
            if rm > 0:
                ex = EXERCISES[eid]
                data.append({
                    "Ejercicio": ex['nombre'],
                    "1RM Actual": f"{rm} kg",
                    "Carga de Trabajo (70%)": f"{rm * 0.7:.1f} kg",
                    "Próximo Objetivo (+10%)": f"{rm * 0.7 * 1.1:.1f} kg"
                })
        if data:
            st.table(pd.DataFrame(data))
        else:
            st.info("Ingresa datos en 'Perfil y 1RM' para ver los cálculos aquí.")

st.sidebar.markdown("---")
st.sidebar.caption("Diseñado bajo guías ACSM para pacientes con LLC.")
