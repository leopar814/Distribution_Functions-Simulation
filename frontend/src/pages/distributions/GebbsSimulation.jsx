import { useState } from "react";
import Header from "../../components/Header";
import DistributionChart from "../../components/DistributionChart";
import Parametros from "../../components/Parametros";

export default function GebbsSimulation() {
  const [funcion, setFuncion] = useState("x*exp(-x-y)"); // Ejemplo
  const [xMin, setXMin] = useState(0);
  const [xMax, setXMax] = useState(10);
  const [yMin, setYMin] = useState(0);
  const [yMax, setYMax] = useState(10);
  const [n, setN] = useState(100);

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const params = [
    { label: "Función f(x,y)", type: "text", value: funcion, setter: setFuncion },
    { label: "Número de muestras (N)", type: "number", value: n, setter: setN },
    { label: "X min", type: "number", value: xMin, setter: setXMin },
    { label: "X max", type: "number", value: xMax, setter: setXMax },
    { label: "Y min", type: "number", value: yMin, setter: setYMin },
    { label: "Y max", type: "number", value: yMax, setter: setYMax },
  ];

  const handleSimulate = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams({
        funcion,
        xmin: xMin,
        xmax: xMax,
        ymin: yMin,
        ymax: yMax,
        n,
      });
      const res = await fetch(`http://localhost:8000/gebbs?${params.toString()}`);
      if (!res.ok) throw new Error("Error en el servidor");
      const json = await res.json();
      setData(json);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

    return (
        <div className="p-6 bg-gray-50 rounded-xl shadow-md">
            <Header 
                distributionName={"Gebbs"}
                formula={funcion}  
            />
            <h1 className="text-2xl font-bold mb-4">Simulación Gibbs</h1>

            <div className="grid grid-cols-2 gap-4 mb-4">

                <Parametros params={params} />

            </div>

            <button
                onClick={handleSimulate}
                disabled={loading}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
            >
                {loading ? "Generando..." : "Generar Muestras"}
            </button>

            {error && <p className="text-red-600 mt-3">{error}</p>}

            {data && (
                <div className="mt-6">
                <DistributionChart type="gebbs" data={data} />
                </div>
            )}
        </div>
    );
}
