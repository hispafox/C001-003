import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";

/**
 * Layout principal: Navbar arriba + contenido dinámico (<Outlet />).
 * Todas las rutas hijas se renderizan dentro de <main>.
 */
export default function MainLayout() {
  return (
    <>
      <Navbar />
      <main className="container">
        <Outlet />
      </main>
    </>
  );
}
