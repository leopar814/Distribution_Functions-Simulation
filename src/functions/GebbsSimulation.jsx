import { useState } from "react";
import Header from "../../components/Header";
import DistributionChart from "../../components/DistributionChart";

export default function GibbsSimulation() {
  const [funcion, setFuncion] = useState("x*exp(-x-y)"); // Ejemplo
  const [xmin, setXmin] = useState(0);
  const [xmax, setXmax] = useState(10);
  const [ymin, setYmin] = useState(0);
  const [ymax, setYmax] = useState(10);
  const [n, setN] = useState(200);

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSimulate = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams({
        funcion,
        xmin,
        xmax,
        ymin,
        ymax,
        n,
      });
      const res = await fetch(`http://localhost:8000/gibbs?${params.toString()}`);
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
                formula={"f(x) = "}  
            />
            <h1 className="text-2xl font-bold mb-4">Simulación Gibbs</h1>

            <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                    <label className="block text-sm font-medium">Función f(x,y)</label>
                <input
                    type="text"
                    value={funcion}
                    onChange={(e) => setFuncion(e.target.value)}
                    className="w-full p-2 border rounded"
                />
                </div>

                <div>
                <label className="block text-sm font-medium">Número de muestras (N)</label>
                <input
                    type="number"
                    value={n}
                    onChange={(e) => setN(e.target.value)}
                    className="w-full p-2 border rounded"
                    min="10"
                />
                </div>

                <div>
                <label className="block text-sm font-medium">X min</label>
                <input
                    type="number"
                    value={xmin}
                    onChange={(e) => setXmin(e.target.value)}
                    className="w-full p-2 border rounded"
                />
                </div>

                <div>
                <label className="block text-sm font-medium">X max</label>
                <input
                    type="number"
                    value={xmax}
                    onChange={(e) => setXmax(e.target.value)}
                    className="w-full p-2 border rounded"
                />
                </div>

                <div>
                <label className="block text-sm font-medium">Y min</label>
                <input
                    type="number"
                    value={ymin}
                    onChange={(e) => setYmin(e.target.value)}
                    className="w-full p-2 border rounded"
                />
                </div>

                <div>
                <label className="block text-sm font-medium">Y max</label>
                <input
                    type="number"
                    value={ymax}
                    onChange={(e) => setYmax(e.target.value)}
                    className="w-full p-2 border rounded"
                />
                </div>
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
                <DistributionChart type="gibbs" data={data} />
                </div>
            )}
        </div>
    );
}
