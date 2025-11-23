import { Link } from "react-router-dom";
import moneda from "/coin.png";
import monedas from "/multiple_coins.png";
import exponencial from "/decreasing_exponential.png";
import normal from "/normal.png";
import dado from "/dice.png";
import gibbs from "/iteration.png";
import bivariada from "/bivariada.png"
import lda from "/lda.png"
import mH from "/mH.png"


export default function MainMenu() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-6">
      <div className="bg-white items-center shadow-lg rounded-2xl p-15 text-center">
        <h1 className="text-5xl font-extrabold text-gray-800 mb-15">
          Simulación de Distribuciones
        </h1>
        <div className="flex flex-col items-center gap-4">
          <Link to="/bernoulli">
            <button className="flex w-80 items-center justify-center gap-2 bg-green-200 hover:bg-green-400 text-black text-xl font-semibold py-3 rounded-xl shadow-md transition duration-300">
              <img src={moneda} alt="icono bernoulli" className="w-6 h-6" />
              Bernoulli
            </button>
          </Link>
          <Link to="/binomial">
            <button className="flex w-80 items-center justify-center gap-2 bg-blue-200 hover:bg-blue-400 text-black text-xl font-semibold py-3 rounded-xl shadow-md transition duration-300">
              <img src={monedas} alt="icono binomial" className="w-6 h-6" />
              Binomial
            </button>
          </Link>
          <Link to="/multinomial">
            <button className="flex w-80 items-center justify-center gap-2 bg-pink-200 hover:bg-pink-400 text-black text-xl font-semibold py-3 rounded-xl shadow-md transition duration-300">
              <img src={dado} alt="icono multinomial" className="w-6 h-6" />
              Multinomial
            </button>
          </Link>
          <Link to="/exponential">
            <button className="flex w-80 items-center justify-center gap-2 bg-purple-200 hover:bg-purple-400 text-black text-xl font-semibold py-3 rounded-xl shadow-md transition duration-300">
              <img src={exponencial} alt="icono exponencial" className="w-6 h-6" />
              Exponencial
            </button>
          </Link>
          <Link to="/normal">
            <button className="flex w-80 items-center justify-center gap-2 bg-rose-200 hover:bg-rose-400 text-black text-xl font-semibold py-3 rounded-xl shadow-md transition duration-300">
              <img src={normal} alt="icono normal" className="w-6 h-6" />
              Normal
            </button>
          </Link>
          <Link to="/bivariada">
            <button className="flex w-80 items-center justify-center gap-2 bg-red-200 hover:bg-red-400 text-black text-xl font-semibold py-3 rounded-xl shadow-md transition duration-300">
              <img src={bivariada} alt="icono bivariada" className="w-6 h-6" />
              Normal Bivariada
            </button>
          </Link>
          <Link to="/gibbs">
            <button className="flex w-80 items-center justify-center gap-2 bg-orange-200 hover:bg-orange-400 text-black text-xl font-semibold py-3 rounded-xl shadow-md transition duration-300">
              <img src={gibbs} alt="icono gibbs" className="w-6 h-6" />
              Gibbs
            </button>
          </Link>
          <Link to="/lda">
            <button className="flex w-80 items-center justify-center gap-2 bg-amber-200 hover:bg-amber-400 text-black text-xl font-semibold py-3 rounded-xl shadow-md transition duration-300">
              <img src={lda} alt="icono lda" className="w-6 h-6" />
              LDA
            </button>
          </Link>
          <Link to="/mH">
            <button className="flex w-80 items-center justify-center gap-2 bg-yellow-300 hover:bg-yellow-400 text-black text-xl font-semibold py-3 rounded-xl shadow-md transition duration-300">
              <img src={mH} alt="icono metropolis hastings" className="w-6 h-6" />
              Metropolis Hastings
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}
