
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

# Catálogo completo sincronizado (19 Tareas para Sesión 1)
EXERCISES = {
    # CALENTAMIENTO
    's1_w_1': {'nombre': 'Caminar círculos + movilidad', 'desc': 'Rápido, paso largo, círculos hombros, rodillas, puntillas, lateral trote.', 'img': 'images/caminar_movilidad.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's1_w_2': {'nombre': 'Equilibrio 1 pierna', 'desc': 'Mantener el equilibrio sobre un solo pie sin apoyos externos.', 'img': 'images/equilibrio.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's1_w_3': {'nombre': 'Flexiones pared/suelo', 'desc': 'Empuje de brazos contra pared o suelo según nivel.', 'img': 'images/flexiones.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 min'},
    's1_w_4': {'nombre': 'Sentadilla pared', 'desc': 'Isometría apoyado en la pared manteniendo rodillas a 90 grados.', 'img': 'images/sentadilla_pared.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 min'},
    's1_w_5': {'nombre': 'Saltar', 'desc': 'Saltos suaves y controlados sobre las puntas de los pies.', 'img': 'images/saltar.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's1_w_6': {'nombre': 'Lanzamientos pelota', 'desc': 'Lanzar y recibir una pelota contra la pared.', 'img': 'images/lanzamientos.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    
    # RESISTENCIA
    's1_r_1': {'nombre': 'Sentadilla peso corporal', 'desc': 'Flexión de cadera y rodillas con control motor.', 'img': 'images/sentadilla_libre.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's1_r_2': {'nombre': 'Peso muerto rumano', 'desc': 'Bisagra de cadera manteniendo la espalda neutra.', 'img': 'images/peso_muerto.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's1_r_3': {'nombre': 'Plancha Isométrica', 'desc': 'Mantener el cuerpo alineado apoyado sobre antebrazos.', 'img': 'images/plancha.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '30s'},
    's1_r_4': {'nombre': 'Press banca barra', 'desc': 'Empuje horizontal desde el pecho.', 'img': 'images/press_banca.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's1_r_5': {'nombre': 'Curl bíceps + flex hombro', 'desc': 'Flexión de codos y elevación frontal.', 'img': 'images/curl_hombro.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's1_r_6': {'nombre': 'Remo mancuernas', 'desc': 'Tracción bilateral hacia la cadera.', 'img': 'images/remo.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    
    # ENFRIAMIENTO
    's1_c_1': {'nombre': 'Caminata + respiración', 'desc': 'Paseo suave coordinando la respiración profunda.', 'img': 'images/caminata_suave.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '3 min'},
    's1_c_2': {'nombre': 'Estiramiento cuádriceps', 'desc': 'Talón al glúteo manteniendo la cadera alineada.', 'img': 'images/est_cuadriceps.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's1_c_3': {'nombre': 'Estiramiento isquios', 'desc': 'Pierna extendida al frente con el talón apoyado.', 'img': 'images/est_isquios.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's1_c_4': {'nombre': 'Estiramiento pantorrilla', 'desc': 'Apoyo en pared estirando la pantorrilla.', 'img': 'images/est_gemelos.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's1_c_5': {'nombre': 'Estiramiento bíceps', 'desc': 'Extensión de brazo contra un soporte.', 'img': 'images/est_biceps.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's1_c_6': {'nombre': 'Estiramiento hombros', 'desc': 'Cruzar el brazo por delante del pecho.', 'img': 'images/est_hombros.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's1_c_7': {'nombre': 'Movilidad cervical', 'desc': 'Movimientos lentos de rotación e inclinación.', 'img': 'images/movilidad_cuello.jpg', 'parte': 'Enfriamiento', 'rpe': 2, 'plan': '2 min'},
}

SESSIONS = [
    {'id': 1, 'nombre': "Sesión 1: Estabilidad Base", 'ejercicios': [
        's1_w_1', 's1_w_2', 's1_w_3', 's1_w_4', 's1_w_5', 's1_w_6',
        's1_r_1', 's1_r_2', 's1_r_3', 's1_r_4', 's1_r_5', 's1_r_6',
        's1_c_1', 's1_c_2', 's1_c_3', 's1_c_4', 's1_c_5', 's1_c_6', 's1_c_7'
    ]},
]

if 'rms' not in st.session_state: st.session_state.rms = {}
if 'profile' not in st.session_state: st.session_state.profile = {'nombre': '', 'apellidos': '', 'edad': 65, 'sexo': 'Hombre'}

def generate_docx(session_id):
    doc = Document()
    session = SESSIONS[session_id-1]
    
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
            # Determinar si es autocarga o tiene peso
            is_autocarga = 'peso corporal' in ex['nombre'].lower() or 'plancha' in ex['nombre'].lower() or 'pared' in ex['nombre'].lower() or 'equilibrio' in ex['nombre'].lower()
            carga = f"{int(round(rm * 0.7))} kg" if (rm > 0 and not is_autocarga) else "P.C."
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
    st.write("Ingrese el peso máximo (1RM) sin decimales para los ejercicios de resistencia.")
    
    res_exs = [k for k,v in EXERCISES.items() if v['parte'] == 'Resistencia' and 'barra' in v['nombre'].lower() or 'mancuerna' in v['nombre'].lower() or 'muerto' in v['nombre'].lower()]
    for eid in res_exs:
        ex = EXERCISES[eid]
        val = st.number_input(f"1RM {ex['nombre']} (kg)", value=float(st.session_state.rms.get(eid, 0.0)), step=1.0)
        st.session_state.rms[eid] = int(round(val))
        st.caption(f"Carga prescrita (70%): **{int(round(st.session_state.rms[eid] * 0.7))} kg**")

elif page == "🏋️ Prescripción Sesiones":
    st.title("Protocolos de Entrenamiento")
    sid = st.radio("Seleccionar Protocolo:", [1], format_func=lambda x: SESSIONS[x-1]['nombre'], horizontal=True)
    session = SESSIONS[sid-1]
    
    st.download_button(
        label="📥 Descargar Informe Word para Paciente",
        data=generate_docx(sid),
        file_name=f"Prescripcion_CLL_{st.session_state.profile['nombre']}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    
    for phase in ['Calentamiento', 'Resistencia', 'Enfriamiento']:
        st.markdown(f"### {phase.upper()}")
        ex_ids = [eid for eid in session['ejercicios'] if EXERCISES[eid]['parte'] == phase]
        cols = st.columns(3)
        for i, eid in enumerate(ex_ids):
            ex = EXERCISES[eid]
            with cols[i % 3]:
                rm = st.session_state.rms.get(eid, 0.0)
                is_autocarga = 'peso corporal' in ex['nombre'].lower() or 'plancha' in ex['nombre'].lower() or 'pared' in ex['nombre'].lower() or 'equilibrio' in ex['nombre'].lower()
                carga = f"{int(round(rm * 0.7))} kg" if (rm > 0 and not is_autocarga) else "P.C."
                
                st.markdown(f"""
                <div class="exercise-card">
                    <img src="{ex['img']}" class="ex-image" onerror="this.src='https://via.placeholder.com/600x400?text=Imagen+en+images/'">
                    <div class="clinical-badge">{ex['parte']}</div>
                    <div style="font-weight:bold; font-size:1.1em; color:#1e293b; margin-bottom:5px;">{ex['nombre']}</div>
                    <div style="font-size:0.75em; color:#64748b; font-style:italic; margin-bottom:15px; height:45px; overflow:hidden;">"{ex['desc']}"</div>
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
