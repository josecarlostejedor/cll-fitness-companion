
import { Exercise, Session } from '../types';

export const EXERCISES: Exercise[] = [
  // --- CALENTAMIENTO (6 Tareas) ---
  { 
    id: 's1_w_1', 
    nombre: 'Marcha + Círculos + Movilidad', 
    descripcion: 'Rápido, paso largo, círculos hombros, rodillas, puntillas, lateral trote.', 
    tipo: 'aeróbico', 
    imagen: '/images/marcha_movilidad.png', 
    agonistas: 'General', sinergistas: '-', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '2 min' 
  },
  { 
    id: 's1_w_2', 
    nombre: 'Equilibrio 1 Pierna', 
    descripcion: 'Mantener el equilibrio sobre una sola pierna.', 
    tipo: 'movilidad', 
    imagen: '/images/equilibrio_unipodal.png', 
    agonistas: 'Glúteo medio', sinergistas: '-', estabilizadores: 'Tobillo/Core', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '2 min' 
  },
  { 
    id: 's1_w_3', 
    nombre: 'Flexiones Pared/Suelo', 
    descripcion: 'Empuje de brazos contra pared o suelo según nivel.', 
    tipo: 'autocarga', 
    imagen: '/images/flexiones.png', 
    agonistas: 'Pectoral', sinergistas: 'Tríceps', estabilizadores: 'Serrato', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '1 min' 
  },
  { 
    id: 's1_w_4', 
    nombre: 'Sentadilla Pared', 
    descripcion: 'Mantener posición de silla apoyado en la pared.', 
    tipo: 'autocarga', 
    imagen: '/images/isometria_pared.png', 
    agonistas: 'Cuádriceps', sinergistas: '-', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '1 min' 
  },
  { 
    id: 's1_w_5', 
    nombre: 'Saltar', 
    descripcion: 'Saltos suaves controlados.', 
    tipo: 'pliométrico', 
    imagen: '/images/saltos.png', 
    agonistas: 'Gemelos', sinergistas: 'Cuádriceps', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '2 min' 
  },
  { 
    id: 's1_w_6', 
    nombre: 'Lanzamientos Pelota', 
    descripcion: 'Lanzar y recibir pelota contra pared o compañero.', 
    tipo: 'movilidad', 
    imagen: '/images/lanzamientos.png', 
    agonistas: 'Hombros', sinergistas: 'Bíceps', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '2 min' 
  },

  // --- RESISTENCIA (6 Tareas - 3x12 al 70%) ---
  { 
    id: 's1_r_1', 
    nombre: 'Sentadilla Peso Corporal', 
    descripcion: 'Sentadilla clásica con control motor.', 
    tipo: 'autocarga', 
    imagen: '/images/sentadilla_libre.png', 
    agonistas: 'Cuádriceps/Glúteo', sinergistas: '-', estabilizadores: 'Erectores espinales', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },
  { 
    id: 's1_r_2', 
    nombre: 'Peso Muerto Rumano', 
    descripcion: 'Bisagra de cadera con carga controlada.', 
    tipo: 'sobrecarga', 
    imagen: '/images/peso_muerto_rumano.png', 
    agonistas: 'Isquiotibiales', sinergistas: 'Glúteo mayor', estabilizadores: 'Lumbar', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },
  { 
    id: 's1_r_3', 
    nombre: 'Plancha Isométrica', 
    descripcion: 'Mantener bloque rígido sobre antebrazos.', 
    tipo: 'autocarga', 
    imagen: '/images/plancha.png', 
    agonistas: 'Recto abdominal', sinergistas: 'Oblicuos', estabilizadores: 'Hombros', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: '30s' 
  },
  { 
    id: 's1_r_4', 
    nombre: 'Press Banca Barra', 
    descripcion: 'Empuje horizontal con barra olímpica o similar.', 
    tipo: 'barra olímpica', 
    imagen: '/images/press_banca.png', 
    agonistas: 'Pectoral mayor', sinergistas: 'Tríceps', estabilizadores: 'Deltoides ant.', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },
  { 
    id: 's1_r_5', 
    nombre: 'Curl Bíceps + Flex Hombro', 
    descripcion: 'Flexión de codo seguido de elevación frontal.', 
    tipo: 'mancuernas', 
    imagen: '/images/curl_flexion.png', 
    agonistas: 'Bíceps/Deltoides ant.', sinergistas: '-', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },
  { 
    id: 's1_r_6', 
    nombre: 'Remo Mancuernas', 
    descripcion: 'Tracción bilateral inclinada hacia la cadera.', 
    tipo: 'mancuernas', 
    imagen: '/images/remo_mancuernas.png', 
    agonistas: 'Dorsal ancho', sinergistas: 'Bíceps', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },

  // --- ENFRIAMIENTO (7 Tareas) ---
  { 
    id: 's1_c_1', 
    nombre: 'Caminata + Respiración', 
    descripcion: 'Caminar suave controlando inhalación diafragmática.', 
    tipo: 'aeróbico', 
    imagen: '/images/caminata_respiracion.png', 
    agonistas: 'Diafragma', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '3 min' 
  },
  { 
    id: 's1_c_2', 
    nombre: 'Estiramiento Cuádriceps', 
    descripcion: 'Llevar talón al glúteo manteniendo rodillas juntas.', 
    tipo: 'movilidad', 
    imagen: '/images/est_cuadriceps.png', 
    agonistas: 'Cuádriceps', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_3', 
    nombre: 'Estiramiento Isquios', 
    descripcion: 'Pierna extendida al frente buscando punta del pie.', 
    tipo: 'movilidad', 
    imagen: '/images/est_isquios.png', 
    agonistas: 'Isquiotibiales', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_4', 
    nombre: 'Estiramiento Pantorrilla', 
    descripcion: 'Apoyo en pared estirando el gastrocnemio.', 
    tipo: 'movilidad', 
    imagen: '/images/est_gemelos.png', 
    agonistas: 'Tríceps sural', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_5', 
    nombre: 'Estiramiento Bíceps', 
    descripcion: 'Extensión de brazo con palma hacia afuera.', 
    tipo: 'movilidad', 
    imagen: '/images/est_biceps.png', 
    agonistas: 'Bíceps braquial', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_6', 
    nombre: 'Estiramiento Hombros', 
    descripcion: 'Cruzar brazo por delante del pecho.', 
    tipo: 'movilidad', 
    imagen: '/images/est_hombros.png', 
    agonistas: 'Deltoides posterior', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_7', 
    nombre: 'Movilidad Cervical', 
    descripcion: 'Rotaciones e inclinaciones laterales suaves.', 
    tipo: 'movilidad', 
    imagen: '/images/movilidad_cuello.png', 
    agonistas: 'ECM/Trapecio', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 2, duracion: '2 min' 
  }
];

export const SESSIONS: Session[] = [
  { 
    id: 1, 
    nombre: "Sesión 1: Estabilidad y Fuerza Base", 
    ejercicios: [
      's1_w_1', 's1_w_2', 's1_w_3', 's1_w_4', 's1_w_5', 's1_w_6',
      's1_r_1', 's1_r_2', 's1_r_3', 's1_r_4', 's1_r_5', 's1_r_6',
      's1_c_1', 's1_c_2', 's1_c_3', 's1_c_4', 's1_c_5', 's1_c_6', 's1_c_7'
    ] 
  }
];
