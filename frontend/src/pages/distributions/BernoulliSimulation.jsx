import { useState } from "react";
import DistributionChart from "../DistributionChart";
import Swal from 'sweetalert2';
import 'katex/dist/katex.min.css';
import { BlockMath } from 'react-katex';


export default function BernoulliSimulation() {
  const [repeticiones, setRepeticiones] = useState(100);
  const [proba_exito, setProba_exito] = useState(0.5);
  const [data, setData] = useState(null);

  const fetchData = async () => {
    const res = await fetch(`http://localhost:8000/bernoulli?repeticiones=${repeticiones}&proba_exito=${proba_exito}`);
    const json = await res.json();
    setData(json);
  };

  return (
    <div className="flex flex-col  items-center min-h-screen bg-gray-50 p-10">
      <div className="w-[90vw] h-[90vh] bg-white shadow-lg rounded-lg p-8">
        <h1 className="text-4xl font-extrabold text-gray-800 mb-6 text-center">Simulación de Distribución Bernoulli</h1>
        <BlockMath math="f(x) = " />

        <div className="flex flex-row items-center justify-center gap-6">
          <div className="flex flex-col gap-4">
            <div>
              <label className="block text-xl text-gray-700 mb-1">Número de Repeticiones:</label>
              <input 
                type="number"
                value={repeticiones}
                onChange={(e) => setRepeticiones(Number(e.target.value))}
                className="border p-2 rounded w-full"
              />
            </div>
            <div>
              <label className="block text-xl text-gray-700 mb-1">Probabilidad de Éxito:</label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="1"
                value={proba_exito}
                onChange={(e) => setProba_exito(Number(e.target.value))}
                className="border p-2 rounded w-full"
              />
            </div>
          </div>
          <button
            onClick={fetchData}
            className="bg-blue-500 text-white px-6 py-3 rounded self-center hover:bg-blue-600"
          >
            Generar
          </button>
        </div>

        {data && (
          <div className="mt-8 flex flex-col items-center">
            <DistributionChart type="bernoulli" data={data} />
            <button
              onClick={() => Swal.fire({
                title: 'Secuencia Bernoulli',
                text: data.secuencia.join(", "),
                icon: 'success'
              })}
              className="bg-green-500 text-white px-4 py-2 rounded mt-4 hover:bg-green-600"
            >
              Ver secuencia
            </button>  
          </div>
        )}
      </div>
    </div>
  );
}