
import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
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

# Estilos CSS (Se inyectan sin sangría para evitar que Streamlit los trate como código)
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 3.5em;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        transition: all 0.3s ease;
    }
    .exercise-card {
        background-color: white;
        padding: 24px;
        border-radius: 25px;
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    .phase-header {
        color: #0f172a;
        border-left: 8px solid #4f46e5;
        padding-left: 20px;
        margin: 40px 0 20px 0;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: -0.02em;
        font-size: 1.8em;
    }
    .stat-label {
        font-size: 0.7em;
        font-weight: 900;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .stat-value {
        font-size: 1.1em;
        font-weight: 800;
        color: #4f46e5;
    }
    .pliometrico-badge {
        background-color: #fef3c7;
        color: #92400e;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.7em;
        font-weight: 800;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# Catálogo total de ejercicios (Basado exactamente en data/exercises.ts)
EXERCISES = {
    # CALENTAMIENTO
    'w_walk_mob': {'nombre': 'Caminar + Movilidad', 'descripcion': 'Rápido, paso largo, círculos hombros, rodillas, puntillas.', 'tipo': 'aeróbico', 'imagen': 'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=400', 'agonistas': 'Cuerpo completo', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x Continuo', 'duracion': '2 min'},
    'w_balance': {'nombre': 'Equilibrio 1 pierna', 'descripcion': 'Mantener posición estable con una pierna elevada.', 'tipo': 'movilidad', 'imagen': 'https://images.unsplash.com/photo-1599901860904-17e6ed7083a0?w=400', 'agonistas': 'Glúteo medio, Cuádriceps', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 x 30s por pierna'},
    'w_pushups_wall': {'nombre': 'Flexiones pared', 'descripcion': 'Empuje horizontal manteniendo alineación.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1598971639058-aba7c11210ee?w=400', 'agonistas': 'Pectoral mayor', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 15-20'},
    'w_squat_wall': {'nombre': 'Sentadilla pared', 'descripcion': 'Posición de silla apoyado en pared.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1574680096145-d05b474e2158?w=400', 'agonistas': 'Cuádriceps', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 60s'},
    'w_jump': {'nombre': 'Saltar', 'descripcion': 'Saltos suaves sobre puntas de pies.', 'tipo': 'aeróbico', 'imagen': 'https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=400', 'agonistas': 'Gemelos', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 2 min'},
    'w_ball_throw': {'nombre': 'Lanzamientos pelota', 'descripcion': 'Lanzar balón contra suelo o pared.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1599447421416-3414500d18a5?w=400', 'agonistas': 'Deltoides, Pectoral', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 x 12-15'},
    'w_prop_tobillo': {'nombre': 'Propiocepción tobillo', 'descripcion': 'Equilibrio dinámico sobre pie.', 'tipo': 'movilidad', 'imagen': 'https://images.unsplash.com/photo-1599901860904-17e6ed7083a0?w=400', 'agonistas': 'Peroneos', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 x 30s por pie'},
    'w_rodilla_brazo': {'nombre': 'Elevación rodilla+brazo', 'descripcion': 'Marcha exagerada coordinada.', 'tipo': 'aeróbico', 'imagen': 'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=400', 'agonistas': 'Psoas, Deltoides', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 1 min'},
    'w_sts': {'nombre': 'Sit-to-stand', 'descripcion': 'Sentarse y levantarse de silla sin manos.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?w=400', 'agonistas': 'Cuádriceps, Glúteos', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 x 10'},
    'w_step_up': {'nombre': 'Step-up', 'descripcion': 'Subir escalón alternando.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1538805060514-97d9cc17730c?w=400', 'agonistas': 'Glúteo mayor', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 20'},
    'w_boxeo': {'nombre': 'Boxeo suave', 'descripcion': 'Golpes al aire controlados.', 'tipo': 'aeróbico', 'imagen': 'https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?w=400', 'agonistas': 'Deltoides, Tríceps', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 2 min'},
    'w_step_lat': {'nombre': 'Step-ups laterales', 'descripcion': 'Subir escalón de lado.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1538805060514-97d9cc17730c?w=400', 'agonistas': 'Glúteo medio', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 10/lado'},
    'w_pushups_close': {'nombre': 'Flexiones cerradas', 'descripcion': 'Manos juntas para tríceps.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1598971639058-aba7c11210ee?w=400', 'agonistas': 'Tríceps', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 10-12'},
    'w_lunge_site': {'nombre': 'Estocadas sitio', 'descripcion': 'Bajar cadera sin avanzar.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1574680096145-d05b474e2158?w=400', 'agonistas': 'Cuádriceps', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 10 por pierna'},
    'w_jumping_jacks': {'nombre': 'Saltos tijera', 'descripcion': 'Coordinación brazos y piernas.', 'tipo': 'aeróbico', 'imagen': 'https://images.unsplash.com/photo-1601422407692-ec4eeec1d9b3?w=400', 'agonistas': 'Cuerpo completo', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 2 min'},
    'w_glute_bridge': {'nombre': 'Puente glúteos', 'descripcion': 'Elevar cadera desde suelo.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1567598508481-65985588e295?w=400', 'agonistas': 'Glúteo mayor', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 x 12'},
    'w_band_curl': {'nombre': 'Flexión codo banda', 'descripcion': 'Bíceps con banda elástica.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1518310383802-640c2de311b2?w=400', 'agonistas': 'Bíceps', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 15'},
    'w_calf_raise': {'nombre': 'Elevación pantorrilla', 'descripcion': 'Puntillas rítmico.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=400', 'agonistas': 'Gemelos', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 20'},
    'w_shoulder_circ': {'nombre': 'Círculos hombros', 'descripcion': 'Círculos amplios brazos.', 'tipo': 'movilidad', 'imagen': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400', 'agonistas': 'Deltoides', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 15/sentido'},

    # RESISTENCIA
    'r_sq_body': {'nombre': 'Sentadilla peso corporal', 'descripcion': 'Flexión rodilla cadera 90 grados.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1566241142559-40e1bfc26ebc?w=400', 'agonistas': 'Cuádriceps', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_rdl': {'nombre': 'Peso muerto rumano', 'descripcion': 'Flexión cadera, espalda recta.', 'tipo': 'sobrecarga', 'imagen': 'https://images.unsplash.com/photo-1534367507873-d2d7e24c797f?w=400', 'agonistas': 'Isquios', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_plank': {'nombre': 'Plancha abdominal', 'descripcion': 'Mantener cuerpo recto antebrazos.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400', 'agonistas': 'Core', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 30s'},
    'r_bench_bar': {'nombre': 'Press banca barra', 'descripcion': 'Empuje barra desde pecho.', 'tipo': 'barra olímpica', 'imagen': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400', 'agonistas': 'Pectoral', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_curl_flex': {'nombre': 'Curl bíceps + Flex hombro', 'descripcion': 'Flexión codo y elevación brazo.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=400', 'agonistas': 'Bíceps, Deltoides', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_row_db': {'nombre': 'Remo mancuernas', 'descripcion': 'Tracción inclinada hacia cadera.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1605296867304-46d5465a13f1?w=400', 'agonistas': 'Dorsal ancho', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_lunge_db': {'nombre': 'Estocada adelante carga', 'descripcion': 'Paso largo frente mancuernas.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1574680096145-d05b474e2158?w=400', 'agonistas': 'Cuádriceps, Glúteo', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_hip_thrust': {'nombre': 'Empuje cadera', 'descripcion': 'Elevación pelvis con carga.', 'tipo': 'sobrecarga', 'imagen': 'https://images.unsplash.com/photo-1567598508481-65985588e295?w=400', 'agonistas': 'Glúteo mayor', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_pallof': {'nombre': 'Press Pallof', 'descripcion': 'Resistir rotación con banda.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1518310383802-640c2de311b2?w=400', 'agonistas': 'Oblicuos', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_bench_db': {'nombre': 'Press banca mancuernas', 'descripcion': 'Empuje independiente.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=400', 'agonistas': 'Pectoral mayor', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_shoulder_db': {'nombre': 'Press hombros', 'descripcion': 'Empuje vertical mancuernas.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1532029836916-f4874460e41f?w=400', 'agonistas': 'Deltoides', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_jump_sts': {'nombre': 'Saltos sentado-parado', 'descripcion': 'Salto explosivo desde silla.', 'tipo': 'pliométrico', 'imagen': 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?w=400', 'agonistas': 'Piernas (Potencia)', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_sq_sumo': {'nombre': 'Sentadilla amplia', 'descripcion': 'Pies abiertos puntas fuera.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1566241142559-40e1bfc26ebc?w=400', 'agonistas': 'Aductores, Glúteo', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_dl_conv': {'nombre': 'Peso muerto', 'descripcion': 'Tracción desde suelo barra.', 'tipo': 'barra olímpica', 'imagen': 'https://images.unsplash.com/photo-1534367507873-d2d7e24c797f?w=400', 'agonistas': 'Cadena posterior', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_row_bar': {'nombre': 'Remo barra', 'descripcion': 'Tracción barra inclinado.', 'tipo': 'barra olímpica', 'imagen': 'https://images.unsplash.com/photo-1605296867304-46d5465a13f1?w=400', 'agonistas': 'Espalda', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_curl_bar': {'nombre': 'Curl bíceps barra', 'descripcion': 'Flexión codos con barra.', 'tipo': 'barra olímpica', 'imagen': 'https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=400', 'agonistas': 'Bíceps', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_lat_raise': {'nombre': 'Elevaciones laterales', 'descripcion': 'Vuelos laterales mancuernas.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1532029836916-f4874460e41f?w=400', 'agonistas': 'Hombro medio', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_box_step_1p': {'nombre': 'Subida caja 1 pierna', 'descripcion': 'Control subiendo caja.', 'tipo': 'pliométrico', 'imagen': 'https://images.unsplash.com/photo-1538805060514-97d9cc17730c?w=400', 'agonistas': 'Glúteo, Tobillo', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_lunge_lat_kb': {'nombre': 'Estocada lat kettlebell', 'descripcion': 'Paso lateral con carga.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400', 'agonistas': 'Aductores', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_fly_inc': {'nombre': 'Vuelo pecho inclinado', 'descripcion': 'Aperturas mancuerna.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400', 'agonistas': 'Pectoral superior', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_tri_ext': {'nombre': 'Extensión tríceps', 'descripcion': 'Skullcrushers mancuernas.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=400', 'agonistas': 'Tríceps', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_front_raise': {'nombre': 'Elevación frontal', 'descripcion': 'Elevación frente ojos.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=400', 'agonistas': 'Hombro anterior', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_jump_sq': {'nombre': 'Sentadilla salto', 'descripcion': 'Potencia vertical.', 'tipo': 'pliométrico', 'imagen': 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?w=400', 'agonistas': 'Piernas (Potencia)', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},

    # ENFRIAMIENTO
    'e_walk': {'nombre': 'Caminata suave', 'descripcion': 'Bajar pulsaciones respirando.', 'tipo': 'aeróbico', 'imagen': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=400', 'agonistas': 'Completo', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 x 3 min'},
    'e_cuad': {'nombre': 'Estiramiento Cuádriceps', 'descripcion': 'Talón al glúteo.', 'tipo': 'movilidad', 'imagen': 'https://images.unsplash.com/photo-1552196563-55cd4e45efb3?w=400', 'agonistas': 'Cuádriceps', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 x 30s/lado'},
    'e_isq': {'nombre': 'Estiramiento Isquios', 'descripcion': 'Bajar tronco a pierna.', 'tipo': 'movilidad', 'imagen': 'https://images.unsplash.com/photo-1518611012118-29a87d528b2f?w=400', 'agonistas': 'Isquiotibiales', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 x 30s/lado'},
    'e_calf': {'nombre': 'Estiramiento Gemelo', 'descripcion': 'Empuje contra pared.', 'tipo': 'movilidad', 'imagen': 'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=400', 'agonistas': 'Gemelos', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 x 30s/lado'},
    'e_bic': {'nombre': 'Estiramiento Bíceps', 'descripcion': 'Brazo atrás palma afuera.', 'tipo': 'movilidad', 'imagen': 'https://images.unsplash.com/photo-1518310383802-640c2de311b2?w=400', 'agonistas': 'Bíceps', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 x 30s/lado'},
    'e_shoulder': {'nombre': 'Estiramiento Hombros', 'descripcion': 'Cruzar brazo frente pecho.', 'tipo': 'movilidad', 'imagen': 'https://images.unsplash.com/photo-1532029836916-f4874460e41f?w=400', 'agonistas': 'Deltoides post.', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 x 30s/lado'},
    'e_cervical': {'nombre': 'Movilidad Cervical', 'descripcion': 'Rotaciones suaves cuello.', 'tipo': 'movilidad', 'imagen': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400', 'agonistas': 'Cuello', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 x 1 min'},
    'e_glute': {'nombre': 'Estiramiento Glúteos', 'descripcion': 'Cruzar pierna tirando rodilla.', 'tipo': 'movilidad', 'imagen': 'https://images.unsplash.com/photo-1599447421416-3414500d18a5?w=400', 'agonistas': 'Glúteos', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 x 30s/lado'},
    'e_adductor': {'nombre': 'Estiramiento Aductor', 'descripcion': 'Pies juntos rodillas afuera.', 'tipo': 'movilidad', 'imagen': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=400', 'agonistas': 'Aductores', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 x 1 min'},
    'e_tri': {'nombre': 'Estiramiento Tríceps', 'descripcion': 'Mano tras cabeza.', 'tipo': 'movilidad', 'imagen': 'https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=400', 'agonistas': 'Tríceps', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 x 30s/lado'},
    'e_chest': {'nombre': 'Estiramiento Pecho', 'descripcion': 'Manos atrás abriendo caja.', 'tipo': 'movilidad', 'imagen': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400', 'agonistas': 'Pectorales', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 x 1 min'},
}

# Las 4 Sesiones definitivas
SESSIONS = [
    {
        'id': 1, 'nombre': "Sesión 1: Estabilidad y Fuerza Base", 
        'ejercicios': ['w_walk_mob', 'w_balance', 'w_pushups_wall', 'w_squat_wall', 'w_jump', 'w_ball_throw', 'r_sq_body', 'r_rdl', 'r_plank', 'r_bench_bar', 'r_curl_flex', 'r_row_db', 'e_walk', 'e_cuad', 'e_isq', 'e_calf', 'e_bic', 'e_shoulder', 'e_cervical']
    },
    {
        'id': 2, 'nombre': "Sesión 2: Propiocepción y Empuje", 
        'ejercicios': ['w_walk_mob', 'w_prop_tobillo', 'w_rodilla_brazo', 'w_sts', 'w_step_up', 'w_boxeo', 'r_lunge_db', 'r_hip_thrust', 'r_pallof', 'r_bench_db', 'r_shoulder_db', 'r_jump_sts', 'e_walk', 'e_cuad', 'e_glute', 'e_adductor', 'e_isq', 'e_shoulder', 'e_cervical']
    },
    {
        'id': 3, 'nombre': "Sesión 3: Tracción y Salto Lateral", 
        'ejercicios': ['w_walk_mob', 'w_step_lat', 'w_pushups_close', 'w_lunge_site', 'w_jumping_jacks', 'w_glute_bridge', 'r_sq_sumo', 'r_dl_conv', 'r_row_bar', 'r_curl_bar', 'r_lat_raise', 'r_box_step_1p', 'e_walk', 'e_cuad', 'e_glute', 'e_isq', 'e_bic', 'e_shoulder', 'e_cervical']
    },
    {
        'id': 4, 'nombre': "Sesión 4: Fuerza Lateral y Movilidad", 
        'ejercicios': ['w_walk_mob', 'w_sts', 'w_band_curl', 'w_calf_raise', 'w_jump', 'w_shoulder_circ', 'r_lunge_lat_kb', 'r_dl_conv', 'r_fly_inc', 'r_tri_ext', 'r_front_raise', 'r_jump_sq', 'e_walk', 'e_cuad', 'e_glute', 'e_tri', 'e_chest', 'e_shoulder', 'e_cervical']
    }
]

# Inicialización de estado
if 'rms' not in st.session_state: st.session_state.rms = {}
if 'profile' not in st.session_state: st.session_state.profile = {'nombre': '', 'apellidos': '', 'sexo': 'Hombre', 'edad': 60}

# Sidebar
st.sidebar.markdown("<h1 style='color:#4f46e5;text-align:center;'>CLL-FITNESS</h1>", unsafe_allow_html=True)
page = st.sidebar.radio("NAVEGACIÓN", ["📋 Perfil y 1RM", "🏋️ Mis 4 Sesiones", "📈 Evolución"])

def generate_docx(session_id):
    session = next(s for s in SESSIONS if s['id'] == session_id)
    doc = Document()
    doc.add_heading('REPORTE DE ENTRENAMIENTO - PACIENTE LLC', 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = doc.add_paragraph()
    p.add_run(f"Paciente: {st.session_state.profile['nombre']} {st.session_state.profile['apellidos']}").bold = True
    p.add_run(f" | Edad: {st.session_state.profile['edad']} | Sesión: {session['nombre']}")
    doc.add_heading('OBJETIVO DIARIO: CAMINAR 60 MINUTOS', level=2)
    for phase in ['Calentamiento', 'Entrenamiento de Resistencia', 'Enfriamiento']:
        ex_ids = [eid for eid in session['ejercicios'] if EXERCISES.get(eid, {}).get('parte') == phase]
        if not ex_ids: continue
        doc.add_heading(phase.upper(), level=1)
        table = doc.add_table(rows=1, cols=4); table.style = 'Table Grid'
        hdr = table.rows[0].cells
        hdr[0].text, hdr[1].text, hdr[2].text, hdr[3].text = 'Ejercicio', 'Plan', 'Carga (70%)', 'RPE'
        for eid in ex_ids:
            ex = EXERCISES[eid]
            row = table.add_row().cells
            row[0].text = ex['nombre']
            row[1].text = ex['plan']
            rm = st.session_state.rms.get(eid, 0)
            row[2].text = "Peso Corp." if ex['tipo'] in ['pliométrico', 'autocarga'] else (f"{rm * 0.7:.1f} kg" if rm > 0 else "-")
            row[3].text = f"RPE {ex['rpe']}"
    buf = BytesIO(); doc.save(buf); buf.seek(0)
    return buf

if page == "📋 Perfil y 1RM":
    st.title("Ficha Clínica del Paciente")
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.subheader("Datos Personales")
        st.session_state.profile['nombre'] = st.text_input("Nombre", st.session_state.profile['nombre'])
        st.session_state.profile['apellidos'] = st.text_input("Apellidos", st.session_state.profile['apellidos'])
        st.session_state.profile['edad'] = st.number_input("Edad", 1, 120, st.session_state.profile['edad'])
    with c2:
        st.subheader("Configuración de Cargas (1RM)")
        st.write("Ingresa tu 1RM para los ejercicios de fuerza para calcular el 70% automático.")
        strength_list = [eid for eid, ex in EXERCISES.items() if ex['parte'] == 'Entrenamiento de Resistencia' and ex['tipo'] not in ['autocarga', 'pliométrico']]
        for eid in sorted(strength_list):
            val = st.session_state.rms.get(eid, 0.0)
            st.session_state.rms[eid] = st.number_input(f"1RM {EXERCISES[eid]['nombre']} (kg)", 0.0, 500.0, float(val), key=f"rm_{eid}")

elif page == "🏋️ Mis 4 Sesiones":
    st.title("Plan de Entrenamiento Diario")
    sel_id = st.radio("SELECCIONA TU SESIÓN:", [1, 2, 3, 4], format_func=lambda x: SESSIONS[x-1]['nombre'], horizontal=True)
    session = SESSIONS[sel_id-1]
    
    col_a, col_b = st.columns([2, 1])
    with col_a: st.success(f"Caminar 60 minutos es tu objetivo base diario.")
    with col_b:
        st.download_button("📥 Reporte Word", generate_docx(sel_id), f"Sesion_{sel_id}.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    for phase in ['Calentamiento', 'Entrenamiento de Resistencia', 'Enfriamiento']:
        st.markdown(f"<h2 class='phase-header'>{phase}</h2>", unsafe_allow_html=True)
        ex_ids = [eid for eid in session['ejercicios'] if EXERCISES.get(eid, {}).get('parte') == phase]
        cols = st.columns(3)
        for i, eid in enumerate(ex_ids):
            ex = EXERCISES[eid]
            with cols[i % 3]:
                is_plio = ex['tipo'] == 'pliométrico'
                rm = st.session_state.rms.get(eid, 0)
                carga = f"{rm * 0.7:.1f} kg" if rm > 0 else "Peso Corp."
                # NOTA: Sin sangría dentro del f-string para evitar el error de visualización
                st.markdown(f"""
<div class='exercise-card'>
<div style='position: relative;'>
<img src='{ex['imagen']}' style='width: 100%; border-radius: 15px; margin-bottom: 15px;'>
{"<span class='pliometrico-badge' style='position: absolute; top: 10px; right: 10px;'>Pliométrico</span>" if is_plio else ""}
</div>
<h4 style='margin: 0; text-transform: uppercase; font-size: 1.1em; color: #1e293b;'>{ex['nombre']}</h4>
<p style='color: #64748b; font-size: 0.85em; font-style: italic; margin-top: 5px; min-height: 45px;'>"{ex['descripcion']}"</p>
<hr style='margin: 15px 0; border: 0.5px solid #f1f5f9;'>
<div style='display: flex; justify-content: space-between;'>
<div><div class='stat-label'>Plan</div><div class='stat-value'>{ex['plan']}</div></div>
<div><div class='stat-label'>Carga</div><div class='stat-value'>{"Peso Corp." if is_plio or ex['tipo'] == 'autocarga' else carga}</div></div>
<div><div class='stat-label'>RPE</div><div class='stat-value'>{ex['rpe']}/10</div></div>
</div>
</div>
""", unsafe_allow_html=True)

elif page == "📈 Evolución":
    st.title("Seguimiento de Progreso")
    st.write("Resumen de tus cargas actuales:")
    res = []
    for eid, rm in st.session_state.rms.items():
        if rm > 0:
            res.append({"Ejercicio": EXERCISES[eid]['nombre'], "1RM": f"{rm} kg", "70% Actual": f"{rm*0.7:.1f} kg", "+10% Siguiente": f"{rm*0.7*1.1:.1f} kg"})
    if res: st.table(pd.DataFrame(res))
    else: st.warning("Completa tus 1RM en el perfil para ver la evolución.")

st.sidebar.markdown("---")
st.sidebar.caption("Diseñado bajo guías ACSM para pacientes con LLC.")
