import { useState } from "react";
import DistributionChart from "../../components/DistributionChart";
import Header from "../../components/Header";
import Swal from 'sweetalert2';
import 'katex/dist/katex.min.css';

export default function BinomialSimulation() {
    
    const [n, setN] = useState(1000);
    const [lambda, setLambda] = useState(1.0);
    const [data, setData] = useState(null);

    const fetchData = async () => {
      if (lambda <= 0) {
        Swal.fire("Error", "λ debe ser mayor que 0", "error");
        return;
      }
      const res = await fetch(`http://localhost:8000/exponential?n=${n}&lambda_=${lambda}`);
      const json = await res.json();
      setData(json);
  };
    return (
      <div className = "flex flex-col  items-center min-h-screen bg-gray-50 p-10">
        <Header 
          distributionName={"Exponencial"}
          formula={"f(x) = \\lambda e^{-\\lambda x}, \\quad x \\geq 0"}  
        />

        <div className="w-[95vw] h-[95vh] bg-white shadow-lg rounded-lg p-6 grid grid-cols-3 gap-4">
          {/* Panel izquierdo (2 filas: inputs y botones) */}
          <div className="col-span-1 flex flex-col gap-6">
              {/* Panel 1: Inputs */}
            <div className="bg-gray-100 p-4 rounded shadow">
              <h2 className="text-xl font-bold text-gray-700 mb-4">
                Parámetros
              </h2>
              <div>
                <label className="block text-xl text-gray-700 mb-1"> Número de Muestras: </label>
                <input 
                    type = "number"
                    value = {n}
                    onChange = {(e) => setN(Number(e.target.value))}
                    className="border p-2 rounded mb-6"
                />
                </div>
                <div>
                <label className="block text-xl text-gray-700 mb-1"> λ (Lambda): </label>
                <input 
                  type = "number"
                  step = "0.1"
                  min = "0.1"
                  value = {lambda}
                  onChange = {(e) => setLambda(Number(e.target.value))}
                  className="border p-2 rounded mb-6"
                    />
                </div>
              
                <button
                  onClick = {fetchData}
                  className="w-full bg-blue-500 text-xl text-white p-4 rounded mb-3 hover:bg-blue-600"
                > 
                  Generar
                </button>
              </div>
          </div>
        
          
          <div className="flex col-span-2 bg-gray-100 p-4 rounded shadow items-center">
            {data && (
              <div className = "w-full flex flex-col items-center">
                <DistributionChart type="exponential" data={data} />

                <button
                  onClick={() => Swal.fire({
                    title: 'Muestras exponenciales',
                    text: data.muestras.join(", "),
                    icon: 'success'
                  })}
                  className="bg-green-500 text-white p-2 rounded mt-1"
                >
                  Ver muestras
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    );
}
