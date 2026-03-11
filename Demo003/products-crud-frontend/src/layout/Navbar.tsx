import { Link } from "react-router-dom";

/** Barra de navegación superior compartida por todas las páginas. */
export default function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        🛒 Products CRUD
      </Link>

      <ul className="navbar-links">
        <li>
          <Link to="/productos">Productos</Link>
        </li>
        <li>
          <Link to="/categorias">Categorías</Link>
        </li>
        <li>
          <Link to="/clientes">Clientes</Link>
        </li>
      </ul>
    </nav>
  );
}
