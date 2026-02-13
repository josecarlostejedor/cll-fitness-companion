
import { Exercise, Session } from '../types';

export const EXERCISES: Exercise[] = [
  // --- CALENTAMIENTO ---
  { 
    id: 'w_walk_mob_s1', 
    nombre: 'Marcha + Movilidad Articular', 
    descripcion: 'Marcha en el sitio levantando rodillas y haciendo círculos con los hombros.', 
    tipo: 'aeróbico', 
    imagen: '/images/marcha-hombros.png', 
    agonistas: 'Sistema Cardio', sinergistas: 'Tren inferior', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 5, duracion: '3 min' 
  },
  { 
    id: 'w_balance_s1', 
    nombre: 'Equilibrio Unipodal', 
    descripcion: 'Mantenerse sobre una pierna (ayuda de silla si es necesario).', 
    tipo: 'movilidad', 
    imagen: '/images/equilibrio.png', 
    agonistas: 'Glúteo medio', sinergistas: 'Tobillo', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 4, duracion: '2 min' 
  },

  // --- ENTRENAMIENTO DE RESISTENCIA ---
  { 
    id: 'r_squat_s1', 
    nombre: 'Sentadilla (Box Squat)', 
    descripcion: 'Sentarse y levantarse de una silla con control.', 
    tipo: 'autocarga', 
    imagen: '/images/sentadilla.png', 
    agonistas: 'Cuádriceps', sinergistas: 'Glúteo mayor', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, repeticiones: 12 
  },
  { 
    id: 'r_pushups_s1', 
    nombre: 'Flexiones en Pared', 
    descripcion: 'Flexo-extensión de brazos apoyado en pared.', 
    tipo: 'autocarga', 
    imagen: '/images/flexiones-pared.png', 
    agonistas: 'Pectoral mayor', sinergistas: 'Tríceps', estabilizadores: 'Serrato', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, repeticiones: 12 
  },
  { 
    id: 'r_rdl_s1', 
    nombre: 'Peso Muerto Rumano', 
    descripcion: 'Bisagra de cadera bajando peso hasta las rodillas.', 
    tipo: 'sobrecarga', 
    imagen: '/images/peso-muerto.png', 
    agonistas: 'Isquiotibiales', sinergistas: 'Glúteo', estabilizadores: 'Erectores', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, repeticiones: 12 
  },
  { 
    id: 'r_row_s1', 
    nombre: 'Remo con Mancuerna', 
    descripcion: 'Tracción de carga hacia la cadera manteniendo espalda recta.', 
    tipo: 'mancuernas', 
    imagen: '/images/remo.png', 
    agonistas: 'Dorsal ancho', sinergistas: 'Bíceps', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, repeticiones: 12 
  },
  { 
    id: 'r_press_s1', 
    nombre: 'Press Militar Sentado', 
    descripcion: 'Empuje vertical sobre la cabeza desde los hombros.', 
    tipo: 'mancuernas', 
    imagen: '/images/press-hombros.png', 
    agonistas: 'Deltoides anterior', sinergistas: 'Tríceps', estabilizadores: 'Trapecio', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, repeticiones: 10 
  },

  // --- ENFRIAMIENTO ---
  { 
    id: 'c_stretch_s1', 
    nombre: 'Estiramiento Global', 
    descripcion: 'Estiramientos sostenidos de grandes grupos musculares.', 
    tipo: 'movilidad', 
    imagen: '/images/estiramiento.png', 
    agonistas: 'Varios', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '5 min' 
  },
  { 
    id: 'c_breathing_s1', 
    nombre: 'Respiración Diafragmática', 
    descripcion: 'Controlar la respiración inflando el abdomen sentado.', 
    tipo: 'movilidad', 
    imagen: '/images/respiracion.png', 
    agonistas: 'Diafragma', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 2, duracion: '2 min' 
  }
];

export const SESSIONS: Session[] = [
  { 
    id: 1, 
    nombre: "Sesión 1: Fuerza y Estabilidad", 
    ejercicios: [
      'w_walk_mob_s1', 'w_balance_s1', 
      'r_squat_s1', 'r_pushups_s1', 'r_rdl_s1', 'r_row_s1', 'r_press_s1', 
      'c_stretch_s1', 'c_breathing_s1'
    ] 
  }
];
