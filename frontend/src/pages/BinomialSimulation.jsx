import { useState } from "react";
import DistributionChart from "./DistributionChart";
import Swal from 'sweetalert2';

export default function BinomialSimulation() {
    
    const [repeticiones, setRepeticiones] = useState(10000);
    const [muestra, setMuestra] = useState(10);
    const [proba_exito, setProba_exito] = useState(0.5);
    const [data, setData] = useState(null);

    const fetchData = async () => {
    const res = await fetch(`http://localhost:8000/binomial?repeticiones=${repeticiones}&muestra=${muestra}&proba_exito=${proba_exito}`);
    const json = await res.json();
    setData(json);
  };
    return (
      <div className = "flex flex-col items-center p-6 gap-4">
        <h1 className = "text-2xl font-bold mb-4">Simulación de Distribución Binomial</h1>

        <div className="flex gap-4 ">
            <div>
            <label> Número de Repeticiones: </label>
            <input 
                type = "number"
                value = {repeticiones}
                onChange = {(e) => setRepeticiones(Number(e.target.value))}
                className="border p-2 rounded mb-6"
            />
            </div>
            <div>
            <label> Elementos en Muestra: </label>
            <input 
              type = "number"
              value = {muestra}
              onChange = {(e) => setMuestra(Number(e.target.value))}
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
            <DistributionChart type="binomial" data={data} />

            <button
              onClick={() => Swal.fire({
                title: 'Secuencia Binomial',
                text: data.secuencia.join(", "),
                icon: 'success'
              })}
              className="bg-green-500 text-white p-2 rounded mt-1"
            >
              Ver secuencia
            </button>
          </div>
        )}

      </div>
    );
}
