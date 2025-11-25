import { useState } from "react";
import DistributionChart from "../../components/DistributionChart";
import Header from "../../components/Header";
import Parametros from "../../components/Parametros";
import Accordion from "../../components/Accordion";

export default function MetropolisHastings() {
  const [targetFunction, setTargetFunction] = useState("exp(-x**2/2)");
  const [initialState, setInitialState] = useState(0);
  const [iterations, setIterations] = useState(10000);
  const [sigma, setSigma] = useState(2.5);
  const [burnin, setBurnin] = useState(1000);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [activeTab, setActiveTab] = useState("histogram");
  const [maxToShow, setMaxToShow] = useState(20);

  const presetFunctions = [
    { name: "Normal estándar", func: "exp(-x**2/2)", desc: "N(0,1)" },
    { name: "Mezcla de normales", func: "0.3*exp(-(x+2)**2/2) + 0.7*exp(-(x-2)**2/2)", desc: "Bimodal" },
    { name: "Gamma", func: "(x**2)*exp(-x) if x > 0 else 0", desc: "Gamma(3,1)" },
    { name: "Cauchy", func: "1/(1+x**2)", desc: "Colas pesadas" },
    { name: "T-Student", func: "(1+x**2/3)**(-2)", desc: "t(3)" }
  ];

  const params = [
    { 
      label: "Estado inicial", 
      marker: "x_0", 
      type: "number", 
      step: "0.1",
      value: initialState, 
      setter: setInitialState 
    },
    { 
      label: "Iteraciones", 
      marker: "N", 
    //   type: "range", 
      type: "number", 
      min: 1000,
      max: 50000,
      step: 1000,
      value: iterations, 
      setter: setIterations,
      showValue: true
    },
    { 
      label: "Sigma (propuesta)", 
      marker: "\\sigma", 
      type: "range", 
      min: 0.1,
      max: 5,
      step: 0.1,
      value: sigma, 
      setter: setSigma,
      showValue: true
    },
    { 
      label: "Burn-in", 
      marker: "B", 
      type: "range", 
      min: 0,
      max: Math.floor(iterations * 0.5),
      step: 100,
      value: burnin, 
      setter: setBurnin,
      showValue: true
    }
  ];

  const fetchData = async () => {
    setLoading(true);
    try {
      const queryParams = new URLSearchParams({
        target_function: targetFunction,
        initial_state: initialState,
        iterations: iterations,
        sigma: sigma,
        burnin: burnin,
        thin: Math.max(1, Math.floor(iterations / 2000))
      });
      
      const res = await fetch(`http://localhost:8000/metropolis_hastings?${queryParams}`);
      
      if (!res.ok) {
        const error = await res.json();
        alert(`Error: ${error.detail}`);
        return;
      }
      
      const json = await res.json();
      setData(json);
    } catch (error) {
      console.error(error);
      alert(`Error de conexión: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const getRecommendationColor = (type) => {
    switch(type) {
      case "success": return "bg-green-100 border-green-400 text-green-800";
      case "warning": return "bg-yellow-100 border-yellow-400 text-yellow-800";
      case "info": return "bg-blue-100 border-blue-400 text-blue-800";
      default: return "bg-gray-100 border-gray-400 text-gray-800";
    }
  };

  const getRecommendationIcon = (type) => {
    switch(type) {
      case "success": return "✓";
      case "warning": return "⚠";
      case "info": return "ℹ";
      default: return "•";
    }
  };

  return (
    <div className="flex flex-col items-center min-h-screen bg-gray-50">
      
      <Header 
        distributionName={"Metropolis-Hastings"}
        formula={"\\alpha = \\min\\left(1, \\frac{\\pi(y)}{\\pi(x)}\\right)"}  
      />

      <div className="w-[95vw] h-fit m-4 bg-white shadow-lg rounded-lg p-6 grid grid-cols-3 gap-4">
        
        {/* Panel izquierdo */}
        <div className="col-span-1 flex flex-col gap-6">
          
          {/* Panel 1: Función objetivo */}
          <div className="bg-gray-100 p-4 rounded shadow">
            <h3 className="text-lg font-bold mb-3">Función Objetivo π(x)</h3>
            
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">
                Expresión matemática:
              </label>
              <input
                type="text"
                value={targetFunction}
                onChange={(e) => setTargetFunction(e.target.value)}
                className="w-full border rounded px-3 py-2 font-mono text-sm"
                placeholder="exp(-x**2/2)"
              />
            </div>

            <Accordion title="Funciones preset">
              <div className="space-y-1">
                {presetFunctions.map((preset, idx) => (
                  <button
                    key={idx}
                    onClick={() => setTargetFunction(preset.func)}
                    className="block w-full text-left text-xs p-2 hover:bg-gray-200 rounded transition"
                  >
                    <span className="font-semibold">{preset.name}</span>
                    <span className="text-gray-600"> - {preset.desc}</span>
                  </button>
                ))}
              </div>
            </Accordion>
          </div>

          {/* Panel 2: Parámetros */}
          <div className="bg-gray-100 p-4 rounded shadow">
            <Parametros 
              params={params} 
              fetchData={fetchData}
              loading={loading}
            />
          </div>

          {/* Panel 3: Estadísticas */}
          {data && (
            <div className="bg-gray-100 p-4 rounded shadow">
              <h3 className="text-lg font-bold mb-3">Estadísticas</h3>
              
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="font-medium">Media:</span>
                  <span>{data.statistics.mean.toFixed(4)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Desv. Est.:</span>
                  <span>{data.statistics.std.toFixed(4)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Mediana:</span>
                  <span>{data.statistics.median.toFixed(4)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Min / Max:</span>
                  <span>
                    {data.statistics.min.toFixed(2)} / {data.statistics.max.toFixed(2)}
                  </span>
                </div>
                
                <hr className="my-3" />
                
                <div className="flex justify-between">
                  <span className="font-medium">Tasa aceptación:</span>
                  <span className={
                    data.diagnostics.accepted_ratio < 0.15 ? "text-red-600 font-bold" :
                    data.diagnostics.accepted_ratio > 0.5 ? "text-yellow-600 font-bold" :
                    "text-green-600 font-bold"
                  }>
                    {(data.diagnostics.accepted_ratio * 100).toFixed(1)}%
                  </span>
                </div>
                
                {/* <div className="flex justify-between">
                  <span className="font-medium">ESS:</span>
                  <span>{data.diagnostics.ess.toFixed(0)}</span>
                </div> */}
                
                {/* <div className="flex justify-between">
                  <span className="font-medium">ESS ratio:</span>
                  <span className={
                    data.diagnostics.ess_ratio < 0.1 ? "text-red-600 font-bold" :
                    data.diagnostics.ess_ratio > 0.3 ? "text-green-600 font-bold" :
                    "text-yellow-600 font-bold"
                  }>
                    {(data.diagnostics.ess_ratio * 100).toFixed(1)}%
                  </span>
                </div> */}
                
                {/* {data.diagnostics.geweke_z !== null && (
                  <div className="flex justify-between">
                    <span className="font-medium">Geweke Z:</span>
                    <span className={
                      Math.abs(data.diagnostics.geweke_z) < 1 ? "text-green-600 font-bold" :
                      Math.abs(data.diagnostics.geweke_z) < 2 ? "text-yellow-600 font-bold" :
                      "text-red-600 font-bold"
                    }>
                      {data.diagnostics.geweke_z.toFixed(3)}
                    </span>
                  </div>
                )} */}
              </div>
            </div>
          )}

          {/* Panel 4: Recomendaciones
          {data && data.recommendations && (
            <div className="bg-gray-100 p-4 rounded shadow">
              <h3 className="text-lg font-bold mb-3">Diagnósticos</h3>
              
              <div className="space-y-3">
                {data.recommendations.map((rec, idx) => (
                  <div
                    key={idx}
                    className={`p-3 border-l-4 rounded ${getRecommendationColor(rec.type)}`}
                  >
                    <div className="flex items-start gap-2">
                      <span className="text-lg font-bold">
                        {getRecommendationIcon(rec.type)}
                      </span>
                      <div className="flex-1">
                        <p className="font-semibold text-sm">{rec.category}</p>
                        <p className="text-xs mt-1">{rec.message}</p>
                        <p className="text-xs mt-1 font-medium italic">{rec.suggestion}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )} */}

          {/* Panel 5: Muestra de valores */}
          {data && (
            <div className="bg-gray-100 p-4 rounded shadow">
              <div className="flex gap-2 justify-between items-center mb-3">
                <h3 className="text-lg font-bold">Muestra</h3>
                <div className="flex gap-2 items-center">
                  <label className="text-sm">Mostrar:</label>
                  <input
                    type="number"
                    min={5}
                    max={100}
                    value={maxToShow}
                    onChange={(e) => setMaxToShow(Number(e.target.value))}
                    className="border px-2 py-1 rounded w-16 text-sm"
                  />
                </div>
              </div>
              
              <Accordion title="Ver primeros valores">
                <div className="grid grid-cols-2 gap-2 max-h-64 overflow-y-auto">
                  {data.samples.slice(0, maxToShow).map((val, idx) => (
                    <div key={idx} className="bg-white px-2 py-1 rounded text-xs font-mono">
                      <span className="text-gray-500">{idx + 1}:</span> {val.toFixed(6)}
                    </div>
                  ))}
                </div>
              </Accordion>
            </div>
          )}
        </div>

        {/* Panel derecho: Gráficas */}
        <div className="col-span-2 flex flex-col bg-gray-100 rounded shadow">
          {data ? (
            <>
              {/* Tabs */}
              <div className="flex gap-2 p-4 border-b bg-white rounded-t">
                {[
                  { id: "histogram", label: "Histograma" },
                  { id: "trace", label: "Trace Plot" },
                  // { id: "autocorr", label: "Autocorrelación" },
                  // { id: "running", label: "Media Acumulada" }
                ].map(tab => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`px-4 py-2 font-medium rounded transition ${
                      activeTab === tab.id
                        ? "bg-blue-600 text-white"
                        : "bg-gray-200 text-gray-700 hover:bg-gray-300"
                    }`}
                  >
                    {tab.label}
                  </button>
                ))}
              </div>

              {/* Contenido de gráficas */}
              <div className="flex-1 p-4">
                {activeTab === "histogram" && (
                  <DistributionChart 
                    type="mh-histogram" 
                    data={{
                      frecuencias: data.plots.histogram,
                      statistics: data.statistics
                    }} 
                  />
                )}

                {activeTab === "trace" && (
                  <DistributionChart 
                    type="mh-trace" 
                    data={{
                      trace: data.plots.trace,
                      burnin: burnin,
                      initial: initialState
                    }} 
                  />
                )}

                {activeTab === "autocorr" && (
                  <DistributionChart 
                    type="mh-autocorr" 
                    data={{
                      autocorrelation: data.plots.autocorrelation
                    }} 
                  />
                )}

                {activeTab === "running" && (
                  <DistributionChart 
                    type="mh-running" 
                    data={{
                      running_mean: data.plots.running_mean,
                      final_mean: data.statistics.mean
                    }} 
                  />
                )}
              </div>
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center p-12">
              <div className="text-center">
                <p className="text-4xl mb-4">📊</p>
                <p className="text-xl text-gray-500 mb-2">
                  Configura los parámetros y ejecuta la simulación
                </p>
                <p className="text-sm text-gray-400">
                  Las gráficas de convergencia aparecerán aquí
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}