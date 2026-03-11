import fetchJson from "./api";
import type { ProductoResumen } from "../types/models";

/** Obtiene todos los productos (GET /api/products). */
export function getProductos(): Promise<ProductoResumen[]> {
  return fetchJson<ProductoResumen[]>("/products");
}
