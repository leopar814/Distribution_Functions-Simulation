import { Outlet, Link } from "react-router-dom";

export default function Layout() {
  return (
    <div className="relative">
      {/* Botón siempre visible: fixed en top-right, ajusta estilos si necesitas */}
      <Link to="/">
        <button className="fixed top-4 left-4 text-xl text-green-700 p-3 border-1 rounded shadow-lg z-50 hover:bg-green-100">
          Menú principal
        </button>
      </Link>
      {/* Contenido de la página secundaria */}
      <Outlet />
    </div>
  );
}