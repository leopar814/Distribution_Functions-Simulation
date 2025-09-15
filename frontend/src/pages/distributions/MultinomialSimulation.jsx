import { useState } from "react";
import DistributionChart from "../../components/DistributionChart";
import Header from "../../components/Header";
import Swal from 'sweetalert2';
import 'katex/dist/katex.min.css';

export default function MultinomialSimulation() {
  const [n, setN] = useState(100); // tamaño de muestra
  const [rep, setRep] = useState(1); // número de repeticiones
  const [numCategorias, setNumCategorias] = useState(3); // número de categorías
  const [probs, setProbs] = useState(Array(3).fill(0.33)); // arreglo dinámico de probabilidades
  const [data, setData] = useState(null);

  const handleNumCategoriasChange = (value) => {
    const num = Number(value);
    setNumCategorias(num);
    setProbs(Array(num).fill(1 / num)); // inicializa con probas iguales
  };

  const fetchData = async () => {
    const params = new URLSearchParams();
    params.append("n", n);
    params.append("rep", rep);
    probs.forEach((p) => params.append("probs", p));
    
    const res = await fetch(`http://localhost:8000/multinomial?${params.toString()}`);
    const json = await res.json();
    setData(json);
  };

  // Actualizar valor de probabilidad individual
  const handleProbChange = (index, value) => {
    const updated = [...probs];
    updated[index] = parseFloat(value) || 0;
    setProbs(updated);
  };

  return (
    <div className="flex flex-col items-center min-h-screen bg-gray-50 p-10">
      <Header 
        distributionName={"Multinomial"}
        formula={"f(x) = \\frac{k!}{n_1!\\,n_2!\\, \\cdots \\, n_k!} \\quad \\theta_1^{n_1} \\, \\theta_2^{n_2} \\, \\cdots \\, \\theta_k^{n_k}"}  
      />

      <div className="w-[95vw] h-[95vh] bg-white shadow-lg rounded-lg p-6 grid grid-cols-3 gap-4">
        {/* Paneles izquierdos*/}
        <div className="col-span-1 flex flex-col gap-6">
          {/* Panel 1: Inputs */}
          <div className="bg-gray-100 p-4 rounded shadow">
            <h2 className="text-xl font-bold text-gray-700 mb-4">
              Parámetros
            </h2>
            <div className="mb-4">
              <label className="block text-gray-700 mb-1">
                Tamaño de muestra (N):
              </label>
              <input
                type="number"
                value={n}
                onChange={(e) => setN(Number(e.target.value))}
                className="w-full border p-2 rounded"
              />
            </div>
            <div className="mb-4">
              <label className="block text-gray-700 mb-1">
                Repeticiones:
              </label>
              <input
                type="number"
                step="1"
                value={rep}
                onChange={(e) => setRep(Number(e.target.value))}
                className="border p-2 rounded w-full"
              />
            </div>
            <div className="mb-2 col-span-2">
              <label className="block text-gray-700 mb-1">Número de categorías</label>
              <input
                type="number"
                min="2"
                value={numCategorias}
                onChange={(e) => handleNumCategoriasChange(e.target.value)}
                className="w-full p-2 border rounded"
              />
            </div>
            <div className="mb-4">
              <h2 className="text-gray-700 font-semibold mb-2">Probabilidades</h2>
              {probs.map((p, idx) => (
                <div key={idx} className="flex items-center gap-2 mb-2">
                  <label className="w-24">Categoría {idx + 1}:</label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    max="1"
                    value={p}
                    onChange={(e) => handleProbChange(idx, e.target.value)}
                    className="border p-2 rounded w-32"
                  />
                </div>
              ))}
              <p className="text-sm text-gray-500">
                ⚠️ La suma de todas las probabilidades debe ser 1.
              </p>
            </div>

          </div>

          {/* Panel 2: Botones */}
          <div className="bg-gray-100 p-4 rounded shadow flex flex-col gap-4">
            <button
              onClick={fetchData}
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              Generar
            </button>
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
        <div className="col-span-2 bg-gray-100 p-4 rounded shadow flex items-center justify-center">
          {data ? (
            <DistributionChart type="multinomial" data={data} />
          ) : (
            <p className="text-gray-500">Genera la simulación para ver la gráfica.</p>
          )}
        </div>
      </div>
    </div>
  );
}