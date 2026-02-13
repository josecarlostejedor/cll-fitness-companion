
import { Exercise, Session } from '../types';

export const EXERCISES: Exercise[] = [
  // --- CALENTAMIENTO (6 Tareas completas según solicitud) ---
  { 
    id: 's1_w_1', 
    nombre: 'Caminar círculos + movilidad', 
    descripcion: 'Rápido, paso largo, círculos hombros, rodillas, puntillas, lateral trote.', 
    tipo: 'aeróbico', 
    imagen: '/images/caminar_movilidad.jpg', 
    agonistas: 'General', sinergistas: '-', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '2 min' 
  },
  { 
    id: 's1_w_2', 
    nombre: 'Equilibrio 1 pierna', 
    descripcion: 'Mantener el equilibrio sobre un solo pie sin apoyos externos.', 
    tipo: 'movilidad', 
    imagen: '/images/equilibrio.jpg', 
    agonistas: 'Glúteo medio', sinergistas: '-', estabilizadores: 'Tobillo', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '2 min' 
  },
  { 
    id: 's1_w_3', 
    nombre: 'Flexiones pared/suelo', 
    descripcion: 'Empuje de brazos contra pared o suelo según nivel de condición física.', 
    tipo: 'autocarga', 
    imagen: '/images/flexiones.jpg', 
    agonistas: 'Pectoral', sinergistas: 'Tríceps', estabilizadores: 'Serrato', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '1 min' 
  },
  { 
    id: 's1_w_4', 
    nombre: 'Sentadilla pared', 
    descripcion: 'Isometría apoyado en la pared manteniendo rodillas a 90 grados.', 
    tipo: 'autocarga', 
    imagen: '/images/sentadilla_pared.jpg', 
    agonistas: 'Cuádriceps', sinergistas: '-', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '1 min' 
  },
  { 
    id: 's1_w_5', 
    nombre: 'Saltar', 
    descripcion: 'Saltos suaves y controlados sobre las puntas de los pies.', 
    tipo: 'pliométrico', 
    imagen: '/images/saltar.jpg', 
    agonistas: 'Gemelos', sinergistas: 'Cuádriceps', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '2 min' 
  },
  { 
    id: 's1_w_6', 
    nombre: 'Lanzamientos pelota', 
    descripcion: 'Lanzar y recibir una pelota contra la pared para activar el tren superior.', 
    tipo: 'movilidad', 
    imagen: '/images/lanzamientos.jpg', 
    agonistas: 'Hombros', sinergistas: 'Bíceps', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Calentamiento', rpe_recomendado: 6, duracion: '2 min' 
  },

  // --- ENTRENAMIENTO DE RESISTENCIA (6 Tareas) ---
  { 
    id: 's1_r_1', 
    nombre: 'Sentadilla peso corporal', 
    descripcion: 'Flexión de cadera y rodillas con control motor excéntrico.', 
    tipo: 'autocarga', 
    imagen: '/images/sentadilla_libre.jpg', 
    agonistas: 'Cuádriceps', sinergistas: 'Glúteo', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },
  { 
    id: 's1_r_2', 
    nombre: 'Peso muerto rumano', 
    descripcion: 'Bisagra de cadera manteniendo la espalda neutra y carga pegada a las piernas.', 
    tipo: 'sobrecarga', 
    imagen: '/images/peso_muerto.jpg', 
    agonistas: 'Isquiotibiales', sinergistas: 'Glúteo mayor', estabilizadores: 'Erectores', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },
  { 
    id: 's1_r_3', 
    nombre: 'Plancha Isométrica', 
    descripcion: 'Mantener el cuerpo alineado apoyado sobre los antebrazos.', 
    tipo: 'autocarga', 
    imagen: '/images/plancha.jpg', 
    agonistas: 'Abdomen', sinergistas: '-', estabilizadores: 'Hombros', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: '30s' 
  },
  { 
    id: 's1_r_4', 
    nombre: 'Press banca barra', 
    descripcion: 'Empuje horizontal desde el pecho con barra olímpica.', 
    tipo: 'barra olímpica', 
    imagen: '/images/press_banca.jpg', 
    agonistas: 'Pectoral mayor', sinergistas: 'Tríceps', estabilizadores: 'Deltoides', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },
  { 
    id: 's1_r_5', 
    nombre: 'Curl bíceps + flex hombro', 
    descripcion: 'Flexión de codos seguida de una elevación frontal controlada.', 
    tipo: 'mancuernas', 
    imagen: '/images/curl_hombro.jpg', 
    agonistas: 'Bíceps/Deltoides anterior', sinergistas: '-', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },
  { 
    id: 's1_r_6', 
    nombre: 'Remo mancuernas', 
    descripcion: 'Tracción bilateral de mancuernas hacia la cadera en posición inclinada.', 
    tipo: 'mancuernas', 
    imagen: '/images/remo.jpg', 
    agonistas: 'Dorsal ancho', sinergistas: 'Bíceps', estabilizadores: 'Core', 
    parte_de_la_sesion: 'Entrenamiento de Resistencia', rpe_recomendado: 7, series: 3, repeticiones: 12 
  },

  // --- ENFRIARSE (7 Tareas) ---
  { 
    id: 's1_c_1', 
    nombre: 'Caminata + respiración', 
    descripcion: 'Paseo muy suave coordinando la inhalación y exhalación profunda.', 
    tipo: 'aeróbico', 
    imagen: '/images/caminata_suave.jpg', 
    agonistas: 'Diafragma', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '3 min' 
  },
  { 
    id: 's1_c_2', 
    nombre: 'Estiramiento cuádriceps', 
    descripcion: 'Llevar el talón al glúteo manteniendo la alineación de la cadera.', 
    tipo: 'movilidad', 
    imagen: '/images/est_cuadriceps.jpg', 
    agonistas: 'Cuádriceps', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_3', 
    nombre: 'Estiramiento isquios', 
    descripcion: 'Pierna extendida al frente con el talón apoyado, inclinando el tronco suavemente.', 
    tipo: 'movilidad', 
    imagen: '/images/est_isquios.jpg', 
    agonistas: 'Isquiotibiales', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_4', 
    nombre: 'Estiramiento pantorrilla', 
    descripcion: 'Apoyo en pared estirando la pantorrilla con la rodilla extendida.', 
    tipo: 'movilidad', 
    imagen: '/images/est_gemelos.jpg', 
    agonistas: 'Gemelos', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_5', 
    nombre: 'Estiramiento bíceps', 
    descripcion: 'Extensión de brazo con palma hacia afuera contra un soporte.', 
    tipo: 'movilidad', 
    imagen: '/images/est_biceps.jpg', 
    agonistas: 'Bíceps', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_6', 
    nombre: 'Estiramiento hombros', 
    descripcion: 'Cruzar el brazo por delante del pecho ejerciendo una ligera presión.', 
    tipo: 'movilidad', 
    imagen: '/images/est_hombros.jpg', 
    agonistas: 'Deltoides posterior', sinergistas: '-', estabilizadores: '-', 
    parte_de_la_sesion: 'Enfriamiento', rpe_recomendado: 3, duracion: '1 min' 
  },
  { 
    id: 's1_c_7', 
    nombre: 'Movilidad cervical', 
    descripcion: 'Movimientos lentos y controlados de rotación e inclinación lateral.', 
    tipo: 'movilidad', 
    imagen: '/images/movilidad_cuello.jpg', 
    agonistas: 'ECM/Trapecio', sinergistas: '-', estabilizadores: '-', 
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
