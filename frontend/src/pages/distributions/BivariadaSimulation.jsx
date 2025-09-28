import { useState } from "react";
import DistributionChart from "../../components/DistributionChart";
import 'katex/dist/katex.min.css';
import { BlockMath } from 'react-katex';
import Header from "../../components/Header";
import Parametros from "../../components/Parametros";
import Accordion from "../../components/Accordion";


export default function BivariadaSimulation() {
  const [n, setN] = useState(500);
  const [mx, setMx] = useState(0);
  const [my, setMy] = useState(0);
  const [varx, setVarx] = useState(1);
  const [vary, setVary] = useState(1);
  const [rho, setRho] = useState(0);
  const [grid, setGrid] = useState(60);

  const [loading, setLoading] = useState(false);
  const [maxToShow, setMaxToShow] = useState(10);
  const [data, setData] = useState(null);

  const params = [
    { label: "Tamaño de muestra", marker: "N", type: "number", value: n, setter: setN },
    { label: "Media X (μx)", type: "number", step: "0.1", value: mx, setter: setMx },
    { label: "Media Y (μy)", type: "number", step: "0.1", value: my, setter: setMy },
    { label: "Varianza X", type: "number", step: "0.1", value: varx, setter: setVarx },
    { label: "Varianza Y", type: "number", step: "0.1", value: vary, setter: setVary },
    { label: "Correlación (ρ)", type: "number", step: "0.01", min: -1, max: 1, value: rho, setter: setRho },
    { label: "Grid (surface resolution)", type: "number", step: 10, value: grid, setter: setGrid },
  ];


 const fetchData = async () => {
    setLoading(true);
    try {
      // Validaciones client-side rápidas
      if (n <= 0) throw new Error("n debe ser mayor que 0");
      if (varx <= 0 || vary <= 0) throw new Error("Las varianzas deben ser mayores que 0");
      if (rho < -1 || rho > 1) throw new Error("ρ debe estar entre -1 y 1");

      const params = new URLSearchParams();
      params.append("n", n);
      params.append("mx", mx);
      params.append("my", my);
      params.append("varx", varx);
      params.append("vary", vary);
      params.append("rho", rho);
      params.append("grid", grid);

      const res = await fetch(`http://localhost:8000/normal_bivariada?${params.toString()}`);
      if (!res.ok) {
        const err = await res.json().catch(() => null);
        throw new Error(err?.detail || `Error ${res.status}`);
      }
      const json = await res.json();
      setData(json);
    } catch (error) {
      console.error(error);
      Swal.fire({ icon: "error", title: "Error", text: error.message || "Fallo al generar" });
    } finally {
      setLoading(false);
    }
  };

    // Helper para renderizar muestras en el formato pedido
  const renderMuestrasInline = (maxDecimals = 4) => {
    if (!data?.muestras) return "";
    return data.muestras
      .slice(0, maxToShow)
      .map((p, i) => (
        <p>
          {`x${i + 1} = ${Number(p[0]).toFixed(maxDecimals)} , y${i + 1} = ${Number(p[1]).toFixed(maxDecimals)}`}
        </p>
      ))};



  return (
    <div className="flex flex-col items-center min-h-screen bg-gray-50">
      
      <Header 
        distributionName={"Normal Bivariada"}
        formula={"\\; f(\\mathbf{x}) = \\frac{1}{2\\pi\\sqrt{|\\Sigma|}} \\exp\\left(-\\tfrac{1}{2}(\\mathbf{x}-\\mu)^T \\Sigma^{-1} (\\mathbf{x}-\\mu)\\right)"}  
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
                <Accordion title={"Ver muestra"}>
                  <div className="text-sm">{renderMuestrasInline(4)}</div>
                </Accordion>

              </div>
            )}
        </div>

        {/* Panel derecho: Gráfica */}
        <div className="flex col-span-2 bg-gray-100 p-4 rounded shadow justify-center items-center">
          {data ? (
            <DistributionChart type="bivariada" data={data} />
          ) : (
            <p className="text-xl text-gray-500">Genera la simulación para ver la gráfica...</p>
          )}
        </div>
      </div>
    </div>
  );
}