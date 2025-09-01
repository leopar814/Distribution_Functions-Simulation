import { Link } from "react-router-dom";

export default function MainMenu() {
  return (
    <div className="flex flex-col items-center p-6 gap-4">
      <h1 className="text-2xl font-bold mb-4">Simulación de Distribuciones</h1>
      <div className="flex flex-col gap-4">
        <Link to="/bernoulli">
          <button className="bg-blue-500 text-white p-4 rounded w-64">Bernoulli</button>
        </Link>
        <Link to="/binomial">
          <button className="bg-blue-500 text-white p-4 rounded w-64">Binomial</button>
        </Link>
        {/* Más botones para otras distribuciones */}
      </div>
    </div>
  );
}