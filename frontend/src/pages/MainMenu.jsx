import { Link } from "react-router-dom";

export default function MainMenu() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-6">
      <div className="bg-white items-center shadow-lg rounded-2xl p-15 text-center">
        <h1 className="text-5xl font-extrabold text-gray-800 mb-15">
          Simulación de Distribuciones
        </h1>
        <div className="flex flex-col gap-4">
          <Link to="/bernoulli">
            <button className="w-[20vw] bg-blue-300 hover:bg-blue-600 text-black text-xl font-semibold py-3 rounded-xl shadow-md transition duration-300">
              Bernoulli
            </button>
          </Link>
          <Link to="/binomial">
            <button className="w-[20vw] bg-green-300 hover:bg-green-600 text-black text-xl font-semibold py-3 rounded-xl shadow-md transition duration-300">
              Binomial
            </button>
          </Link>
          {/* Más botones para otras distribuciones */}
          <Link to="/exponential">
            <button className="w-[20vw] bg-purple-300 hover:bg-purple-600 text-black text-xl font-semibold py-3 rounded-xl shadow-md transition duration-300">
              Exponencial
            </button>
          </Link>
          <Link to="/normal">
            <button className="w-[20vw] bg-pink-300 hover:bg-pink-600 text-black text-xl font-semibold py-3 rounded-xl shadow-md transition duration-300">
              Normal
            </button>
          </Link>
          <Link to="/multinomial">
            <button className="w-[20vw] bg-red-300 hover:bg-red-500 text-black text-xl font-semibold py-3 rounded-xl shadow-md transition duration-300">
              Multinomial
            </button>
          </Link>
          <Link to="/gebbs">
            <button className="w-[20vw] bg-orange-300 hover:bg-orange-500 text-black text-xl font-semibold py-3 rounded-xl shadow-md transition duration-300">
              Gebbs
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}
