
export type ExerciseCategory = 'autocarga' | 'sobrecarga' | 'mancuernas' | 'barra olímpica' | 'pliométrico' | 'movilidad' | 'aeróbico';
export type SessionPhase = 'Calentamiento' | 'Entrenamiento de Resistencia' | 'Enfriamiento';

export interface UserProfile {
  nombre: string;
  apellidos: string;
  sexo: string;
  edad: string;
}

export interface Exercise {
  id: string;
  nombre: string;
  descripcion: string;
  tipo: ExerciseCategory;
  imagen: string;
  agonistas: string;
  sinergistas: string;
  estabilizadores: string;
  parte_de_la_sesion: SessionPhase;
  rpe_recomendado: number;
  duracion?: string;
  series?: number;
  repeticiones?: string | number;
}

export interface Session {
  id: number;
  nombre: string;
  ejercicios: string[];
}

export interface UserStats {
  profile: UserProfile;
  rms: Record<string, number>;
  history: Record<string, { sessionsCompleted: number, currentWeight: number }>;
}
