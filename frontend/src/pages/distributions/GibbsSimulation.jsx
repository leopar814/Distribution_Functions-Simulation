import { useState } from "react";
import Header from "../../components/Header";
import DistributionChart from "../../components/DistributionChart";
import Parametros from "../../components/Parametros";
import Accordion from "../../components/Accordion";

export default function GibbsSimulation() {
  const [funcion, setFuncion] = useState("1/28*(2*x+3*y+2)"); // Ejemplo
  const [xMin, setXMin] = useState(0);
  const [xMax, setXMax] = useState(2);
  const [yMin, setYMin] = useState(0);
  const [yMax, setYMax] = useState(2);
  const [xInicio, setXInicio] = useState(5);
  const [yInicio, setYInicio] = useState(5);
  const [puntoInicial, setPuntoInicial] = useState(false); // false si es aleatorio
  const [n, setN] = useState(20);

  const[maxToShow, setMaxToShow] = useState(10);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const params = [
    { label: "Función f(x, y) a simular: ", type: "text", value: funcion, setter: setFuncion },
    { label: "Tamaño de muestra", marker: "N", type: "number", value: n, setter: setN },
    { marker: "x_{min}", type: "number", value: xMin, setter: setXMin },
    { marker: "x_{max}", type: "number", value: xMax, setter: setXMax },
    { marker: "y_{min}", type: "number", value: yMin, setter: setYMin },
    { marker: "y_{max}", type: "number", value: yMax, setter: setYMax },
    {
      label: "Punto inicial",
      type: "radio", // nuevo tipo
      options: [
        { label: "Aleatorio", value: false },
        { label: "Definido", value: true },
      ],
      value: puntoInicial,
      setter: setPuntoInicial,
    },
  ];

  if (puntoInicial) {
    params.push(
      { marker: "x_{inicio}", type: "number", value: xInicio, setter: setXInicio },
      { marker: "y_{inicio}", type: "number", value: yInicio, setter: setYInicio }
    );
  }


  const fetchData = async () => {
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
        ...(puntoInicial && { xinicio: xInicio, yinicio: yInicio }),
      });
      const res = await fetch(`http://localhost:8000/gibss?${params.toString()}`);
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
    <div className="flex flex-col items-center min-h-screen bg-gray-50">
      <Header 
        distributionName={"Gibbs"}
        formula={funcion}  
      />
      <div className="w-[95vw] h-fit m-4 bg-white shadow-lg rounded-lg p-6 grid grid-cols-3 gap-4">
        <div className="flex flex-col col-span-1 gap-4 bg-gray-100 p-4 rounded shadow">
          <div className="mb-4">

            <Parametros 
              params={params} 
              fetchData={fetchData}
              loading={loading}
            />
            
            {data && (
              <div className="flex flex-col items-center bg-gray-100 p-4 rounder shadow gap-4 mb-4">
                <div className="flex gap-2 justify-center items-center">
                  <label>Mostrar primeros:</label>
                  <input
                    type="number"
                    min={1}
                    max={data.muestras.length}
                    value={maxToShow}
                    onChange={(e) => setMaxToShow(Number(e.target.value))}
                    className="border px-2 py-1 rounded w-20"
                  />
                  <span>elementos</span>
                </div>
                <Accordion title="Ver muestra">
                  {data.muestras.slice(0, maxToShow).map((p, idx) => (
                    <p key={idx}>
                      {`x${idx+1} = ${p.x.toFixed(5)}, y${idx+1} = ${p.y.toFixed(5)}`}
                    </p>
                  ))}
                </Accordion>


              </div>
            )}

          </div>

        {error && <p className="text-red-600 mt-3">{error}</p>}
        </div>
        <div className="col-span-2 bg-gray-100 p-4 rounded shadow flex items-center justify-center">
          {data && (
            <div className="mt-6">
            <DistributionChart type="gibss" data={data} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
