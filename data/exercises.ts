
import { Exercise, Session } from '../types';

export const EXERCISES: Exercise[] = [
  // --- CALENTAMIENTO (Sesión 1) ---
  { 
    id: 's1_w_1', 
    nombre: '2 min caminar círculos + movilidad', 
    descripcion: 'Rápido, paso largo, círculos hombros, rodillas, puntillas, lateral trote.', 
    tipo: 'aeróbico', 
    imagen: '/images/marcha_movilidad.png', 
    agonistas: 'General', sinergistas: '-', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '2 min' 
  },
  { 
    id: 's1_w_2', 
    nombre: '2 min equilibrio 1 pierna', 
    descripcion: 'Mantener el equilibrio sobre una sola pierna (unipodal).', 
    tipo: 'movilidad', 
    imagen: '/images/equilibrio_unipodal.png', 
    agonistas: 'Glúteo medio', sinergistas: '-', estabilizadores: 'Tobillo', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '2 min' 
  },
  { 
    id: 's1_w_3', 
    nombre: '1 min flexiones pared/suelo', 
    descripcion: 'Empuje de brazos contra superficie vertical o inclinada.', 
    tipo: 'autocarga', 
    imagen: '/images/flexiones.png', 
    agonistas: 'Pectoral', sinergistas: 'Tríceps', estabilizadores: 'Serrato', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '1 min' 
  },
  { 
    id: 's1_w_4', 
    nombre: '1 min sentadilla pared', 
    descripcion: 'Isometría contra la pared manteniendo ángulos de 90 grados.', 
    tipo: 'autocarga', 
    imagen: '/images/isometria_pared.png', 
    agonistas: 'Cuádriceps', sinergistas: '-', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '1 min' 
  },
  { 
    id: 's1_w_5', 
    nombre: '2 min saltar', 
    descripcion: 'Saltos controlados sobre las puntas de los pies.', 
    tipo: 'pliométrico', 
    imagen: '/images/saltos.png', 
    agonistas: 'Gemelos', sinergistas: 'Cuádriceps', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '2 min' 
  },
  { 
    id: 's1_w_6', 
    nombre: '2 min lanzamientos pelota', 
    descripcion: 'Lanzar y recibir balón contra pared para activar tren superior.', 
    tipo: 'movilidad', 
    imagen: '/images/lanzamientos.png', 
    agonistas: 'Hombros', sinergistas: 'Bíceps', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '2 min' 
  },

  // --- ENTRENAMIENTO DE RESISTENCIA (Sesión 1) ---
  { 
    id: 's1_r_1', 
    nombre: 'Sentadilla peso corporal', 
    descripcion: 'Flexión de cadera y rodillas manteniendo espalda neutra.', 
    tipo: 'autocarga', 
    imagen: '/images/sentadilla_libre.png', 
    agonistas: 'Cuádriceps', sinergistas: 'Glúteo mayor', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },
  { 
    id: 's1_r_2', 
    nombre: 'Peso muerto rumano', 
    descripcion: 'Bisagra de cadera bajando carga por debajo de rodillas.', 
    tipo: 'sobrecarga', 
    imagen: '/images/peso_muerto_rumano.png', 
    agonistas: 'Isquiotibiales', sinergistas: 'Glúteo', estabilizadores: 'Lumbar', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },
  { 
    id: 's1_r_3', 
    nombre: 'Plancha 3x30s', 
    descripcion: 'Estabilización del core sobre antebrazos.', 
    tipo: 'autocarga', 
    imagen: '/images/plancha.png', 
    agonistas: 'Recto abdominal', sinergistas: 'Oblicuos', estabilizadores: 'Hombros', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: '30s' 
  },
  { 
    id: 's1_r_4', 
    nombre: 'Press banca barra', 
    descripcion: 'Empuje horizontal en banco plano.', 
    tipo: 'barra olímpica', 
    imagen: '/images/press_banca.png', 
    agonistas: 'Pectoral mayor', sinergistas: 'Tríceps', estabilizadores: 'Deltoides', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },
  { 
    id: 's1_r_5', 
    nombre: 'Curl bíceps + flex hombro', 
    descripcion: 'Flexión de codo y elevación de brazo frontal.', 
    tipo: 'mancuernas', 
    imagen: '/images/curl_hombro.png', 
    agonistas: 'Bíceps/Deltoides ant.', sinergistas: '-', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },
  { 
    id: 's1_r_6', 
    nombre: 'Remo mancuernas', 
    descripcion: 'Tracción de mancuernas hacia la cadera en posición inclinada.', 
    tipo: 'mancuernas', 
    imagen: '/images/remo_mancuernas.png', 
    agonistas: 'Dorsal ancho', sinergistas: 'Bíceps', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },

  // --- ENFRIARSE (Sesión 1) ---
  { 
    id: 's1_c_1', 
    nombre: '3 min caminata + respiración', 
    descripcion: 'Paseo muy suave coordinando aire.', 
    tipo: 'aeróbico', 
    imagen: '/images/caminata_suave.png', 
    agonistas: 'Diafragma', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '3 min' 
  },
  { 
    id: 's1_c_2', 
    nombre: '1 min cuádriceps', 
    descripcion: 'Estiramiento anterior del muslo.', 
    tipo: 'movilidad', 
    imagen: '/images/est_cuadriceps.png', 
    agonistas: 'Cuádriceps', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_3', 
    nombre: '1 min isquios', 
    descripcion: 'Estiramiento posterior del muslo.', 
    tipo: 'movilidad', 
    imagen: '/images/est_isquios.png', 
    agonistas: 'Isquiotibiales', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_4', 
    nombre: '1 min pantorrilla', 
    descripcion: 'Estiramiento de gemelos.', 
    tipo: 'movilidad', 
    imagen: '/images/est_gemelos.png', 
    agonistas: 'Gemelos', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_5', 
    nombre: '1 min bíceps', 
    descripcion: 'Estiramiento de la cara anterior del brazo.', 
    tipo: 'movilidad', 
    imagen: '/images/est_biceps.png', 
    agonistas: 'Bíceps', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_6', 
    nombre: '1 min hombros', 
    descripcion: 'Estiramiento cruzado de deltoides.', 
    tipo: 'movilidad', 
    imagen: '/images/est_hombros.png', 
    agonistas: 'Hombros', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_7', 
    nombre: '2 min movilidad cervical', 
    descripcion: 'Rotaciones lentas de cuello.', 
    tipo: 'movilidad', 
    imagen: '/images/movilidad_cuello.png', 
    agonistas: 'Cuello', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 2, duracion: '2 min' 
  }
];

export const SESSIONS: Session[] = [
  { 
    id: 1, 
    nombre: "Sesión 1: Base de Fuerza (Protocolo ACSM)", 
    ejercicios: [
      's1_w_1', 's1_w_2', 's1_w_3', 's1_w_4', 's1_w_5', 's1_w_6',
      's1_r_1', 's1_r_2', 's1_r_3', 's1_r_4', 's1_r_5', 's1_r_6',
      's1_c_1', 's1_c_2', 's1_c_3', 's1_c_4', 's1_c_5', 's1_c_6', 's1_c_7'
    ] 
  }
];
