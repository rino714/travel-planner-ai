import type { Spot, SpotCreate, Trip, TripCreate } from "@/types";

const API_BASE = "/api";

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `HTTP ${res.status}`);
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  // Spots
  createSpot: (data: SpotCreate) =>
    request<Spot>("/spots", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  listSpots: () => request<Spot[]>("/spots"),

  deleteSpot: (id: number) =>
    request<void>(`/spots/${id}`, { method: "DELETE" }),

  // Trips
  createTrip: (data: TripCreate) =>
    request<Trip>("/trips", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  getTrip: (id: number) => request<Trip>(`/trips/${id}`),
};
