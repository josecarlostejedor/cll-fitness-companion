
import { Exercise, Session } from '../types';

export const EXERCISES: Exercise[] = [
  // --- CALENTAMIENTO (6 Tareas) ---
  { 
    id: 's1_w_1', 
    nombre: 'Caminar círculos + movilidad', 
    descripcion: 'Rápido, paso largo, círculos hombros, rodillas, puntillas, lateral trote.', 
    tipo: 'aeróbico', 
    imagen: '/images/marcha_movilidad.png', 
    agonistas: 'General', sinergistas: '-', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '2 min' 
  },
  { 
    id: 's1_w_2', 
    nombre: 'Equilibrio 1 pierna', 
    descripcion: 'Mantener el equilibrio sobre un solo pie sin apoyos.', 
    tipo: 'movilidad', 
    imagen: '/images/equilibrio.png', 
    agonistas: 'Glúteo medio', sinergistas: '-', estabilizadores: 'Tobillo', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '2 min' 
  },
  { 
    id: 's1_w_3', 
    nombre: 'Flexiones pared/suelo', 
    descripcion: 'Empuje de brazos contra pared o suelo.', 
    tipo: 'autocarga', 
    imagen: '/images/flexiones_pared.png', 
    agonistas: 'Pectoral', sinergistas: 'Tríceps', estabilizadores: 'Serrato', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '1 min' 
  },
  { 
    id: 's1_w_4', 
    nombre: 'Sentadilla pared', 
    descripcion: 'Isometría apoyado en la pared (silla imaginaria).', 
    tipo: 'autocarga', 
    imagen: '/images/sentadilla_pared.png', 
    agonistas: 'Cuádriceps', sinergistas: '-', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '1 min' 
  },
  { 
    id: 's1_w_5', 
    nombre: 'Saltar', 
    descripcion: 'Saltos suaves sobre la punta de los pies.', 
    tipo: 'pliométrico', 
    imagen: '/images/saltos.png', 
    agonistas: 'Gemelos', sinergistas: 'Cuádriceps', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '2 min' 
  },
  { 
    id: 's1_w_6', 
    nombre: 'Lanzamientos pelota', 
    descripcion: 'Lanzar y recibir una pelota contra la pared.', 
    tipo: 'movilidad', 
    imagen: '/images/lanzamientos.png', 
    agonistas: 'Hombros', sinergistas: 'Bíceps', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '2 min' 
  },

  // --- ENTRENAMIENTO DE RESISTENCIA (6 Tareas - 3x12 al 70%) ---
  { 
    id: 's1_r_1', 
    nombre: 'Sentadilla peso corporal', 
    descripcion: 'Sentadilla clásica controlando la bajada.', 
    tipo: 'autocarga', 
    imagen: '/images/sentadilla_libre.png', 
    agonistas: 'Cuádriceps', sinergistas: 'Glúteo', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },
  { 
    id: 's1_r_2', 
    nombre: 'Peso muerto rumano', 
    descripcion: 'Bisagra de cadera con carga controlada.', 
    tipo: 'sobrecarga', 
    imagen: '/images/peso_muerto.png', 
    agonistas: 'Isquiotibiales', sinergistas: 'Glúteo mayor', estabilizadores: 'Erectores', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },
  { 
    id: 's1_r_3', 
    nombre: 'Plancha Isométrica', 
    descripcion: 'Mantener posición rígida sobre antebrazos.', 
    tipo: 'autocarga', 
    imagen: '/images/plancha.png', 
    agonistas: 'Abdomen', sinergistas: '-', estabilizadores: 'Hombros', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: '30s' 
  },
  { 
    id: 's1_r_4', 
    nombre: 'Press banca barra', 
    descripcion: 'Empuje horizontal con barra desde el pecho.', 
    tipo: 'barra olímpica', 
    imagen: '/images/press_banca.png', 
    agonistas: 'Pectoral mayor', sinergistas: 'Tríceps', estabilizadores: 'Deltoides', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },
  { 
    id: 's1_r_5', 
    nombre: 'Curl bíceps + flex hombro', 
    descripcion: 'Flexión de codo y elevación frontal de brazo.', 
    tipo: 'mancuernas', 
    imagen: '/images/curl_hombro.png', 
    agonistas: 'Bíceps/Hombro', sinergistas: '-', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },
  { 
    id: 's1_r_6', 
    nombre: 'Remo mancuernas', 
    descripcion: 'Tracción de peso hacia la cadera inclinado.', 
    tipo: 'mancuernas', 
    imagen: '/images/remo.png', 
    agonistas: 'Dorsal', sinergistas: 'Bíceps', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },

  // --- ENFRIARSE (7 Tareas) ---
  { 
    id: 's1_c_1', 
    nombre: 'Caminata + respiración', 
    descripcion: 'Paseo muy suave coordinando la respiración.', 
    tipo: 'aeróbico', 
    imagen: '/images/caminata_suave.png', 
    agonistas: 'Diafragma', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '3 min' 
  },
  { 
    id: 's1_c_2', 
    nombre: 'Estiramiento cuádriceps', 
    descripcion: 'Talón al glúteo manteniendo rodillas juntas.', 
    tipo: 'movilidad', 
    imagen: '/images/est_cuadriceps.png', 
    agonistas: 'Cuádriceps', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_3', 
    nombre: 'Estiramiento isquios', 
    descripcion: 'Pierna extendida al frente buscando el pie.', 
    tipo: 'movilidad', 
    imagen: '/images/est_isquios.png', 
    agonistas: 'Isquiotibiales', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_4', 
    nombre: 'Estiramiento pantorrilla', 
    descripcion: 'Apoyo en pared estirando el gemelo.', 
    tipo: 'movilidad', 
    imagen: '/images/est_gemelos.png', 
    agonistas: 'Gemelos', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_5', 
    nombre: 'Estiramiento bíceps', 
    descripcion: 'Extensión de brazo contra marco de puerta.', 
    tipo: 'movilidad', 
    imagen: '/images/est_biceps.png', 
    agonistas: 'Bíceps', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_6', 
    nombre: 'Estiramiento hombros', 
    descripcion: 'Cruzar brazo por delante del pecho.', 
    tipo: 'movilidad', 
    imagen: '/images/est_hombros.png', 
    agonistas: 'Deltoides', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_7', 
    nombre: 'Movilidad cervical', 
    descripcion: 'Rotaciones lentas de cuello a ambos lados.', 
    tipo: 'movilidad', 
    imagen: '/images/cuello.png', 
    agonistas: 'Trapecio', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 2, duracion: '2 min' 
  }
];

export const SESSIONS: Session[] = [
  { 
    id: 1, 
    nombre: "Sesión 1: Estabilidad Base", 
    ejercicios: [
      's1_w_1', 's1_w_2', 's1_w_3', 's1_w_4', 's1_w_5', 's1_w_6',
      's1_r_1', 's1_r_2', 's1_r_3', 's1_r_4', 's1_r_5', 's1_r_6',
      's1_c_1', 's1_c_2', 's1_c_3', 's1_c_4', 's1_c_5', 's1_c_6', 's1_c_7'
    ] 
  }
];
