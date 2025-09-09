import { useState } from "react";
import DistributionChart from "../DistributionChart";
import Swal from 'sweetalert2';
import 'katex/dist/katex.min.css';
import { BlockMath } from 'react-katex';

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
        <div className="w-[90vw] h-[90vh] bg-white shadow-lg rounded-lg p-8">
          <h1 className = "ttext-4xl font-extrabold text-gray-800 mb-6 text-center">Simulación de Distribución Exponencial</h1>
          <BlockMath math="f(x) = \lambda e^{-\lambda x}, \quad x \geq 0" />
          
          <div className="flex flex-row items-center justify-center gap-6">
            <div className="flex flex-col gap-4 ">
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
            </div>
            <button
                    onClick = {fetchData}
                    className="bg-blue-500 text-white p-5 rounded mb-10"
                > Generar </button>
          </div>

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
    );
}
