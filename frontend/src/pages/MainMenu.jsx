import { Link } from "react-router-dom";

export default function MainMenu() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-6">
      <div className="bg-white items-center shadow-lg rounded-2xl p-8 w-full max-w-md text-center">
        <h1 className="text-5xl font-extrabold text-gray-800 mb-6">
          Simulación de Distribuciones
        </h1>
        <div className="flex flex-col gap-4">
          <Link to="/bernoulli">
            <button className="w-full bg-blue-300 hover:bg-blue-600 text-black font-semibold py-3 rounded-xl shadow-md transition duration-300">
              Bernoulli
            </button>
          </Link>
          <Link to="/binomial">
            <button className="w-full bg-green-300 hover:bg-green-600 text-black font-semibold py-3 rounded-xl shadow-md transition duration-300">
              Binomial
            </button>
          </Link>
          {/* Más botones para otras distribuciones */}
          <Link to="/normal">
            <button className="w-full bg-purple-300 hover:bg-purple-600 text-black font-semibold py-3 rounded-xl shadow-md transition duration-300">
              Normal
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}
