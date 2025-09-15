import { useState } from "react";
import Swal from 'sweetalert2';
import 'katex/dist/katex.min.css';
import DistributionChart from "../../components/DistributionChart";
import Header from "../../components/Header";
import Parametros from "../../components/Parametros";


export default function BinomialSimulation() {
    
    const [n, setN] = useState(1000);
    const [media, setMedia] = useState(0);
    const [desviacionEst, setDesviacionEst] = useState(1);
    const [data, setData] = useState(null);

    const params = [
      { label: "Tamaño de la Muestra", type: "number",  min: 0, value: n, setter: setN },
      { label: "Media", type: "number", min: 0, value: media, setter: setMedia },
      { label: "Desviación Estándar", type: "number", min: 0, value: desviacionEst, setter: setDesviacionEst }
    ];

    const fetchData = async () => {
      const res = await fetch(`http://localhost:8000/normal?repeticiones=${n}&mu=${media}&sigma=${desviacionEst}`);
      const json = await res.json();
      setData(json);
  };
    return (
      <div className = "flex flex-col  items-center min-h-screen bg-gray-50 p-10">
        
        <Header 
          distributionName={"Normal"}
          formula={"f(x) = \\frac{1}{\\sigma \\sqrt{2\\pi}} \\exp^{\\!\\biggl(-\\frac{(x - \\mu)^2}{2\\sigma^2}\\biggr)}"}  
        />

        <div className="w-[95vw] h-[95vh] bg-white shadow-lg rounded-lg p-6 grid grid-cols-3 gap-4">
          {/* Panel izquierdo (2 filas: inputs y botones) */}
          <div className="col-span-1 flex flex-col gap-6">
              {/* Panel 1: Inputs */}
            <div className="bg-gray-100 p-4 rounded shadow">

              <Parametros params={params} />

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
                <DistributionChart type="normal" data={data} />

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
