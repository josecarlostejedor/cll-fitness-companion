
import streamlit as st
import pandas as pd
import base64
import os
from io import BytesIO
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, ns

# Configuración
st.set_page_config(page_title="CLL-CARE Prescripción", layout="wide", initial_sidebar_state="expanded")

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return f"data:image/jpg;base64,{base64.b64encode(img_file.read()).decode()}"
    return "https://via.placeholder.com/600x400?text=Imagen+No+Encontrada"

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

def set_cell_background(cell, fill_color):
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(ns.qn('w:fill'), fill_color)
    cell._tc.get_or_add_tcPr().append(shading_elm)

# Catálogo completo (Asegurando que todas las imágenes y datos estén presentes)
from data.exercises import EXERCISES as EX_DATA, SESSIONS as SESS_DATA

# Convertimos a formato diccionario para búsqueda rápida
EXERCISES = {ex.id: {
    'nombre': ex.nombre, 
    'desc': ex.descripcion, 
    'img': ex.imagen.lstrip('/'), 
    'parte': ex.parte_de_la_sesion.replace('Entrenamiento de ', ''),
    'rpe': ex.rpe_recomendado,
    'plan': ex.duracion if ex.duracion else f"{ex.series}x{ex.repeticiones}"
} for ex in EX_DATA}

SESSIONS = [{'id': s.id, 'nombre': s.nombre, 'ejercicios': s.ejercicios} for s in SESS_DATA]

if 'rms' not in st.session_state: st.session_state.rms = {}
if 'profile' not in st.session_state: st.session_state.profile = {'nombre': '', 'apellidos': '', 'edad': 65, 'sexo': 'Hombre'}

def generate_docx(session_id):
    doc = Document()
    session = next(s for s in SESSIONS if s['id'] == session_id)
    
    for section in doc.sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)
        
        # Encabezado en todas las páginas
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

    doc.add_heading('PLAN TERAPÉUTICO CLL-CARE', 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_patient = p_info.add_run(f"Paciente: {st.session_state.profile['nombre']} {st.session_state.profile['apellidos']} ({st.session_state.profile['sexo']})")
    run_patient.bold = True
    p_info.add_run(f"\nSesión: {session['id']} - {session['nombre']}")

    phases = ['Calentamiento', 'Resistencia', 'Enfriamiento']
    for idx, phase_label in enumerate(phases):
        if idx > 0: doc.add_page_break()
        doc.add_heading(phase_label.upper(), level=1)
        
        ex_ids = [eid for eid in session['ejercicios'] if phase_label in EXERCISES[eid]['parte']]
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
                    p_name.add_run(f"EJERCICIO:\n{ex['nombre']}").bold = True
                    
                    if os.path.exists(ex['img']):
                        cell.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
                        cell.paragraphs[-1].add_run().add_picture(ex['img'], width=Inches(1.5))
                    
                    rm = st.session_state.rms.get(eid, 0.0)
                    is_autocarga = any(word in ex['nombre'].lower() for word in ['peso corporal', 'plancha', 'pared', 'equilibrio', 'sit-to-stand', 'paso', 'tijera', 'rodilla', 'boxeo', 'salto'])
                    carga = f"{int(round(rm * 0.7))} kg" if (rm > 0 and not is_autocarga) else "P.C."
                    
                    p_data = cell.add_paragraph()
                    p_data.add_run(f"Plan: {ex['plan']}\nCarga: {carga}\nRPE: {ex['rpe']}/10").font.size = Pt(9)

        if phase_label == 'Enfriamiento':
            doc.add_heading('INSTRUCCIONES DE REPETICIÓN', level=2)
            p_inst = doc.add_paragraph()
            p_inst.add_run("Debe repetir el protocolo completo ").font.size = Pt(11)
            p_inst.add_run("3 VECES").bold = True
            p_inst.add_run(" por sesión. Al terminar el enfriamiento, descanse 3 minutos antes de volver a empezar. Caminar 60 minutos cada día de la semana para combatir la fatiga oncológica.").font.size = Pt(11)

    # Página Final Combinada
    doc.add_page_break()
    doc.add_heading('COMPROMISO DIARIO', level=1)
    img_comp = "images/compromiso_diario.jpg"
    if os.path.exists(img_comp):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.paragraphs[-1].add_run().add_picture(img_comp, width=Inches(3.5))
    
    p_comp = doc.add_paragraph()
    p_comp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_c = p_comp.add_run("Caminar 60 minutos cada día de la semana para combatir la fatiga oncológica.")
    run_c.bold = True
    run_c.font.size = Pt(14)
    run_c.font.color.rgb = RGBColor(200, 0, 0)

    doc.add_paragraph("\n")
    doc.add_heading('ESCALA DE BORG (Percepción del esfuerzo)', level=2)
    doc.add_paragraph("Nos referimos a medir la percepción del esfuerzo, mientras realizamos actividad física. Marque su sensación percibida con una X.")
    
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
        cell_top = borg_table.cell(0, i)
        set_cell_background(cell_top, color)
        p = cell_top.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run(f"{val}\n").bold = True
        p.add_run(desc).font.size = Pt(7)
        borg_table.cell(1, i).height = Inches(0.4)

    target = BytesIO()
    doc.save(target)
    return target.getvalue()

# UI de Streamlit
st.sidebar.title("CLL-CARE ADMIN")
page = st.sidebar.radio("Secciones", ["👤 Perfil Paciente", "🏋️ Prescripción Sesiones", "⚙️ Gestión de RM"])

if page == "👤 Perfil Paciente":
    st.title("Historial del Paciente")
    c1, c2, c3 = st.columns(3)
    with c1: st.session_state.profile['nombre'] = st.text_input("Nombre", st.session_state.profile['nombre'])
    with c2: st.session_state.profile['apellidos'] = st.text_input("Apellidos", st.session_state.profile['apellidos'])
    with c3: st.session_state.profile['sexo'] = st.selectbox("Sexo", ["Hombre", "Mujer", "Otro"])
    st.session_state.profile['edad'] = st.number_input("Edad", 1, 120, int(st.session_state.profile['edad']))
    st.success("Recomendación Médica: Caminar 60 min cada día para combatir la fatiga oncológica.")

elif page == "⚙️ Gestión de RM":
    st.title("Gestión de 1RM")
    for eid, ex in EXERCISES.items():
        if 'Resistencia' in ex['parte']:
            val = st.number_input(f"1RM {ex['nombre']} (kg)", value=float(st.session_state.rms.get(eid, 0.0)), key=eid)
            st.session_state.rms[eid] = int(val)

elif page == "🏋️ Prescripción Sesiones":
    st.title("Protocolos de Entrenamiento")
    sid = st.radio("Seleccionar Protocolo:", [s['id'] for s in SESSIONS], format_func=lambda x: f"Sesión {x}", horizontal=True)
    st.download_button(label="📥 Descargar Informe Word Profesional", data=generate_docx(sid), file_name=f"Prescripcion_{st.session_state.profile['nombre']}.docx")
    
    active_sess = next(s for s in SESSIONS if s['id'] == sid)
    st.markdown(f"### {active_sess['nombre']}")
    cols = st.columns(3)
    for i, eid in enumerate(active_sess['ejercicios']):
        ex = EXERCISES[eid]
        with cols[i % 3]:
            st.image(get_base64_image(ex['img']), caption=ex['nombre'])
