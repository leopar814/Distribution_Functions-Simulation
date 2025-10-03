import { useState } from "react";
import DistributionChart from "../../components/DistributionChart";
import Header from "../../components/Header";
import Accordion from "../../components/Accordion";
import Swal from 'sweetalert2';
import 'katex/dist/katex.min.css';
import Parametros from "../../components/Parametros";

export default function BinomialSimulation() {
    
    const [n, setN] = useState(1000);
    const [lambda, setLambda] = useState(1.0);
    const [loading, setLoading] = useState(false);
    const [maxToShow, setMaxToShow] = useState(10);

    const [data, setData] = useState(null);

    const params = [
      { label: "Tamaño de muestra", marker: "N", type: "number",  min: 0, value: n, setter: setN },
      { label: "Lambda", marker: "\\lambda", type: "number", min: 0, value: lambda, setter: setLambda }
    ];

    const fetchData = async () => {
      if (lambda <= 0) {
        Swal.fire("Error", "λ debe ser mayor que 0", "error");
        return;
      }
      setLoading(true);
      try {
        const res = await fetch(`http://localhost:8000/exponential?n=${n}&lambda_=${lambda}`);
        const json = await res.json();
        setData(json);
      } catch (err) {
          console.log(err.message);
      } finally {
          setLoading(false);
      }
  };
    return (
      <div className = "flex flex-col  items-center min-h-screen bg-gray-50">
        
        <Header 
          distributionName={"Exponencial"}
          formula={"f(x) = \\lambda e^{-\\lambda x}, \\quad x \\geq 0, \\quad \\lambda > 0"}  
        />

        <div className="w-[95vw] h-fit m-4 bg-white shadow-lg rounded-lg p-6 grid grid-cols-3 gap-4">
          {/* Panel izquierdo (2 filas: inputs y botones) */}
          <div className="col-span-1 flex flex-col gap-6">
              {/* Panel 1: Inputs */}
            <div className="bg-gray-100 p-4 rounded shadow">

              <Parametros 
                params={params} 
                fetchData={fetchData}
                loading={loading}
              />  

            </div>

            {/* Panel 2 */}            
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
                    {data.frecuencias.slice(0, maxToShow).map((p, idx) => (
                      <p key={idx}>
                        {`x${idx+1} = ${p.x.toFixed(5)}, y${idx+1} = ${p.y.toFixed(5)}`}
                      </p>
                    ))}
                </Accordion>
              </div>
            )}
            
          </div>
        
          
          <div className="flex bg-black col-span-2 bg-gray-100 p-4 rounded shadow justify-center items-center">
            {data ? (
              <DistributionChart type="exponencial" data={data} />
            ) : (
              <p className="text-xl text-gray-500">Genera la simulación para ver la gráfica...</p>
            )}
          </div>
        </div>
      </div>
    );
}
