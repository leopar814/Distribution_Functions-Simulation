import { Outlet, Link } from "react-router-dom";

export default function Layout() {
  return (
    <div className="relative">
      {/* Botón siempre visible: fixed en top-right, ajusta estilos si necesitas */}
      <Link to="/">
        <button className="fixed bottom-4 left-4 text-xl bg-green-600 text-white p-3 rounded shadow-lg z-50 hover:bg-green-500 hover:text-black">
          Menú principal
        </button>
      </Link>
      {/* Contenido de la página secundaria */}
      <Outlet />
    </div>
  );
}