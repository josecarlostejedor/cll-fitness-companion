
import streamlit as st
import pandas as pd
import base64
import os
from io import BytesIO
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement, ns

# Configuración
st.set_page_config(page_title="CLL-CARE Prescripción", layout="wide", initial_sidebar_state="expanded")

# Función para convertir imagen local a base64 (para Streamlit)
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return f"data:image/jpg;base64,{base64.b64encode(img_file.read()).decode()}"
    return "https://via.placeholder.com/600x400?text=Imagen+No+Encontrada"

# Helper para añadir número de página en docx
def add_page_number(run):
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(ns.qn('w:fldCharType'), 'begin')
    run._r.append(fldChar1)
    instrText = OxmlElement('w:instrText')
    instrText.set(ns.qn('xml:space'), 'preserve')
    instrText.text = "PAGE"
    run._r.append(instrText)
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(ns.qn('w:fldCharType'), 'end')
    run._r.append(fldChar2)

# Helper para colorear celdas
def set_cell_background(cell, fill_color):
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(ns.qn('w:fill'), fill_color)
    cell._tc.get_or_add_tcPr().append(shading_elm)

# CSS para UI de Streamlit
st.markdown("""
<style>
.exercise-card {
    background-color: white; padding: 1.5rem; border-radius: 1.5rem; border: 1px solid #f1f5f9;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 1.5rem;
    display: flex; flex-direction: column; height: 100%;
}
.ex-image { width: 100%; height: 180px; object-fit: cover; border-radius: 1rem; margin-bottom: 1rem; }
.clinical-badge {
    font-size: 0.65em; font-weight: 800; color: #2563eb; text-transform: uppercase;
    background: #eff6ff; padding: 3px 10px; border-radius: 999px; width: fit-content; margin-bottom: 0.5rem;
}
.label-val { display: flex; justify-content: space-between; font-size: 0.85em; margin-top: 5px; }
.instruction-box {
    background-color: #f0f7ff; border: 2px solid #2563eb; padding: 2rem; border-radius: 1.5rem; margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Catálogo completo sincronizado (Simplificado para el ejemplo pero funcional con tus imágenes)
EXERCISES = {
    # SESIÓN 1
    's1_w_1': {'nombre': 'Caminar círculos + movilidad', 'desc': 'Rápido, paso largo, círculos hombros, rodillas.', 'img': 'images/caminar_movilidad.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's1_w_2': {'nombre': 'Equilibrio 1 pierna', 'desc': 'Mantener el equilibrio sobre un solo pie.', 'img': 'images/equilibrio.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's1_w_3': {'nombre': 'Flexiones pared/suelo', 'desc': 'Empuje de brazos.', 'img': 'images/flexiones.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 min'},
    's1_w_4': {'nombre': 'Sentadilla pared', 'desc': 'Isometría apoyado en la pared.', 'img': 'images/sentadilla_pared.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '1 min'},
    's1_w_5': {'nombre': 'Saltar', 'desc': 'Saltos suaves y controlados.', 'img': 'images/saltar.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's1_w_6': {'nombre': 'Lanzamientos pelota', 'desc': 'Lanzar y recibir una pelota.', 'img': 'images/lanzamientos.jpg', 'parte': 'Calentamiento', 'rpe': 6, 'plan': '2 min'},
    's1_r_1': {'nombre': 'Sentadilla peso corporal', 'desc': 'Flexión de cadera y rodillas.', 'img': 'images/sentadilla_libre.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's1_r_2': {'nombre': 'Peso muerto rumano', 'desc': 'Bisagra de cadera con carga.', 'img': 'images/peso_muerto.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's1_r_3': {'nombre': 'Plancha Isométrica', 'desc': 'Core estable.', 'img': 'images/plancha.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '30s'},
    's1_r_4': {'nombre': 'Press banca barra', 'desc': 'Empuje horizontal.', 'img': 'images/press_banca.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's1_r_5': {'nombre': 'Curl bíceps + flex hombro', 'desc': 'Tren superior.', 'img': 'images/curl_hombro.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's1_r_6': {'nombre': 'Remo mancuernas', 'desc': 'Tracción bilateral.', 'img': 'images/remo.jpg', 'parte': 'Resistencia', 'rpe': 7, 'plan': '12 rep'},
    's1_c_1': {'nombre': 'Caminata + respiración', 'desc': 'Vuelta a la calma.', 'img': 'images/caminata_suave.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '3 min'},
    's1_c_2': {'nombre': 'Estiramiento cuádriceps', 'desc': 'Talón al glúteo.', 'img': 'images/est_cuadriceps.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's1_c_3': {'nombre': 'Estiramiento isquios', 'desc': 'Pierna extendida.', 'img': 'images/est_isquios.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's1_c_4': {'nombre': 'Estiramiento pantorrilla', 'desc': 'Apoyo en pared.', 'img': 'images/est_gemelos.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's1_c_5': {'nombre': 'Estiramiento bíceps', 'desc': 'Extensión de brazo.', 'img': 'images/est_biceps.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's1_c_6': {'nombre': 'Estiramiento hombros', 'desc': 'Cruzado frontal.', 'img': 'images/est_hombros.jpg', 'parte': 'Enfriamiento', 'rpe': 3, 'plan': '1 min'},
    's1_c_7': {'nombre': 'Movilidad cervical', 'desc': 'Rotaciones suaves.', 'img': 'images/movilidad_cuello.jpg', 'parte': 'Enfriamiento', 'rpe': 2, 'plan': '2 min'},
}

SESSIONS = [
    {'id': 1, 'nombre': "Sesión 1: Estabilidad Base", 'ejercicios': ['s1_w_1', 's1_w_2', 's1_w_3', 's1_w_4', 's1_w_5', 's1_w_6', 's1_r_1', 's1_r_2', 's1_r_3', 's1_r_4', 's1_r_5', 's1_r_6', 's1_c_1', 's1_c_2', 's1_c_3', 's1_c_4', 's1_c_5', 's1_c_6', 's1_c_7']}
]

if 'rms' not in st.session_state: st.session_state.rms = {}
if 'profile' not in st.session_state: st.session_state.profile = {'nombre': '', 'apellidos': '', 'edad': 65, 'sexo': 'Hombre'}

def generate_docx(session_id):
    doc = Document()
    session = SESSIONS[session_id-1]
    
    # Configuración de página y encabezados
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)
        
        # Encabezado personalizado
        header = section.header
        htext = header.paragraphs[0]
        htext.text = "Rutina de trabajo creada por el Dr. Juan Luis Sánchez, Víctor Vicente y José Carlos Tejedor"
        htext.style = doc.styles['Caption']
        htext.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Pie de página con numeración
        footer = section.footer
        ftext = footer.paragraphs[0]
        ftext.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = ftext.add_run("Página ")
        add_page_number(run)

    # TITULO PRINCIPAL
    title = doc.add_heading('PLAN TERAPÉUTICO CLL-CARE', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_patient = p_info.add_run(f"Paciente: {st.session_state.profile['nombre']} {st.session_state.profile['apellidos']} ({st.session_state.profile['sexo']})")
    run_patient.bold = True
    p_info.add_run(f"\nSesión: {session['id']} - {session['nombre']}")

    # BLOQUES DE EJERCICIO
    phases = ['Calentamiento', 'Resistencia', 'Enfriamiento']
    for idx, phase_label in enumerate(phases):
        if idx > 0: doc.add_page_break()
        doc.add_heading(phase_label.upper(), level=1)
        
        ex_ids = [eid for eid in session['ejercicios'] if EXERCISES[eid]['parte'] == phase_label]
        table = doc.add_table(rows=0, cols=3)
        table.style = 'Table Grid'
        
        for i in range(0, len(ex_ids), 3):
            row_cells = table.add_row().cells
            for j in range(3):
                if i + j < len(ex_ids):
                    eid = ex_ids[i + j]
                    ex = EXERCISES[eid]
                    cell = row_cells[j]
                    
                    p_name = cell.paragraphs[0]
                    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    run_name = p_name.add_run(f"EJERCICIO:\n{ex['nombre']}")
                    run_name.bold = True
                    run_name.font.size = Pt(10)
                    
                    if os.path.exists(ex['img']):
                        p_img = cell.add_paragraph()
                        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        p_img.add_run().add_picture(ex['img'], width=Inches(1.5))
                    
                    rm = st.session_state.rms.get(eid, 0.0)
                    is_autocarga = any(word in ex['nombre'].lower() for word in ['peso corporal', 'plancha', 'pared', 'equilibrio', 'sit-to-stand', 'paso', 'tijera', 'rodilla', 'boxeo', 'salto'])
                    carga = f"{int(round(rm * 0.7))} kg" if (rm > 0 and not is_autocarga) else "P.C."
                    
                    p_data = cell.add_paragraph()
                    p_data.add_run(f"Plan: {ex['plan']}\n").font.size = Pt(9)
                    p_data.add_run(f"Carga: {carga}\n").font.size = Pt(9)
                    p_data.add_run(f"RPE: {ex['rpe']}/10").font.size = Pt(9)

        # Si es ENFRIAMIENTO, añadir instrucciones justo debajo
        if phase_label == 'Enfriamiento':
            doc.add_heading('INSTRUCCIONES DE REPETICIÓN', level=2)
            p_inst = doc.add_paragraph()
            p_inst.add_run("Debe repetir el protocolo completo ").font.size = Pt(11)
            p_inst.add_run("3 VECES").bold = True
            p_inst.add_run(" por sesión. Al terminar el enfriamiento, descanse 3 minutos antes de volver a empezar. Caminar 60 minutos cada día para combatir la fatiga oncológica.").font.size = Pt(11)

    # PÁGINA FINAL: COMPROMISO Y BORG
    doc.add_page_break()
    doc.add_heading('COMPROMISO DIARIO Y SEGUIMIENTO', level=1)
    
    # Compromiso Diario
    img_comp = "images/compromiso_diario.jpg"
    if os.path.exists(img_comp):
        p_ic = doc.add_paragraph()
        p_ic.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_ic.add_run().add_picture(img_comp, width=Inches(4))
    
    p_comp = doc.add_paragraph()
    p_comp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_comp = p_comp.add_run("Caminar 60 minutos cada día de la semana para combatir la fatiga oncológica.")
    run_comp.bold = True
    run_comp.font.size = Pt(14)
    run_comp.font.color.rgb = RGBColor(200, 0, 0)
    
    doc.add_paragraph("\n") # Espacio
    
    # Escala de Borg
    doc.add_heading('ESCALA DE BORG (Percepción del esfuerzo)', level=2)
    doc.add_paragraph("Marque con una 'X' la intensidad percibida durante la sesión.")
    
    borg_data = [
        ("0", "Reposo", "D9E9FF"), ("1", "M. Ligero", "D9E9FF"), ("2", "M. Ligero", "D9E9FF"),
        ("3", "Ligero", "D9FFD9"), ("4", "Algo Pesado", "D9FFD9"), 
        ("5", "Pesado", "FFFFD9"), ("6", "Más Pesado", "FFFFD9"),
        ("7", "Muy Pesado", "FFE9D9"), ("8", "Muy Muy Pesado", "FFE9D9"),
        ("9", "Máximo", "FFD9D9"), ("10", "Extremo", "FFD9D9")
    ]
    
    borg_table = doc.add_table(rows=2, cols=11)
    borg_table.style = 'Table Grid'
    
    for i, (val, desc, color) in enumerate(borg_data):
        # Fila superior
        cell_top = borg_table.cell(0, i)
        set_cell_background(cell_top, color)
        p_bt = cell_top.paragraphs[0]
        p_bt.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_bt.add_run(f"{val}\n").bold = True
        p_bt.add_run(desc).font.size = Pt(7)
        
        # Fila inferior
        cell_bottom = borg_table.cell(1, i)
        cell_bottom.height = Inches(0.4)

    target = BytesIO()
    doc.save(target)
    return target.getvalue()

# Sidebar y lógica de Streamlit (Se mantiene igual)
st.sidebar.title("CLL-CARE ADMIN")
page = st.sidebar.radio("Secciones", ["👤 Perfil Paciente", "🏋️ Prescripción Sesiones", "⚙️ Gestión de RM"])

if page == "👤 Perfil Paciente":
    st.title("Historial del Paciente")
    c1, c2, c3 = st.columns(3)
    with c1: st.session_state.profile['nombre'] = st.text_input("Nombre", st.session_state.profile['nombre'])
    with c2: st.session_state.profile['apellidos'] = st.text_input("Apellidos", st.session_state.profile['apellidos'])
    with c3: st.session_state.profile['sexo'] = st.selectbox("Sexo", ["Hombre", "Mujer", "Otro"])
    st.session_state.profile['edad'] = st.number_input("Edad", 1, 120, st.session_state.profile['edad'])
    st.success("Recomendación Médica: Caminar 60 min cada día para combatir la fatiga oncológica.")

elif page == "⚙️ Gestión de RM":
    st.title("Gestión de 1RM")
    for eid, ex in EXERCISES.items():
        if ex['parte'] == 'Resistencia':
            val = st.number_input(f"1RM {ex['nombre']} (kg)", value=float(st.session_state.rms.get(eid, 0.0)), key=eid)
            st.session_state.rms[eid] = int(val)

elif page == "🏋️ Prescripción Sesiones":
    st.title("Protocolos de Entrenamiento")
    sid = st.radio("Seleccionar Protocolo:", [1], horizontal=True)
    st.download_button(label="📥 Descargar Informe Word Profesional", data=generate_docx(sid), file_name=f"Prescripcion_{st.session_state.profile['nombre']}.docx")
    
    # Vista previa en pantalla (Streamlit)
    ex_ids = EXERCISES.keys()
    cols = st.columns(3)
    for i, eid in enumerate(ex_ids):
        ex = EXERCISES[eid]
        with cols[i % 3]:
            img_b64 = get_base64_image(ex['img'])
            st.markdown(f"""<div class="exercise-card"><img src="{img_b64}" class="ex-image"><div class="clinical-badge">{ex['parte']}</div><b>{ex['nombre']}</b><p>{ex['desc']}</p></div>""", unsafe_allow_html=True)
