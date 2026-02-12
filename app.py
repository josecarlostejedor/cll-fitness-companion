
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

# Estilos CSS mejorados
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

# Catálogo total de ejercicios (Replicado de data/exercises.ts)
EXERCISES = {
    # CALENTAMIENTO
    'w_walk_mob': {'nombre': 'Caminar + Movilidad', 'descripcion': 'Rápido, paso largo, círculos hombros, rodillas, puntillas.', 'tipo': 'aeróbico', 'imagen': 'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=400', 'agonistas': 'Cuerpo completo', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x Continuo', 'duracion': '2 min'},
    'w_balance': {'nombre': 'Equilibrio 1 pierna', 'descripcion': 'Mantener posición estable con una pierna elevada.', 'tipo': 'movilidad', 'imagen': 'https://images.unsplash.com/photo-1599901860904-17e6ed7083a0?w=400', 'agonistas': 'Glúteo medio, Cuádriceps', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 x 30s por pierna', 'duracion': '2 min'},
    'w_pushups_wall': {'nombre': 'Flexiones pared', 'descripcion': 'Empuje horizontal manteniendo alineación.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1598971639058-aba7c11210ee?w=400', 'agonistas': 'Pectoral mayor', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 15-20'},
    'w_squat_wall': {'nombre': 'Sentadilla pared', 'descripcion': 'Mantener posición de silla apoyado en pared.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1574680096145-d05b474e2158?w=400', 'agonistas': 'Cuádriceps', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 60s'},
    'w_jump': {'nombre': 'Saltos suaves', 'descripcion': 'Saltos suaves sobre puntas de pies.', 'tipo': 'aeróbico', 'imagen': 'https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=400', 'agonistas': 'Gemelos', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 2 min'},
    'w_ball_throw': {'nombre': 'Lanzamientos pelota', 'descripcion': 'Lanzar balón contra suelo o pared.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1599447421416-3414500d18a5?w=400', 'agonistas': 'Deltoides', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 x 15'},
    'w_prop_tobillo': {'nombre': 'Propiocepción tobillo', 'descripcion': 'Equilibrio dinámico sobre un pie.', 'tipo': 'movilidad', 'imagen': 'https://images.unsplash.com/photo-1599901860904-17e6ed7083a0?w=400', 'agonistas': 'Peroneos', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 x 30s'},
    'w_rodilla_brazo': {'nombre': 'Elevación rodilla+brazo', 'descripcion': 'Marcha exagerada coordinada.', 'tipo': 'aeróbico', 'imagen': 'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=400', 'agonistas': 'Psoas, Deltoides', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 1 min'},
    'w_sts': {'nombre': 'Sit-to-stand', 'descripcion': 'Sentarse y levantarse de silla sin manos.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?w=400', 'agonistas': 'Glúteos', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 x 10'},
    'w_step_up': {'nombre': 'Step-up', 'descripcion': 'Subir escalón alternando.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1538805060514-97d9cc17730c?w=400', 'agonistas': 'Glúteo mayor', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 20'},
    'w_boxeo': {'nombre': 'Boxeo suave', 'descripcion': 'Golpes al aire controlados.', 'tipo': 'aeróbico', 'imagen': 'https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?w=400', 'agonistas': 'Deltoides', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 2 min'},
    'w_step_lat': {'nombre': 'Step-ups laterales', 'descripcion': 'Subir escalón de lado.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1538805060514-97d9cc17730c?w=400', 'agonistas': 'Glúteo medio', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 10/lado'},
    'w_pushups_close': {'nombre': 'Flexiones cerradas', 'descripcion': 'Manos juntas para tríceps.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1598971639058-aba7c11210ee?w=400', 'agonistas': 'Tríceps', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 12'},
    'w_lunge_site': {'nombre': 'Estocadas sitio', 'descripcion': 'Bajar cadera sin avanzar.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1574680096145-d05b474e2158?w=400', 'agonistas': 'Cuádriceps', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 10/lado'},
    'w_jumping_jacks': {'nombre': 'Saltos tijera', 'descripcion': 'Coordinación brazos y piernas.', 'tipo': 'aeróbico', 'imagen': 'https://images.unsplash.com/photo-1601422407692-ec4eeec1d9b3?w=400', 'agonistas': 'Completo', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 2 min'},
    'w_glute_bridge': {'nombre': 'Puente glúteos', 'descripcion': 'Elevar cadera desde suelo.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1567598508481-65985588e295?w=400', 'agonistas': 'Glúteo mayor', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 x 12'},
    'w_band_curl': {'nombre': 'Flexión codo banda', 'descripcion': 'Calentar bíceps con banda.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1518310383802-640c2de311b2?w=400', 'agonistas': 'Bíceps', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 15'},
    'w_calf_raise': {'nombre': 'Elevación pantorrilla', 'descripcion': 'Puntillas rítmico.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=400', 'agonistas': 'Gemelos', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 20'},
    'w_shoulder_circ': {'nombre': 'Círculos hombros', 'descripcion': 'Círculos amplios brazos.', 'tipo': 'movilidad', 'imagen': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400', 'agonistas': 'Deltoides', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 x 15'},

    # RESISTENCIA
    'r_sq_body': {'nombre': 'Sentadilla peso corporal', 'descripcion': 'Flexión rodilla cadera 90 grados.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1566241142559-40e1bfc26ebc?w=400', 'agonistas': 'Cuádriceps', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_rdl': {'nombre': 'Peso muerto rumano', 'descripcion': 'Flexión cadera, barra/mancuernas.', 'tipo': 'sobrecarga', 'imagen': 'https://images.unsplash.com/photo-1534367507873-d2d7e24c797f?w=400', 'agonistas': 'Isquios', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_plank': {'nombre': 'Plancha abdominal', 'descripcion': 'Mantener cuerpo recto antebrazos.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400', 'agonistas': 'Core', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 30s'},
    'r_bench_bar': {'nombre': 'Press banca barra', 'descripcion': 'Empuje barra desde pecho.', 'tipo': 'barra olímpica', 'imagen': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400', 'agonistas': 'Pectoral', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_curl_flex': {'nombre': 'Curl + Press', 'descripcion': 'Flexión codo y elevación.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=400', 'agonistas': 'Bíceps, Hombro', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_row_db': {'nombre': 'Remo mancuernas', 'descripcion': 'Tracción hacia cadera.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1605296867304-46d5465a13f1?w=400', 'agonistas': 'Dorsal', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_lunge_db': {'nombre': 'Estocada con carga', 'descripcion': 'Paso adelante con mancuernas.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1574680096145-d05b474e2158?w=400', 'agonistas': 'Cuádriceps', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_hip_thrust': {'nombre': 'Hip Thrust', 'descripcion': 'Elevación pelvis con carga.', 'tipo': 'sobrecarga', 'imagen': 'https://images.unsplash.com/photo-1567598508481-65985588e295?w=400', 'agonistas': 'Glúteo', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_pallof': {'nombre': 'Press Pallof', 'descripcion': 'Resistir rotación banda.', 'tipo': 'autocarga', 'imagen': 'https://images.unsplash.com/photo-1518310383802-640c2de311b2?w=400', 'agonistas': 'Core', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_bench_db': {'nombre': 'Press banca mancuernas', 'descripcion': 'Empuje independiente.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=400', 'agonistas': 'Pectoral', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_shoulder_db': {'nombre': 'Press hombros DB', 'descripcion': 'Empuje vertical mancuernas.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1532029836916-f4874460e41f?w=400', 'agonistas': 'Deltoides', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_jump_sts': {'nombre': 'Salto Sit-to-Stand', 'descripcion': 'Salto explosivo desde silla.', 'tipo': 'pliométrico', 'imagen': 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?w=400', 'agonistas': 'Piernas (Potencia)', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_sq_sumo': {'nombre': 'Sentadilla sumo', 'descripcion': 'Pies abiertos con mancuerna.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1566241142559-40e1bfc26ebc?w=400', 'agonistas': 'Aductores, Glúteo', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_dl_conv': {'nombre': 'Peso muerto barra', 'descripcion': 'Tracción desde suelo.', 'tipo': 'barra olímpica', 'imagen': 'https://images.unsplash.com/photo-1534367507873-d2d7e24c797f?w=400', 'agonistas': 'Cadena posterior', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_row_bar': {'nombre': 'Remo barra', 'descripcion': 'Tracción barra inclinado.', 'tipo': 'barra olímpica', 'imagen': 'https://images.unsplash.com/photo-1605296867304-46d5465a13f1?w=400', 'agonistas': 'Espalda', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_curl_bar': {'nombre': 'Curl bíceps barra', 'descripcion': 'Flexión codos con barra.', 'tipo': 'barra olímpica', 'imagen': 'https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=400', 'agonistas': 'Bíceps', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_lat_raise': {'nombre': 'Elevaciones laterales', 'descripcion': 'Vuelos laterales.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1532029836916-f4874460e41f?w=400', 'agonistas': 'Hombro medio', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_box_step_1p': {'nombre': 'Subida caja 1 pierna', 'descripcion': 'Control subiendo caja.', 'tipo': 'pliométrico', 'imagen': 'https://images.unsplash.com/photo-1538805060514-97d9cc17730c?w=400', 'agonistas': 'Glúteo, Tobillo', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_lunge_lat_kb': {'nombre': 'Estocada lat kettlebell', 'descripcion': 'Paso lateral con carga.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400', 'agonistas': 'Aductores', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_fly_inc': {'nombre': 'Vuelo pecho inclinado', 'descripcion': 'Aperturas mancuerna.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400', 'agonistas': 'Pectoral superior', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_tri_ext': {'nombre': 'Extensión tríceps', 'descripcion': 'Skullcrushers mancuernas.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=400', 'agonistas': 'Tríceps', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_front_raise': {'nombre': 'Elevación frontal', 'descripcion': 'Elevación frente ojos.', 'tipo': 'mancuernas', 'imagen': 'https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=400', 'agonistas': 'Hombro anterior', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},
    'r_jump_sq': {'nombre': 'Sentadilla salto', 'descripcion': 'Potencia vertical.', 'tipo': 'pliométrico', 'imagen': 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?w=400', 'agonistas': 'Piernas (Potencia)', 'parte': 'Entrenamiento de Resistencia', 'rpe': 7, 'plan': '3 x 12'},

    # ENFRIAMIENTO
    'e_walk': {'nombre': 'Caminata suave', 'descripcion': 'Ritmo suave bajando pulsaciones.', 'tipo': 'aeróbico', 'imagen': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=400', 'agonistas': 'Completo', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 x 3 min'},
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

# Definición de las 4 Sesiones
SESSIONS = [
    {
        'id': 1, 
        'nombre': "Sesión 1: Estabilidad y Fuerza Base", 
        'ejercicios': [
            'w_walk_mob', 'w_balance', 'w_pushups_wall', 'w_squat_wall', 'w_jump', 'w_ball_throw',
            'r_sq_body', 'r_rdl', 'r_plank', 'r_bench_bar', 'r_curl_flex', 'r_row_db',
            'e_walk', 'e_cuad', 'e_isq', 'e_calf', 'e_bic', 'e_shoulder', 'e_cervical'
        ]
    },
    {
        'id': 2, 
        'nombre': "Sesión 2: Propiocepción y Empuje", 
        'ejercicios': [
            'w_walk_mob', 'w_prop_tobillo', 'w_rodilla_brazo', 'w_sts', 'w_step_up', 'w_boxeo',
            'r_lunge_db', 'r_hip_thrust', 'r_pallof', 'r_bench_db', 'r_shoulder_db', 'r_jump_sts',
            'e_walk', 'e_cuad', 'e_glute', 'e_adductor', 'e_isq', 'e_shoulder', 'e_cervical'
        ]
    },
    {
        'id': 3, 
        'nombre': "Sesión 3: Tracción y Salto Lateral", 
        'ejercicios': [
            'w_walk_mob', 'w_step_lat', 'w_pushups_close', 'w_lunge_site', 'w_jumping_jacks', 'w_glute_bridge',
            'r_sq_sumo', 'r_dl_conv', 'r_row_bar', 'r_curl_bar', 'r_lat_raise', 'r_box_step_1p',
            'e_walk', 'e_cuad', 'e_glute', 'e_isq', 'e_bic', 'e_shoulder', 'e_cervical'
        ]
    },
    {
        'id': 4, 
        'nombre': "Sesión 4: Fuerza Lateral y Movilidad", 
        'ejercicios': [
            'w_walk_mob', 'w_sts', 'w_band_curl', 'w_calf_raise', 'w_jump', 'w_shoulder_circ',
            'r_lunge_lat_kb', 'r_dl_conv', 'r_fly_inc', 'r_tri_ext', 'r_front_raise', 'r_jump_sq',
            'e_walk', 'e_cuad', 'e_glute', 'e_tri', 'e_chest', 'e_shoulder', 'e_cervical'
        ]
    }
]

# Inicialización de estado
if 'rms' not in st.session_state:
    st.session_state.rms = {}
if 'profile' not in st.session_state:
    st.session_state.profile = {'nombre': '', 'apellidos': '', 'sexo': 'Hombre', 'edad': 60}

# Sidebar - Navegación Profesional
st.sidebar.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='color: #4f46e5; margin-bottom: 0;'>CLL-FITNESS</h1>
        <p style='font-size: 0.8em; font-weight: 700; color: #94a3b8; text-transform: uppercase;'>Protocolo ACSM</p>
    </div>
    """, unsafe_allow_html=True)
page = st.sidebar.radio("MENÚ PRINCIPAL", ["📋 Mi Perfil / 1RM", "🏋️ Mis Sesiones", "📈 Mi Evolución"])

def generate_docx(session_id):
    session = next(s for s in SESSIONS if s['id'] == session_id)
    doc = Document()
    
    # Estilos del documento Word
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(10)

    # Header
    title = doc.add_heading('REPORTE DE ENTRENAMIENTO - PACIENTE LLC', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    p = doc.add_paragraph()
    p.add_run(f"Paciente: {st.session_state.profile['nombre']} {st.session_state.profile['apellidos']}").bold = True
    p.add_run(f" | Edad: {st.session_state.profile['edad']} | Sexo: {st.session_state.profile['sexo']}\n")
    p.add_run(f"Sesión: {session['nombre']}").bold = True
    p.add_run(f" | Fecha: {datetime.now().strftime('%d/%m/%Y')}")
    
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
            is_pliometrico = ex['tipo'] == 'pliométrico' or ex['tipo'] == 'autocarga'
            load = "Peso Corp." if is_pliometrico else (f"{rm * 0.7:.1f} kg" if rm > 0 else "-")
            row_cells[2].text = load
            row_cells[3].text = f"RPE {ex['rpe']}"

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

if page == "📋 Mi Perfil / 1RM":
    st.title("Gestión de Perfil Clínico")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("Datos del Paciente")
        st.session_state.profile['nombre'] = st.text_input("Nombre", st.session_state.profile['nombre'])
        st.session_state.profile['apellidos'] = st.text_input("Apellidos", st.session_state.profile['apellidos'])
        st.session_state.profile['sexo'] = st.selectbox("Sexo", ["Hombre", "Mujer", "Otro"], index=0)
        st.session_state.profile['edad'] = st.number_input("Edad", min_value=1, max_value=120, value=st.session_state.profile['edad'])
        
        st.info("💡 Consejo: Completa todos tus 1RM para que los cálculos de carga sean precisos.")

    with col2:
        st.subheader("Configuración de Cargas (1RM)")
        st.markdown("Ingresa tu **Repetición Máxima** solo para ejercicios de sobrecarga. Los pliométricos se calculan como Peso Corporal.")
        
        # Filtrar solo ejercicios de resistencia que necesitan carga
        strength_ex = [eid for eid, ex in EXERCISES.items() if ex['parte'] == 'Entrenamiento de Resistencia' and ex['tipo'] not in ['autocarga', 'pliométrico']]
        
        for eid in sorted(strength_ex):
            ex = EXERCISES[eid]
            current_rm = st.session_state.rms.get(eid, 0.0)
            st.session_state.rms[eid] = st.number_input(f"1RM {ex['nombre']} (kg)", min_value=0.0, value=float(current_rm), key=f"rm_{eid}")

elif page == "🏋️ Mis Sesiones":
    st.title("Entrenamiento Diario")
    
    # Selector de las 4 sesiones
    selected_session_id = st.radio(
        "Elige la sesión correspondiente a tu ciclo actual:",
        [s['id'] for s in SESSIONS],
        format_func=lambda x: next(s['nombre'] for s in SESSIONS if s['id'] == x),
        horizontal=True
    )
    
    session = next(s for s in SESSIONS if s['id'] == selected_session_id)
    
    st.markdown(f"### {session['nombre']}")
    
    # Barra de descarga y acciones
    col_dl, col_info = st.columns([1, 2])
    with col_dl:
        doc_buffer = generate_docx(session['id'])
        st.download_button(
            label="📥 Descargar Reporte PDF/Word",
            data=doc_buffer,
            file_name=f"Reporte_Sesion_{selected_session_id}_{st.session_state.profile['nombre']}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    with col_info:
        st.success("✅ Objetivo Base: Caminar 60 minutos hoy.")

    # Renderizar ejercicios por fases
    for phase in ['Calentamiento', 'Entrenamiento de Resistencia', 'Enfriamiento']:
        st.markdown(f"<h2 class='phase-header'>{phase}</h2>", unsafe_allow_html=True)
        ex_ids = [eid for eid in session['ejercicios'] if EXERCISES.get(eid, {}).get('parte') == phase]
        
        # Crear filas de 3 columnas para los ejercicios
        cols = st.columns(3)
        for i, eid in enumerate(ex_ids):
            ex = EXERCISES[eid]
            with cols[i % 3]:
                is_pliometrico = ex['tipo'] == 'pliométrico'
                rm = st.session_state.rms.get(eid, 0)
                carga_calculada = f"{rm * 0.7:.1f} kg" if rm > 0 else "Peso Corp."
                
                # Visualización de la tarjeta
                st.markdown(f"""
                <div class='exercise-card'>
                    <div style='position: relative;'>
                        <img src='{ex['imagen']}' style='width: 100%; border-radius: 15px; margin-bottom: 15px;'>
                        {"<span class='pliometrico-badge' style='position: absolute; top: 10px; right: 10px;'>Pliométrico</span>" if is_pliometrico else ""}
                    </div>
                    <h4 style='margin: 0; text-transform: uppercase; font-size: 1.1em; color: #1e293b;'>{ex['nombre']}</h4>
                    <p style='color: #64748b; font-size: 0.85em; font-style: italic; margin-top: 5px; min-height: 45px;'>"{ex['descripcion']}"</p>
                    <hr style='margin: 15px 0; border: 0.5px solid #f1f5f9;'>
                    <div style='display: flex; justify-content: space-between;'>
                        <div>
                            <div class='stat-label'>Plan</div>
                            <div class='stat-value'>{ex['plan']}</div>
                        </div>
                        <div>
                            <div class='stat-label'>Carga (70%)</div>
                            <div class='stat-value'>{"Peso Corp." if is_pliometrico or ex['tipo'] == 'autocarga' else carga_calculada}</div>
                        </div>
                        <div>
                            <div class='stat-label'>RPE</div>
                            <div class='stat-value'>{ex['rpe']}/10</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

elif page == "📈 Mi Evolución":
    st.title("Seguimiento de Progreso")
    
    st.markdown("#### Resumen de Cargas de Trabajo")
    data = []
    for eid, rm in st.session_state.rms.items():
        if rm > 0:
            ex = EXERCISES[eid]
            data.append({
                "Ejercicio": ex['nombre'],
                "1RM Base": f"{rm} kg",
                "Carga Actual (70%)": f"{rm * 0.7:.1f} kg",
                "Próximo Incremento (+10%)": f"{rm * 0.7 * 1.1:.1f} kg"
            })
    
    if data:
        st.table(pd.DataFrame(data))
        st.info("💡 Recuerda: Si completas 12 repeticiones en 3 series durante 2 sesiones seguidas, incrementa la carga un 10%.")
    else:
        st.warning("⚠️ No hay datos de 1RM registrados aún.")

st.sidebar.markdown("---")
st.sidebar.info("Este sistema es una herramienta de apoyo. Consulta siempre con tu hematólogo antes de realizar cambios intensos en tu rutina.")
