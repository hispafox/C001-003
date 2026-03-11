// ──────────────────────────────────────────────
// Cliente HTTP centralizado para llamadas a la API.
// Usa el proxy de Vite → las peticiones van a /api/*
// y Vite las reenvía a https://localhost:7001.
// ──────────────────────────────────────────────

const BASE_URL = "/api";

/**
 * Wrapper de fetch que:
 * 1. Prefija la URL con /api
 * 2. Parsea la respuesta como JSON
 * 3. Lanza error si la respuesta no es ok
 */
async function fetchJson<T>(endpoint: string): Promise<T> {
  const response = await fetch(`${BASE_URL}${endpoint}`);

  if (!response.ok) {
    throw new Error(`Error ${response.status}: ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}

export default fetchJson;
