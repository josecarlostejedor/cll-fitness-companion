
import streamlit as st
import pandas as pd
from io import BytesIO
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Configuración
st.set_page_config(page_title="CLL-CARE Prescripción", layout="wide", initial_sidebar_state="expanded")

# CSS para tarjetas profesionales
st.markdown("""
<style>
.exercise-card {
    background-color: white;
    padding: 1.5rem;
    border-radius: 1.5rem;
    border: 1px solid #f1f5f9;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    margin-bottom: 1.5rem;
    display: flex;
    flex-direction: column;
}
.ex-image {
    width: 100%;
    height: 180px;
    object-fit: cover;
    border-radius: 1rem;
    margin-bottom: 1rem;
}
.clinical-badge {
    font-size: 0.65em;
    font-weight: 800;
    color: #2563eb;
    text-transform: uppercase;
    background: #eff6ff;
    padding: 3px 10px;
    border-radius: 999px;
    width: fit-content;
    margin-bottom: 0.5rem;
}
.label-val {
    display: flex;
    justify-content: space-between;
    font-size: 0.85em;
    margin-top: 5px;
}
.instruction-box {
    background-color: #f0f7ff;
    border: 2px solid #2563eb;
    padding: 2rem;
    border-radius: 1.5rem;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Catálogo completo
EXERCISES = {
    'w_walk_mob': {'nombre': 'Caminar + Movilidad', 'desc': 'Marcha suave con círculos de hombros.', 'img': 'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=600&q=80', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    'w_balance': {'nombre': 'Equilibrio 1 Pierna', 'desc': 'Controlar peso en un solo pie.', 'img': 'https://images.unsplash.com/photo-1518611012118-2969c6a2c5a7?w=600&q=80', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '30s/lado'},
    'w_pushups_wall': {'nombre': 'Flexiones Pared', 'desc': 'Empuje inclinado contra pared.', 'img': 'https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=600&q=80', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '15 rep'},
    'w_sts': {'nombre': 'Sit-to-Stand', 'desc': 'Levantarse de silla sin manos.', 'img': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&q=80', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '10 rep'},
    'r_sq_body': {'nombre': 'Sentadilla', 'desc': 'Controlar bajada de cadera.', 'img': 'https://images.unsplash.com/photo-1574680096145-d05b474e2158?w=600&q=80', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    'r_rdl': {'nombre': 'Peso Muerto', 'desc': 'Bisagra de cadera controlada.', 'img': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600&q=80', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    'r_bench_db': {'nombre': 'Press Mancuernas', 'desc': 'Empuje desde el pecho.', 'img': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&q=80', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    'r_curl_db': {'nombre': 'Curl Bíceps', 'desc': 'Flexión de codos con carga.', 'img': 'https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=600&q=80', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    'r_row_db': {'nombre': 'Remo Mancuerna', 'desc': 'Tracción hacia la cadera.', 'img': 'https://images.unsplash.com/photo-1594737625785-a239f56d0bdc?w=600&q=80', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    'r_plank': {'nombre': 'Plancha', 'desc': 'Bloque sobre antebrazos.', 'img': 'https://images.unsplash.com/photo-1566241142559-40e1bfc26ebc?w=600&q=80', 'parte': 'Resistencia', 'rpe': 7, 'plan': '30s'},
    'r_jump_sts': {'nombre': 'Salto STS', 'desc': 'Potencia desde silla.', 'img': 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?w=600&q=80', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    'e_walk': {'nombre': 'Caminata Suave', 'desc': 'Paseo de recuperación.', 'img': 'https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=600&q=80', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '3 min'},
    'e_stretch_quad': {'nombre': 'Estiramiento', 'desc': 'Talón al glúteo.', 'img': 'https://images.unsplash.com/photo-1552196563-55cd4e45efb3?w=600&q=80', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '30s/lado'},
}

SESSIONS = [
    {'id': 1, 'nombre': "Sesión 1: Estabilidad Base", 'ejercicios': ['w_walk_mob', 'w_balance', 'w_pushups_wall', 'r_sq_body', 'r_rdl', 'r_bench_db', 'r_row_db', 'r_plank', 'e_walk', 'e_stretch_quad']},
    {'id': 2, 'nombre': "Sesión 2: Potencia y Control", 'ejercicios': ['w_walk_mob', 'w_sts', 'r_sq_body', 'r_jump_sts', 'r_curl_db', 'r_row_db', 'r_plank', 'e_walk', 'e_stretch_quad']},
    {'id': 3, 'nombre': "Sesión 3: Resistencia Superior", 'ejercicios': ['w_walk_mob', 'w_pushups_wall', 'r_bench_db', 'r_row_db', 'r_curl_db', 'r_plank', 'e_walk', 'e_stretch_quad']},
    {'id': 4, 'nombre': "Sesión 4: Coordinación Global", 'ejercicios': ['w_walk_mob', 'w_sts', 'w_balance', 'r_sq_body', 'r_rdl', 'r_bench_db', 'r_plank', 'e_walk', 'e_stretch_quad']},
]

if 'rms' not in st.session_state: st.session_state.rms = {}
if 'profile' not in st.session_state: st.session_state.profile = {'nombre': '', 'apellidos': '', 'edad': 65, 'sexo': 'Hombre'}

def generate_docx(session_id):
    doc = Document()
    session = SESSIONS[session_id-1]
    
    # Header
    title = doc.add_heading('PLAN TERAPÉUTICO CLL-CARE', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    p = doc.add_paragraph()
    p.add_run(f"Paciente: {st.session_state.profile['nombre']} {st.session_state.profile['apellidos']} ({st.session_state.profile['sexo']})").bold = True
    p.add_run(f"\nSesión: {session['id']} - {session['nombre']}")
    
    for phase in ['Calentamiento', 'Resistencia', 'Enfriamiento']:
        doc.add_heading(phase.upper(), level=1)
        table = doc.add_table(rows=1, cols=3)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Ejercicio'
        hdr_cells[1].text = 'Dosificación'
        hdr_cells[2].text = 'Carga'
        
        ex_ids = [eid for eid in session['ejercicios'] if EXERCISES[eid]['parte'] == phase]
        for eid in ex_ids:
            ex = EXERCISES[eid]
            row_cells = table.add_row().cells
            row_cells[0].text = ex['nombre']
            row_cells[1].text = ex['plan']
            rm = st.session_state.rms.get(eid, 0.0)
            carga = f"{int(round(rm * 0.7))} kg" if rm > 0 else "Peso Corp."
            row_cells[2].text = carga
            
    doc.add_heading('INSTRUCCIONES DE REPETICIÓN', level=1)
    doc.add_paragraph("Debe repetir el protocolo completo 3 VECES por sesión. Al terminar el enfriamiento, descanse 3 minutos antes de volver a empezar desde el calentamiento.")
    
    target = BytesIO()
    doc.save(target)
    return target.getvalue()

# Sidebar
st.sidebar.title("CLL-CARE ADMIN")
page = st.sidebar.radio("Secciones", ["👤 Perfil Paciente", "🏋️ Prescripción Sesiones", "⚙️ Gestión de RM"])

if page == "👤 Perfil Paciente":
    st.title("Historial del Paciente")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state.profile['nombre'] = st.text_input("Nombre", st.session_state.profile['nombre'])
    with c2:
        st.session_state.profile['apellidos'] = st.text_input("Apellidos", st.session_state.profile['apellidos'])
    with c3:
        st.session_state.profile['sexo'] = st.selectbox("Sexo", ["Hombre", "Mujer", "Otro"], index=["Hombre", "Mujer", "Otro"].index(st.session_state.profile['sexo']))
    
    st.session_state.profile['edad'] = st.number_input("Edad", 1, 120, st.session_state.profile['edad'])
    
    st.markdown("### Resumen Histórico")
    st.write(f"**Paciente:** {st.session_state.profile['nombre']} {st.session_state.profile['apellidos']}")
    st.write(f"**Sexo:** {st.session_state.profile['sexo']} | **Edad:** {st.session_state.profile['edad']} años")
    
    st.success("Recomendación Médica: Caminar 60 min cada día para combatir la fatiga oncológica.")

elif page == "⚙️ Gestión de RM":
    st.title("Configuración de 1RM (Enteros)")
    st.write("Ingrese el peso máximo (1RM) sin decimales. El sistema calculará la carga meta entera.")
    
    res_exs = [k for k,v in EXERCISES.items() if v['parte'] == 'Resistencia' and 'img' in v]
    for eid in res_exs:
        ex = EXERCISES[eid]
        val = st.number_input(f"1RM {ex['nombre']} (kg)", value=float(st.session_state.rms.get(eid, 0.0)), step=1.0)
        st.session_state.rms[eid] = int(round(val))
        st.caption(f"Carga prescrita (70%): **{int(round(st.session_state.rms[eid] * 0.7))} kg**")

elif page == "🏋️ Prescripción Sesiones":
    st.title("Protocolos de Entrenamiento")
    sid = st.radio("Seleccionar Protocolo:", [1, 2, 3, 4], format_func=lambda x: SESSIONS[x-1]['nombre'], horizontal=True)
    session = SESSIONS[sid-1]
    
    st.download_button(
        label="📥 Descargar Informe Word para Paciente",
        data=generate_docx(sid),
        file_name=f"Prescripcion_CLL_{st.session_state.profile['nombre']}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    
    for phase in ['Calentamiento', 'Resistencia', 'Enfriamiento']:
        st.subheader(phase.upper())
        ex_ids = [eid for eid in session['ejercicios'] if EXERCISES[eid]['parte'] == phase]
        cols = st.columns(3)
        for i, eid in enumerate(ex_ids):
            ex = EXERCISES[eid]
            with cols[i % 3]:
                rm = st.session_state.rms.get(eid, 0.0)
                carga = f"{int(round(rm * 0.7))} kg" if rm > 0 else "Peso Corp."
                st.markdown(f"""
                <div class="exercise-card">
                    <img src="{ex['img']}" class="ex-image">
                    <div class="clinical-badge">{ex['parte']}</div>
                    <div style="font-weight:bold; font-size:1.1em; color:#1e293b; margin-bottom:5px;">{ex['nombre']}</div>
                    <div style="font-size:0.75em; color:#64748b; font-style:italic; margin-bottom:15px; height:40px; overflow:hidden;">"{ex['desc']}"</div>
                    <div class="label-val"><b>Plan:</b> <span>{ex['plan']}</span></div>
                    <div class="label-val"><b>Carga:</b> <span style="color:#2563eb; font-weight:bold;">{carga}</span></div>
                    <div class="label-val"><b>RPE:</b> <span>{ex['rpe']}/10</span></div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="instruction-box">
        <h3 style="margin-top:0;">📋 Instrucción de Repetición del Plan</h3>
        <p>Debe repetir <b>este plan completo 3 veces</b> por sesión.</p>
        <p>Al terminar la lista de ejercicios, <b>descanse 3 minutos</b> para recuperarse.</p>
        <p>Vuelva a empezar desde el calentamiento hasta completar las 3 series globales.</p>
    </div>
    """, unsafe_allow_html=True)
