// ──────────────────────────────────────────────
// Interfaces TypeScript que reflejan los DTOs
// que devuelve la API .NET en cada endpoint GET.
// ──────────────────────────────────────────────

// ─── HATEOAS ─────────────────────────────────
/** Enlace HATEOAS que acompaña a algunos recursos. */
export interface LinkDto {
  href: string;
  rel: string;
  method: string;
}

// ─── PRODUCTOS ───────────────────────────────
/** Lo que devuelve GET /api/products (cada elemento). */
export interface ProductoResumen {
  id: number;
  name: string;
  description: string | null;
  price: number;
  stock: number;
  clienteId: number;
  clienteNombre: string;
  links: LinkDto[];
}

// ─── CATEGORÍAS ──────────────────────────────
/** Lo que devuelve GET /api/categories (cada elemento).
 *  ⚠️ La API solo devuelve el nombre en el listado. */
export interface CategoriaResumen {
  name: string;
}

/** Resumen extendido (GET /api/categories/{id} → se lista en el futuro). */
export interface CategoriaSummary {
  id: number;
  name: string;
  isActive: boolean;
  productsCount: number;
}

/** Producto anidado dentro del detalle de categoría. */
export interface ProductoEnCategoria {
  id: number;
  name: string;
  price: number;
}

/** Detalle completo de una categoría (GET /api/categories/{id}). */
export interface CategoriaDetalle {
  id: number;
  name: string;
  description: string | null;
  isActive: boolean;
  products: ProductoEnCategoria[];
}

// ─── CLIENTES ────────────────────────────────
/** Lo que devuelve GET /api/clientes (cada elemento). */
export interface ClienteResumen {
  id: number;
  nombre: string;
  apellidos: string;
  email: string;
  telefono: string | null;
  activo: boolean;
  fechaAlta: string; // ISO date string
  productosCount: number;
}

/** Producto anidado dentro del detalle de un cliente. */
export interface ClienteProducto {
  id: number;
  name: string;
  price: number;
  categoryName: string;
}

/** Detalle completo de un cliente (GET /api/clientes/{id}). */
export interface ClienteDetalle {
  id: number;
  nombre: string;
  apellidos: string;
  email: string;
  telefono: string | null;
  direccion: string | null;
  fechaAlta: string;
  activo: boolean;
  productos: ClienteProducto[];
}
