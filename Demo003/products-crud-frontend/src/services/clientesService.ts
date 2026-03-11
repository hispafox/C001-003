import fetchJson from "./api";
import type { ClienteResumen } from "../types/models";

/**
 * Obtiene clientes (GET /api/clientes).
 * @param activo  - Filtro opcional por estado activo/inactivo.
 * @param buscar  - Texto de búsqueda (nombre, apellidos, email).
 */
export function getClientes(
  activo?: boolean,
  buscar?: string
): Promise<ClienteResumen[]> {
  const params = new URLSearchParams();
  if (activo !== undefined) params.set("activo", String(activo));
  if (buscar) params.set("buscar", buscar);

  const query = params.toString();
  return fetchJson<ClienteResumen[]>(`/clientes${query ? `?${query}` : ""}`);
}
