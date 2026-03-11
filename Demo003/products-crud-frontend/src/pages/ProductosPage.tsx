import { useEffect, useState } from "react";
import { getProductos } from "../services/productosService";
import type { ProductoResumen } from "../types/models";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";

/** Página de listado de productos. */
export default function ProductosPage() {
  // Estado: lista de productos, cargando, error
  const [productos, setProductos] = useState<ProductoResumen[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Llamar a la API al montar el componente
  useEffect(() => {
    getProductos()
      .then(setProductos)
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Loading />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <section>
      <h1>Productos</h1>

      {productos.length === 0 ? (
        <p>No hay productos registrados.</p>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Precio</th>
              <th>Stock</th>
              <th>Cliente</th>
            </tr>
          </thead>
          <tbody>
            {productos.map((p) => (
              <tr key={p.id}>
                <td>{p.id}</td>
                <td>{p.name}</td>
                <td>${p.price.toFixed(2)}</td>
                <td>{p.stock}</td>
                <td>{p.clienteNombre}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
