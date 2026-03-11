import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "./layout/MainLayout";
import HomePage from "./pages/HomePage";
import ProductosPage from "./pages/ProductosPage";
import CategoriasPage from "./pages/CategoriasPage";
import ClientesPage from "./pages/ClientesPage";

/**
 * Componente raíz de la aplicación.
 * Define el enrutamiento con React Router v6.
 */
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Todas las rutas comparten el layout principal */}
        <Route element={<MainLayout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/productos" element={<ProductosPage />} />
          <Route path="/categorias" element={<CategoriasPage />} />
          <Route path="/clientes" element={<ClientesPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
