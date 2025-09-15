import { useState } from "react";
import DistributionChart from "../../components/DistributionChart";
import Swal from 'sweetalert2';
import 'katex/dist/katex.min.css';
import { BlockMath } from 'react-katex';
import Header from "../../components/Header";


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
    <div className="flex flex-col items-center min-h-screen bg-gray-50 p-10">
      <Header 
        distributionName={"Bernoulli"}
        formula={"f(x) = \\theta^x \\, (1-\\theta)^{1-x}, \\quad x = 0,1"}  
      />

      <div className="w-[95vw] h-[95vh] bg-white shadow-lg rounded-lg p-6 grid grid-cols-3 gap-4">
        {/* Panel izquierdo (2 filas: inputs y botones) */}
        <div className="col-span-1 flex flex-col gap-6">
          {/* Panel 1: Inputs */}
          <div className="bg-gray-100 p-4 rounded shadow">
            <h2 className="text-xl font-bold text-gray-700 mb-4">
              Parámetros
            </h2>
            <div className="mb-4">
              <label className="block text-gray-700 mb-1">
                Número de Repeticiones:
              </label>
              <input
                type="number"
                value={repeticiones}
                onChange={(e) => setRepeticiones(Number(e.target.value))}
                className="border p-2 rounded w-full"
              />
            </div>
            <div>
              <label className="block text-gray-700 mb-1">
                Probabilidad de Éxito:
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="1"
                value={proba_exito}
                onChange={(e) => setProba_exito(Number(e.target.value))}
                className="border p-2 rounded w-full mb-5"
              />
            </div>
            <button
              onClick={fetchData}
              className="w-full bg-blue-500 text-xl text-white p-4 rounded mb-3 hover:bg-blue-600"
            >
              Generar
            </button>
          </div>

          {/* Panel 2: Botones */}
          <div className="bg-gray-100 p-4 rounded shadow flex flex-col gap-4">
            
            {data && (
              <button
                onClick={() =>
                  Swal.fire({
                    title: "Secuencia Bernoulli",
                    text: data.secuencia.join(", "),
                    icon: "info",
                    width: "60%",
                  })
                }
                className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
              >
                Ver muestra
              </button>
            )}
          </div>
        </div>

        {/* Panel derecho: Gráfica */}
        <div className="flex col-span-2 bg-gray-100 p-4 rounded shadow justify-center items-center">
          {data ? (
            <DistributionChart type="bernoulli" data={data} />
          ) : (
            <p className="text-xl text-gray-500">Genera la simulación para ver la gráfica...</p>
          )}
        </div>
      </div>
    </div>
  );
}