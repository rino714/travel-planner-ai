export interface Spot {
  id: number;
  name: string;
  address: string | null;
  lat: number;
  lng: number;
  created_at: string;
}

export interface SpotCreate {
  name: string;
  address?: string;
  lat: number;
  lng: number;
}

export interface TripCreate {
  spot_ids: number[];
  start_date: string;
  days: number;
}

export interface ScheduleItem {
  time: string;
  type: "spot" | "move" | "accommodation";
  name: string;
  duration_min: number | null;
  from?: string;
  to?: string;
}

export interface DaySchedule {
  day: number;
  date: string;
  items: ScheduleItem[];
}

export interface Trip {
  id: number;
  start_date: string;
  days: number;
  schedule: DaySchedule[];
  created_at: string;
}
