import { useState } from "react";
import DistributionChart from "../../components/DistributionChart";
import Swal from 'sweetalert2';
import 'katex/dist/katex.min.css';
import Header from "../../components/Header";
import Parametros from "../../components/Parametros";

export default function BinomialSimulation() {
    
    const [repeticiones, setRepeticiones] = useState(10000);
    const [muestra, setMuestra] = useState(10);
    const [probaExito, setProbaExito] = useState(0.5);
    const [data, setData] = useState(null);

    const params = [
      { label: "Número de repeticiones", type: "number", value: repeticiones, setter: setRepeticiones },
      { label: "Elementos en Muestra", type: "number", min: 0, value: muestra, setter: setMuestra },
      { label: "Probabilidad de éxito", type: "number", step: 0.01, min: 0, max: 1, value: probaExito, setter: setProbaExito }
    ];

    const fetchData = async () => {
    const res = await fetch(`http://localhost:8000/binomial?repeticiones=${repeticiones}&muestra=${muestra}&proba_exito=${probaExito}`);
    const json = await res.json();
    setData(json);
  };
    return (
      <div className = "flex flex-col items-center min-h-screen bg-gray-50 p-10">
        
        <Header 
          distributionName={"Binomial"}
          formula={"f(x) = \\binom{k}{x} = \\theta^x \\, (1-\\theta)^{1-x}, \\quad x = 0, 1, 2, \\dots, k"}  
        />

        <div className="w-[95vw] h-[95vh] bg-white shadow-lg rounded-lg p-6 grid grid-cols-3 gap-4">
          {/* Panel izquierdo (2 filas: inputs y botones) */}
          <div className="col-span-1 flex flex-col gap-6">
            <div className="bg-gray-100 p-4 rounded shadow">

              <Parametros params={params} />

              <button
                      onClick = {fetchData}
                      className="w-full bg-blue-500 text-xl text-white p-4 rounded mb-3 hover:bg-blue-600"
                  > Generar </button>
              </div>
            </div>
          

              <div className="flex col-span-2 bg-gray-100 p-4 rounded shadow items-center">
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
        </div>
      </div>
    );
}
