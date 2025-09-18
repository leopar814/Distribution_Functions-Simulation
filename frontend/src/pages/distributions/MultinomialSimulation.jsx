import { useState, useEffect } from "react";
import DistributionChart from "../../components/DistributionChart";
import Header from "../../components/Header";
import Swal from 'sweetalert2';
import 'katex/dist/katex.min.css';
import Parametros from "../../components/Parametros";
import Accordion from "../../components/Accordion";

export default function MultinomialSimulation() {

  const [n, setN] = useState(100); // tamaño de muestra
  const [rep, setRep] = useState(1); // número de repeticiones
  const [numCategorias, setNumCategorias] = useState(3); // número de categorías
  const [probs, setProbs] = useState(Array(3).fill(0.33)); // arreglo dinámico de probabilidades
  const [loading, setLoading] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [data, setData] = useState(null);
  const params = [
    { label: "Tamaño de Muestra", marker: "N", type: "number", value: n, setter: setN },
    { label: "Repeticiones", type: "number", step: 1, value: rep, setter: setRep },
    { label: "Número de categorías", type: "number", step: 1, min: 2, value: numCategorias, setter: setNumCategorias }
  ];

  useEffect(() => {
    setProbs(Array(numCategorias).fill(1 / numCategorias)); // inicializa con probas iguales
  }, [numCategorias]);

  const fetchData = async () => {
    setLoading(true);
    try {

      const params = new URLSearchParams();
      params.append("n", n);
      params.append("rep", rep);
      probs.forEach((p) => params.append("probs", p));
        
      const res = await fetch(`http://localhost:8000/multinomial?${params.toString()}`);
      const json = await res.json();
    setData(json);
    } catch (err) {
        console.log(err.message);
    } finally {
        setLoading(false);
    }
  };


  // Actualizar valor de probabilidad individual
  const handleProbChange = (index, value) => {
    const updated = [...probs];
    updated[index] = parseFloat(value) || 0;
    setProbs(updated);
  };

  return (
    <div className="flex flex-col items-center h-screen overflow-auto bg-gray-50">

      <Header 
        distributionName={"Multinomial"}
        formula={"f(x) = \\frac{k!}{n_1!\\,n_2!\\, \\cdots \\, n_k!} \\quad \\theta_1^{n_1} \\, \\theta_2^{n_2} \\, \\cdots \\, \\theta_k^{n_k}"}  
      />

      <div className="w-[95vw] bg-white shadow-lg rounded-lg p-6 grid grid-cols-3 gap-4">
        {/* Paneles izquierdos*/}
        <div className="col-span-1 flex flex-col gap-6">
          {/* Panel 1: Inputs */}
          <div className="bg-gray-100 p-4 rounded shadow">

            <Parametros 
              params={params} 
            />

            <div className="mb-4">
              <h2 className="text-gray-700 font-semibold text-xl mb-2">Probabilidades</h2>
              {probs.map((p, idx) => (
                <div key={idx} className="flex items-center gap-2 mb-2">
                  <label className="w-24 text-lg">Categoría {idx + 1}:</label>
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
            <button
              onClick={fetchData}
              disabled={loading}
              className="w-full px-4 py-3 text-blue-800 border-2 border-blue-800 rounded hover:bg-blue-100 disabled:bg-gray-500 disabled:text-gray-200 disabled:border-none"
            >
              {loading ? "Generando..." : "Generar Muestras"}
            </button>
          </div>

          {/* Panel 2:*/}
          {data && (
            <div className="flex flex-col items-center bg-gray-100 p-4 rounder shadow gap-4 mb-4">
              <Accordion title="Ver muestra">
                {data.vectores.map((_, i) => (
                  <p key={i} value={i}>
                    {`{ ${data.vectores[i].join(", ")} }`}
                  </p>
                ))}
              </Accordion>
            </div>
          )}
        </div>

        {/* Panel derecho: Gráfica */}
        <div className="col-span-2 bg-gray-100 p-4 rounded shadow flex items-center justify-center">
          {data ? (
            <DistributionChart type="multinomial" data={data} selectedIndex={selectedIndex} setSelectedIndex={setSelectedIndex}/>
          ) : (
            <p className="text-gray-500">Genera la simulación para ver la gráfica.</p>
          )}
        </div>
      </div>
    </div>
  );
}