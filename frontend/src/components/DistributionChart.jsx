import Plot from "react-plotly.js";

export default function DistributionChart({ type, data }) {
  if (type === "bernoulli") {
    const x = ["Éxito", "Fracaso"];
    const y = [Number(data.exitos), Number(data.fracasos)];

    return (
      <div className="flex flex-col p-4 h-full w-full justify-center items-center">
        <h2 className="flex text-lg font-bold mb-2">Resultados</h2>
        <Plot
          data={[
            {
              x,
              y,
              type: "bar",
              marker: { color: ["#4CAF50", "#F44336"] },
              text: y.map(String),
              textposition: "inside",
              insidetextanchor: "middle",
              textfont: { size: 18, color: "white"},
            },
          ]}
          layout={{
            autosize: true,
            margin: { t: 40, b: 50, l: 50, r: 30 },
            xaxis: { title: {text: "Resultado"} },
            yaxis: { title: {text: "Frecuencia"} },
          }}

          useResizeHandler={true}
          style={{ width: "80%", height: "80%" }}

        />
      </div>
    );
  }

  else if (type === "binomial") {
    return (
      <div className="flex flex-col p-4 h-full w-full justify-center items-center">
        <h2 className="text-lg font-bold mb-2">Distribución Binomial</h2>
        <Plot
          data={[
            {
              x: data.frecuencias.map(d => d.x),
              y: data.frecuencias.map(d => d.y),
              type: "bar",
              marker: { color: "#82ca9d" },
              text: data.frecuencias.map(d => d.y.toString()),
              textposition: "inside",
              insidetextanchor: "middle",
              textfont: { size: 16, color: "black" },
            },
          ]}
          layout={{
            autosize: true,
            margin: { t: 40, b: 50, l: 50, r: 30 },
            xaxis: { title: { text: "Número de éxitos", font: { size: 14 } } },
            yaxis: { title: { text: "Frecuencia", font: { size: 14 } } },
          }}

          useResizeHandler={true}
          style={{ width: "80%", height: "100%" }}

        />
      </div>
    );
  }

  else if (type === "exponential") {

    return (
      <div className="flex flex-col p-4 h-full w-full justify-center items-center">
        <h2 className="text-lg font-bold mb-2">Distribución Exponencial</h2>
        <Plot
          data={[
            {
              x: data.frecuencias.map(d => d.x),
              y: data.frecuencias.map(d => d.y),
              type: "bar",
              marker: { color: "#344fd8" },
              name: "Frecuencias simuladas",
            },
            {
              x: data.teorica.map(d => d.x),
              y: data.teorica.map(d => d.y),
              type: "scatter",
              mode: "lines",
              line: { color: "red", width: 2 },
              name: "Distribución teórica",
            },
          ]}
          layout={{
            autosize: true,
            margin: { t: 40, b: 50, l: 50, r: 30 },
            xaxis: { title: "Intervalos" },
            yaxis: { title: "Frecuencia" },
            xaxis: { title: { text: "x", font: { size: 16 } } },
            yaxis: { title: { text: "Frecuencia / Densidad", font: { size: 16 } } },
            showlegend: true,
          }}
        />
      </div>
    );
  }

  else if (type === "multinomial") {
    return (
      <div className="flex flex-col p-4 h-full w-full justify-center items-center">
        <h2 className="text-lg font-bold mb-2">Distribución Multinomial</h2>
        <Plot
          data={[
            {
              x: data.categorias,
              y: data.conteos,
              type: "bar",
              marker: { color: "#2196F3" },
              text: data.conteos.map(c => c.toString()),
              textposition: "inside",
              insidetextanchor: "middle",
              textfont: { size: 16, color: "white" },
            },
          ]}
          layout={{
            autosize: true,
            margin: { t: 40, b: 50, l: 50, r: 30 },
            xaxis: { title: { text: "Categorías", font: { size: 14 } } },
            yaxis: { title: { text: "Frecuencia", font: { size: 14 } } },
          }}
        />
      </div>
    );
  }

  else if (type === "gebbs") {
    return (
      <div className="flex flex-col p-4 h-full w-full justify-center items-center">
        <h2 className="text-lg font-bold mb-2">Muestreo por Gibbs</h2>
        <Plot
          data={[
            {
              x: data.muestras.map(p => p.x),
              y: data.muestras.map(p => p.y),
              type: "scatter",
              mode: "markers+lines",
              marker: { color: "red", size: 6 },
              line: { color: "rgba(0,0,0,0.2)", width: 1 },
              name: "Muestras"
            },
            {
              x: [data.inicio.x],
              y: [data.inicio.y],
              type: "scatter",
              mode: "markers+text",
              text: ["Inicio"],
              textposition: "top right",
              marker: { color: "green", size: 10 },
              name: "Inicio"
            },
            {
              x: [data.fin.x],
              y: [data.fin.y],
              type: "scatter",
              mode: "markers+text",
              text: ["Fin"],
              textposition: "top right",
              marker: { color: "blue", size: 10 },
              name: "Fin"
            }
          ]}
          layout={{
            autosize: true,
            margin: { t: 40, b: 50, l: 60, r: 40 },
            xaxis: { title: { text: "X", font: { size: 14 } } },
            yaxis: { title: { text: "Y", font: { size: 14 } } },
            showlegend: true
          }}
        />
      </div>
    );
  }


  return null;
}
