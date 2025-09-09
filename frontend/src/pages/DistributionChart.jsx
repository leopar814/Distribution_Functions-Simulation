import Plot from "react-plotly.js";

export default function DistributionChart({ type, data }) {
  if (type === "bernoulli") {
    const x = ["Éxito", "Fracaso"];
    const y = [Number(data.exitos), Number(data.fracasos)];

    return (
      <div className="p-4">
        <h2 className="text-lg font-bold mb-2">Resultados</h2>
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
            width: 600,
            height: 300,
            margin: { t: 40, b: 50, l: 50, r: 30 },
            xaxis: { title: {text: "Resultado"} },
            yaxis: { title: {text: "Frecuencia"} },
          }}
        />
      </div>
    );
  }

  else if (type === "binomial") {
    return (
      <div className="p-4">
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
            width: 600,
            height: 300,
            margin: { t: 40, b: 50, l: 50, r: 30 },
            xaxis: { title: { text: "Número de éxitos", font: { size: 14 } } },
            yaxis: { title: { text: "Frecuencia", font: { size: 14 } } },
          }}
        />
      </div>
    );
  }

  else if (type === "exponential") {

    return (
      <div className="p-4">
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
            width: 600,
            height: 300,
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

  return null;
}
