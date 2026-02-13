
import streamlit as st
import pandas as pd
import base64
import os
from io import BytesIO
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Configuración
st.set_page_config(page_title="CLL-CARE Prescripción", layout="wide", initial_sidebar_state="expanded")

# Función para convertir imagen local a base64 (para Streamlit)
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return f"data:image/jpg;base64,{base64.b64encode(img_file.read()).decode()}"
    return "https://via.placeholder.com/600x400?text=Imagen+No+Encontrada"

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
    height: 100%;
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

# Catálogo completo sincronizado con 4 Sesiones
EXERCISES = {
    # SESIÓN 1
    's1_w_1': {'nombre': 'Caminar círculos + movilidad', 'desc': 'Rápido, paso largo, círculos hombros, rodillas, puntillas, lateral trote.', 'img': 'images/caminar_movilidad.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's1_w_2': {'nombre': 'Equilibrio 1 pierna', 'desc': 'Mantener el equilibrio sobre un solo pie.', 'img': 'images/equilibrio.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's1_w_3': {'nombre': 'Flexiones pared/suelo', 'desc': 'Empuje de brazos contra pared o suelo.', 'img': 'images/flexiones.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 min'},
    's1_w_4': {'nombre': 'Sentadilla pared', 'desc': 'Isometría apoyado en la pared.', 'img': 'images/sentadilla_pared.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 min'},
    's1_w_5': {'nombre': 'Saltar', 'desc': 'Saltos suaves y controlados.', 'img': 'images/saltar.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's1_w_6': {'nombre': 'Lanzamientos pelota', 'desc': 'Lanzar y recibir una pelota contra la pared.', 'img': 'images/lanzamientos.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's1_r_1': {'nombre': 'Sentadilla peso corporal', 'desc': 'Flexión de cadera y rodillas.', 'img': 'images/sentadilla_libre.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's1_r_2': {'nombre': 'Peso muerto rumano', 'desc': 'Bisagra de cadera con carga.', 'img': 'images/peso_muerto.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's1_r_3': {'nombre': 'Plancha Isométrica', 'desc': 'Mantener cuerpo alineado sobre antebrazos.', 'img': 'images/plancha.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '30s'},
    's1_r_4': {'nombre': 'Press banca barra', 'desc': 'Empuje horizontal desde el pecho.', 'img': 'images/press_banca.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's1_r_5': {'nombre': 'Curl bíceps + flex hombro', 'desc': 'Flexión de codos y elevación frontal.', 'img': 'images/curl_hombro.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's1_r_6': {'nombre': 'Remo mancuernas', 'desc': 'Tracción bilateral hacia la cadera.', 'img': 'images/remo.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's1_c_1': {'nombre': 'Caminata + respiración', 'desc': 'Paseo suave coordinando respiración profunda.', 'img': 'images/caminata_suave.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '3 min'},
    's1_c_2': {'nombre': 'Estiramiento cuádriceps', 'desc': 'Talón al glúteo.', 'img': 'images/est_cuadriceps.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's1_c_3': {'nombre': 'Estiramiento isquios', 'desc': 'Pierna extendida al frente.', 'img': 'images/est_isquios.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's1_c_4': {'nombre': 'Estiramiento pantorrilla', 'desc': 'Apoyo en pared estirando pantorrilla.', 'img': 'images/est_gemelos.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's1_c_5': {'nombre': 'Estiramiento bíceps', 'desc': 'Extensión de brazo contra soporte.', 'img': 'images/est_biceps.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's1_c_6': {'nombre': 'Estiramiento hombros', 'desc': 'Cruzar brazo frontalmente.', 'img': 'images/est_hombros.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's1_c_7': {'nombre': 'Movilidad cervical', 'desc': 'Rotaciones de cuello lentas.', 'img': 'images/movilidad_cuello.jpg', 'parte': 'Enfriamiento', 'rpe': 2, 'plan': '2 min'},

    # SESIÓN 2
    's2_w_1': {'nombre': 'Caminar + movilidad', 'desc': 'Caminata fluida con movilidad articular.', 'img': 'images/caminar_movilidad_2.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's2_w_2': {'nombre': 'Propiocepción tobillo', 'desc': 'Estabilidad unipodal.', 'img': 'images/propiocepcion.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's2_w_3': {'nombre': 'Elevación rodilla+brazo', 'desc': 'Coordinación tren superior e inferior.', 'img': 'images/rodilla_brazo.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 min'},
    's2_w_4': {'nombre': 'Sit-to-stand', 'desc': 'Sentarse y levantarse sin manos.', 'img': 'images/sit_to_stand.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 min'},
    's2_w_5': {'nombre': 'Step-up', 'desc': 'Subida controlada al escalón.', 'img': 'images/step_up.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's2_w_6': {'nombre': 'Boxeo suave', 'desc': 'Lanzamiento de puñetazos rítmicos.', 'img': 'images/boxeo.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's2_r_1': {'nombre': 'Estocada adelante carga', 'desc': 'Zancada frontal con peso.', 'img': 'images/estocada_carga.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's2_r_2': {'nombre': 'Empuje cadera', 'desc': 'Elevación de pelvis con carga.', 'img': 'images/hip_thrust.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's2_r_3': {'nombre': 'Press Pallof', 'desc': 'Anti-rotación con banda elástica.', 'img': 'images/pallof.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's2_r_4': {'nombre': 'Press banca mancuernas', 'desc': 'Empuje con mancuernas independientes.', 'img': 'images/press_mancuernas.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's2_r_5': {'nombre': 'Press hombros', 'desc': 'Empuje vertical con mancuernas.', 'img': 'images/press_hombro_manc.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's2_r_6': {'nombre': 'Saltos sentado-parado', 'desc': 'Incorporación explosiva con salto.', 'img': 'images/salto_silla.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's2_c_1': {'nombre': 'Caminata', 'desc': 'Caminata suave de enfriamiento.', 'img': 'images/caminata_2.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '3 min'},
    's2_c_2': {'nombre': 'Est. cuádriceps', 'desc': 'Talón al glúteo.', 'img': 'images/est_cuadriceps_2.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's2_c_3': {'nombre': 'Est. glúteos', 'desc': 'Cruzar pierna y rodilla al pecho.', 'img': 'images/est_gluteo.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's2_c_4': {'nombre': 'Est. aductor', 'desc': 'Inclinación lateral cadera.', 'img': 'images/est_aductor.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's2_c_5': {'nombre': 'Est. isquios', 'desc': 'Inclinación a pierna extendida.', 'img': 'images/est_isquios_2.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's2_c_6': {'nombre': 'Est. hombros', 'desc': 'Cruzado frontal brazo.', 'img': 'images/est_hombros_2.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's2_c_7': {'nombre': 'Movilidad cervical', 'desc': 'Movimientos lentos de cuello.', 'img': 'images/movilidad_cuello_2.jpg', 'parte': 'Enfriamiento', 'rpe': 2, 'plan': '2 min'},

    # SESIÓN 3
    's3_w_1': {'nombre': 'Caminar + movilidad', 'desc': 'Caminata rítmica y movilidad.', 'img': 'images/caminar_3.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's3_w_2': {'nombre': 'Step-ups laterales', 'desc': 'Subida lateral al escalón.', 'img': 'images/step_lateral.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's3_w_3': {'nombre': 'Flexiones cerradas', 'desc': 'Manos a anchura de hombros.', 'img': 'images/flexiones_cerradas.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 min'},
    's3_w_4': {'nombre': 'Estocadas sitio', 'desc': 'Tijeras estáticas.', 'img': 'images/estocada_sitio.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 min'},
    's3_w_5': {'nombre': 'Saltos tijera', 'desc': 'Jumping jacks moderados.', 'img': 'images/jumping_jacks.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's3_w_6': {'nombre': 'Puente glúteos', 'desc': 'Elevación cadera desde suelo.', 'img': 'images/puente.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's3_r_1': {'nombre': 'Sentadilla amplia', 'desc': 'Sumo squat con carga.', 'img': 'images/sentadilla_sumo.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's3_r_2': {'nombre': 'Peso muerto', 'desc': 'Peso muerto con barra u objeto.', 'img': 'images/peso_muerto_3.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's3_r_3': {'nombre': 'Remo barra', 'desc': 'Tracción horizontal inclinada.', 'img': 'images/remo_barra.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's3_r_4': {'nombre': 'Curl bíceps barra', 'desc': 'Flexión de codos con barra.', 'img': 'images/curl_barra.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's3_r_5': {'nombre': 'Elevaciones laterales', 'desc': 'Apertura lateral de hombros.', 'img': 'images/elev_laterales.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's3_r_6': {'nombre': 'Subida caja 1 pierna', 'desc': 'Subida explosiva a cajón.', 'img': 'images/subida_caja.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's3_c_1': {'nombre': 'Caminar', 'desc': 'Caminata de vuelta a la calma.', 'img': 'images/caminar_3_end.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '3 min'},
    's3_c_2': {'nombre': 'Est. cuádriceps', 'desc': 'Talón al glúteo.', 'img': 'images/est_cuadriceps_3.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's3_c_3': {'nombre': 'Est. glúteos', 'desc': 'Rodilla al pecho.', 'img': 'images/est_gluteo_3.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's3_c_4': {'nombre': 'Est. isquios', 'desc': 'Inclinación frontal profunda.', 'img': 'images/est_isquios_3.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's3_c_5': {'nombre': 'Est. bíceps', 'desc': 'Extensión completa de brazo.', 'img': 'images/est_biceps_3.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's3_c_6': {'nombre': 'Est. hombros', 'desc': 'Cruzar brazo frontal.', 'img': 'images/est_hombros_3.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's3_c_7': {'nombre': 'Movilidad cervical', 'desc': 'Rotaciones de cuello.', 'img': 'images/movilidad_cuello_3.jpg', 'parte': 'Enfriamiento', 'rpe': 2, 'plan': '2 min'},

    # SESIÓN 4
    's4_w_1': {'nombre': 'Caminar + movilidad', 'desc': 'Caminata y movimientos articulares.', 'img': 'images/caminar_4.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's4_w_2': {'nombre': 'Sit-to-stand', 'desc': 'Levantarse de silla controladamente.', 'img': 'images/sit_to_stand_4.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's4_w_3': {'nombre': 'Flexión codo banda', 'desc': 'Bíceps con banda elástica.', 'img': 'images/curl_banda.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 min'},
    's4_w_4': {'nombre': 'Elevación pantorrilla', 'desc': 'Elevación de talones.', 'img': 'images/gemelos.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 min'},
    's4_w_5': {'nombre': 'Saltos', 'desc': 'Saltos cortos rítmicos.', 'img': 'images/saltos_cortos.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's4_w_6': {'nombre': 'Circunducción hombros', 'desc': 'Rotación amplia de hombros.', 'img': 'images/circunduccion.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's4_r_1': {'nombre': 'Estocada lateral kettlebell', 'desc': 'Paso lateral con carga.', 'img': 'images/estocada_lat_kb.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's4_r_2': {'nombre': 'Peso muerto', 'desc': 'Bisagra de cadera controlada.', 'img': 'images/peso_muerto_4.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's4_r_3': {'nombre': 'Vuelo pecho banco inclinado', 'desc': 'Aperturas de pecho con mancuernas.', 'img': 'images/vuelo_pecho.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's4_r_4': {'nombre': 'Press tríceps supino', 'desc': 'Extensión codos tumbado.', 'img': 'images/press_frances.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's4_r_5': {'nombre': 'Elevación frontal', 'desc': 'Hombros tren superior.', 'img': 'images/elev_frontal.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's4_r_6': {'nombre': 'Sentadillas salto', 'desc': 'Potencia explosiva inferior.', 'img': 'images/sentadilla_salto.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's4_c_1': {'nombre': 'Caminata', 'desc': 'Vuelta a la calma.', 'img': 'images/caminata_4_end.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '3 min'},
    's4_c_2': {'nombre': 'Est. cuádriceps', 'desc': 'Pierna atrás talón glúteo.', 'img': 'images/est_cuadriceps_4.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's4_c_3': {'nombre': 'Est. glúteos', 'desc': 'Rodilla al pecho profunda.', 'img': 'images/est_gluteo_4.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's4_c_4': {'nombre': 'Est. tríceps', 'desc': 'Extensión codo tras nuca.', 'img': 'images/est_triceps.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's4_c_5': {'nombre': 'Est. pecho', 'desc': 'Apertura de caja torácica.', 'img': 'images/est_pecho.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's4_c_6': {'nombre': 'Est. hombros', 'desc': 'Cruzado frontal.', 'img': 'images/est_hombros_4.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's4_c_7': {'nombre': 'Movilidad cervical', 'desc': 'Movimientos suaves de cuello.', 'img': 'images/movilidad_cuello_4.jpg', 'parte': 'Enfriamiento', 'rpe': 2, 'plan': '2 min'},
}

SESSIONS = [
    {'id': 1, 'nombre': "Sesión 1: Estabilidad Base", 'ejercicios': ['s1_w_1', 's1_w_2', 's1_w_3', 's1_w_4', 's1_w_5', 's1_w_6', 's1_r_1', 's1_r_2', 's1_r_3', 's1_r_4', 's1_r_5', 's1_r_6', 's1_c_1', 's1_c_2', 's1_c_3', 's1_c_4', 's1_c_5', 's1_c_6', 's1_c_7']},
    {'id': 2, 'nombre': "Sesión 2: Potencia Dinámica", 'ejercicios': ['s2_w_1', 's2_w_2', 's2_w_3', 's2_w_4', 's2_w_5', 's2_w_6', 's2_r_1', 's2_r_2', 's2_r_3', 's2_r_4', 's2_r_5', 's2_r_6', 's2_c_1', 's2_c_2', 's2_c_3', 's2_c_4', 's2_c_5', 's2_c_6', 's2_c_7']},
    {'id': 3, 'nombre': "Sesión 3: Fuerza Integral", 'ejercicios': ['s3_w_1', 's3_w_2', 's3_w_3', 's3_w_4', 's3_w_5', 's3_w_6', 's3_r_1', 's3_r_2', 's3_r_3', 's3_r_4', 's3_r_5', 's3_r_6', 's3_c_1', 's3_c_2', 's3_c_3', 's3_c_4', 's3_c_5', 's3_c_6', 's3_c_7']},
    {'id': 4, 'nombre': "Sesión 4: Control y Empuje", 'ejercicios': ['s4_w_1', 's4_w_2', 's4_w_3', 's4_w_4', 's4_w_5', 's4_w_6', 's4_r_1', 's4_r_2', 's4_r_3', 's4_r_4', 's4_r_5', 's4_r_6', 's4_c_1', 's4_c_2', 's4_c_3', 's4_c_4', 's4_c_5', 's4_c_6', 's4_c_7']}
]

if 'rms' not in st.session_state: st.session_state.rms = {}
if 'profile' not in st.session_state: st.session_state.profile = {'nombre': '', 'apellidos': '', 'edad': 65, 'sexo': 'Hombre'}

def generate_docx(session_id):
    doc = Document()
    
    # Ajuste de márgenes para maximizar espacio
    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

    session = SESSIONS[session_id-1]
    
    # Encabezado principal
    title = doc.add_heading('PLAN TERAPÉUTICO CLL-CARE', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_patient = p_info.add_run(f"Paciente: {st.session_state.profile['nombre']} {st.session_state.profile['apellidos']} ({st.session_state.profile['sexo']})")
    run_patient.bold = True
    p_info.add_run(f"\nSesión: {session['id']} - {session['nombre']}")

    # Iterar por fases
    for phase_label in ['Calentamiento', 'Resistencia', 'Enfriamiento']:
        doc.add_heading(phase_label.upper(), level=1)
        
        # Filtrar ejercicios de esta fase
        ex_ids = [eid for eid in session['ejercicios'] if EXERCISES[eid]['parte'] == phase_label]
        
        # Crear tabla de 3 columnas para la rejilla
        table = doc.add_table(rows=0, cols=3)
        table.style = 'Table Grid'
        
        # Llenar la tabla en grupos de 3
        for i in range(0, len(ex_ids), 3):
            row_cells = table.add_row().cells
            for j in range(3):
                if i + j < len(ex_ids):
                    eid = ex_ids[i + j]
                    ex = EXERCISES[eid]
                    cell = row_cells[j]
                    
                    # 1. Etiqueta "Ejercicio"
                    p_ej = cell.paragraphs[0]
                    p_ej.text = "Ejercicio"
                    p_ej.bold = True
                    p_ej.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    
                    # 2. Nombre del Ejercicio
                    p_name = cell.add_paragraph()
                    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    run_name = p_name.add_run(ex['nombre'])
                    run_name.bold = True
                    run_name.font.size = Pt(10)
                    
                    # 3. Imagen del Ejercicio
                    if os.path.exists(ex['img']):
                        p_img = cell.add_paragraph()
                        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        run_img = p_img.add_run()
                        run_img.add_picture(ex['img'], width=Inches(1.4))
                    else:
                        p_noimg = cell.add_paragraph("[Imagen no disponible]")
                        p_noimg.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    
                    # 4. Datos técnicos (Plan, Carga, RPE)
                    rm = st.session_state.rms.get(eid, 0.0)
                    is_autocarga = any(word in ex['nombre'].lower() for word in ['peso corporal', 'plancha', 'pared', 'equilibrio', 'sit-to-stand', 'paso', 'tijera', 'rodilla', 'boxeo', 'salto'])
                    carga = f"{int(round(rm * 0.7))} kg" if (rm > 0 and not is_autocarga) else "P.C."
                    
                    p_data = cell.add_paragraph()
                    p_data.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    p_data.add_run(f"Plan: {ex['plan']}\n").font.size = Pt(9)
                    p_data.add_run(f"Carga: {carga}\n").font.size = Pt(9)
                    p_data.add_run(f"RPE: {ex['rpe']}/10").font.size = Pt(9)

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
    with c1: st.session_state.profile['nombre'] = st.text_input("Nombre", st.session_state.profile['nombre'])
    with c2: st.session_state.profile['apellidos'] = st.text_input("Apellidos", st.session_state.profile['apellidos'])
    with c3: st.session_state.profile['sexo'] = st.selectbox("Sexo", ["Hombre", "Mujer", "Otro"], index=["Hombre", "Mujer", "Otro"].index(st.session_state.profile['sexo']))
    st.session_state.profile['edad'] = st.number_input("Edad", 1, 120, st.session_state.profile['edad'])
    st.markdown("### Resumen Histórico")
    st.write(f"**Paciente:** {st.session_state.profile['nombre']} {st.session_state.profile['apellidos']}")
    st.write(f"**Sexo:** {st.session_state.profile['sexo']} | **Edad:** {st.session_state.profile['edad']} años")
    st.success("Recomendación Médica: Caminar 60 min cada día para combatir la fatiga oncológica.")

elif page == "⚙️ Gestión de RM":
    st.title("Configuración de 1RM (Enteros)")
    st.write("Ingrese el peso máximo (1RM) sin decimales para los ejercicios de resistencia.")
    res_exs = [k for k,v in EXERCISES.items() if v['parte'] == 'Resistencia' and any(w in v['nombre'].lower() for w in ['barra', 'mancuerna', 'muerto', 'carga', 'kettlebell', 'empuje'])]
    for eid in res_exs:
        ex = EXERCISES[eid]
        val = st.number_input(f"1RM {ex['nombre']} (kg)", value=float(st.session_state.rms.get(eid, 0.0)), key=eid, step=1.0)
        st.session_state.rms[eid] = int(round(val))
        st.caption(f"Carga prescrita (70%): **{int(round(st.session_state.rms[eid] * 0.7))} kg**")

elif page == "🏋️ Prescripción Sesiones":
    st.title("Protocolos de Entrenamiento")
    sid = st.radio("Seleccionar Protocolo:", [1, 2, 3, 4], format_func=lambda x: SESSIONS[x-1]['nombre'], horizontal=True)
    session = SESSIONS[sid-1]
    st.download_button(label="📥 Descargar Informe Word para Paciente", data=generate_docx(sid), file_name=f"Prescripcion_CLL_{st.session_state.profile['nombre']}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    for phase in ['Calentamiento', 'Resistencia', 'Enfriamiento']:
        st.markdown(f"### {phase.upper()}")
        ex_ids = [eid for eid in session['ejercicios'] if EXERCISES[eid]['parte'] == phase]
        cols = st.columns(3)
        for i, eid in enumerate(ex_ids):
            ex = EXERCISES[eid]
            with cols[i % 3]:
                rm = st.session_state.rms.get(eid, 0.0)
                is_autocarga = any(word in ex['nombre'].lower() for word in ['peso corporal', 'plancha', 'pared', 'equilibrio', 'sit-to-stand', 'paso', 'tijera', 'rodilla', 'boxeo', 'salto'])
                carga = f"{int(round(rm * 0.7))} kg" if (rm > 0 and not is_autocarga) else "P.C."
                
                # Obtenemos el Base64 de la imagen local
                img_b64 = get_base64_image(ex['img'])
                
                st.markdown(f"""
                <div class="exercise-card">
                    <img src="{img_b64}" class="ex-image">
                    <div class="clinical-badge">{ex['parte']}</div>
                    <div style="font-weight:bold; font-size:1.1em; color:#1e293b; margin-bottom:5px;">{ex['nombre']}</div>
                    <div style="font-size:0.75em; color:#64748b; font-style:italic; margin-bottom:15px; height:45px; overflow:hidden;">"{ex['desc']}"</div>
                    <div class="label-val"><b>Plan:</b> <span>{ex['plan']}</span></div>
                    <div class="label-val"><b>Carga:</b> <span style="color:#2563eb; font-weight:bold;">{carga}</span></div>
                    <div class="label-val"><b>RPE:</b> <span>{ex['rpe']}/10</span></div>
                </div>
                """, unsafe_allow_html=True)
    st.markdown("""<div class="instruction-box"><h3>📋 Instrucción Global</h3><p>Repetir plan completo 3 veces. Descanso 3 min entre series globales.</p></div>""", unsafe_allow_html=True)
