import { useEffect, useState } from "react";
import { getCategorias } from "../services/categoriasService";
import type { CategoriaResumen } from "../types/models";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";

/** Página de listado de categorías (solo activas por defecto). */
export default function CategoriasPage() {
  const [categorias, setCategorias] = useState<CategoriaResumen[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getCategorias(true) // solo activas
      .then(setCategorias)
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Loading />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <section>
      <h1>Categorías</h1>

      {categorias.length === 0 ? (
        <p>No hay categorías registradas.</p>
      ) : (
        <ul className="card-list">
          {categorias.map((c, index) => (
            <li key={index} className="card">
              {c.name}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
