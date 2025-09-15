import { Outlet, Link } from "react-router-dom";

export default function Layout() {
  return (
    <div className="relative">
      {/* Botón siempre visible: fixed en top-right, ajusta estilos si necesitas */}
      <Link to="/">
        <button className="fixed top-4 right-4 bg-green-500 text-white p-2 rounded shadow-lg z-50">
          Menú principal
        </button>
      </Link>
      {/* Contenido de la página secundaria */}
      <Outlet />
    </div>
  );
}