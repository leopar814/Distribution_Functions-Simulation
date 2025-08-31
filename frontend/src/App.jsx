import { useState } from "react";
import DistributionChart from "./DistributionChart";

export default function App() {

  const [repeticiones, setRepeticiones] = useState(100);
  const [proba_exito, setProba_exito] = useState(0.5);
  const [data, setData] = useState(null);

  const fetchData = async () => {
    const res = await fetch(`http://localhost:8000/bernoulli?repeticiones=${repeticiones}&proba_exito=${proba_exito}`);
    const json = await res.json();
    setData(json);
  };
    return (
      <div className = "flex flex-col items-center p-6 gap-4">
        <h1 className = "text-2xl font-bold mb-4">Simulación de Distribuciones</h1>

        <div className="flex gap-4 ">
          <div>
            <label> Número de muestras: </label>
            <input 
              type = "number"
              value = {repeticiones}
              onChange = {(e) => setRepeticiones(Number(e.target.value))}
              className="border p-2 rounded mb-6"
            />
          </div>
          <div>
            <label> Probabilidad de éxito: </label>
            <input
              type = "number"
              step = "0.01"
              min = "0"
              max = "1"
              value = {proba_exito}
              onChange = {(e) => setProba_exito(Number(e.target.value))}
              className="border p-1 rounded mb-6"

            />
          </div>
          <button
            onClick = {fetchData}
            className="bg-blue-500 text-white p-5 rounded mb-10"
          > Generar </button>
        </div>

        {data && (
          <div className = "w-full flex flex-col items-center">
            <DistributionChart exitos = {data.exitos} fracasos = {data.fracasos} />

            <button
              onClick = {() => alert(data.secuencia.join(", "))}
              className="bg-green-500 text-white p-2 rounded mt-1"
            > Ver secuencia </button>  
          </div>
        )}

      </div>
    );
}


//   const [dist, setDist] = useState("normal");

//   return (
//     <div className="flex flex-col items-center p-6">
//       <h1 className="text-2xl font-bold mb-4">Simulación de Distribuciones</h1>
      
//       <select
//         value={dist}
//         onChange={(e) => setDist(e.target.value)}
//         className="border p-2 rounded mb-6"
//       >
//         <option value="normal">Normal</option>
//         <option value="uniform">Uniforme</option>
//       </select>

//       <DistributionChart type={dist} />
//     </div>
//   );
// }
