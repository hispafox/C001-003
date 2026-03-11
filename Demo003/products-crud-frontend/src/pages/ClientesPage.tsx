import { useEffect, useState } from "react";
import { getClientes } from "../services/clientesService";
import type { ClienteResumen } from "../types/models";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";

/** Página de listado de clientes (solo activos por defecto). */
export default function ClientesPage() {
  const [clientes, setClientes] = useState<ClienteResumen[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getClientes(true) // solo activos
      .then(setClientes)
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Loading />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <section>
      <h1>Clientes</h1>

      {clientes.length === 0 ? (
        <p>No hay clientes registrados.</p>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Email</th>
              <th>Teléfono</th>
              <th>Productos</th>
              <th>Fecha alta</th>
            </tr>
          </thead>
          <tbody>
            {clientes.map((c) => (
              <tr key={c.id}>
                <td>{c.id}</td>
                <td>
                  {c.nombre} {c.apellidos}
                </td>
                <td>{c.email}</td>
                <td>{c.telefono ?? "—"}</td>
                <td>{c.productosCount}</td>
                <td>{new Date(c.fechaAlta).toLocaleDateString("es-ES")}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
