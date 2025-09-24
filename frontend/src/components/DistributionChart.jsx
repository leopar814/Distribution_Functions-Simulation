import { useState } from "react";
import Plot from "react-plotly.js";

export default function DistributionChart({ type, data, selectedIndex, setSelectedIndex }) {
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
              marker: { color: ["#6fcf72ff", "#F44336"] },
              text: y.map(String),
              textposition: "inside",
              insidetextanchor: "middle",
              textfont: { size: 18, color: "gray-800"},
            },
          ]}
          layout={{
            autosize: true,
            margin: { t: 40, b: 50, l: 50, r: 30 },
            xaxis: { title: {text: "Resultado"} },
            yaxis: { title: {text: "Frecuencia"} },
          }}

          useResizeHandler={true}
          style={{ width: "90%", height: "90%" }}

        />
      </div>
    );
  }

  else if (type === "binomial") {
    const x = data.frecuencias.map(d => d.x);
    const y = data.frecuencias.map(d => d.y);

    return (
      <div className="flex flex-col p-4 h-full w-full justify-center items-center">
        <h2 className="w-full text-2xl font-bold mb-2">Distribución Binomial</h2>
        <Plot
          data={[
            {
              x,
              y,
              type: "bar",
              marker: { color: "#35bc68ff" },
              text: data.frecuencias.map(d => d.y.toString()),
              textposition: "inside",
              insidetextanchor: "middle",
              textfont: { size: 16, color: "black" },
            },
          ]}
          layout={{
            autosize: true,
            margin: { t: 10, b: 50, l: 50, r: 10 },
            xaxis: { 
              title: { text: "Número de éxitos", font: { size: 14 } }, 
              tickmode: "array",
              tickfont: { size: 14 },
              tickvals: x,
              ticktext: x,
              tickangle: 0,     
              automargin: true,
            },
            yaxis: { title: { text: "Frecuencia", font: { size: 14 } } },
          }}

          useResizeHandler={true}
          style={{ width: "100%", height: "100%" }}

        />
      </div>
    );
  }

  else if (type === "exponencial") {

    return (
      <div className="flex flex-col p-4 h-full w-full justify-center items-center">
        <h2 className="w-full text-2xl font-bold mb-2">Distribución Exponencial</h2>
        <Plot
          data={[
            {
              x: data.frecuencias.map(d => d.x),
              y: data.frecuencias.map(d => d.y),
              type: "bar",
              opacity: 0.9,
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
            margin: { t: 10, b: 50, l: 50, r: 10 },
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

    const categorias = data.categorias;
    const vectores = data.vectores;
    const conteoActual = vectores[selectedIndex].map(Number);

    return (
      <div className="flex flex-col p-4 h-full w-full justify-center items-center">
        <h2 className="w-full text-2xl font-bold mb-2">Distribución Multinomial</h2>
        
        <div className="mb-4 flex items-center gap-2">
          <label className="text-sm font-medium">Selecciona vector:</label>
          <select
            value={selectedIndex}
            onChange={(e) => setSelectedIndex(Number(e.target.value))}
            className="border px-2 py-1 rounded"
          >
            {vectores.map((_, i) => (
              <option key={i} value={i}>
                {`Vector ${i + 1} - { ${data.vectores[i].join(", ")} }`}
              </option>
            ))}
          </select>
        </div>


        <Plot
          data={[
            {
              x: categorias,
              y: conteoActual,
              type: "bar",
              marker: { color: "#2196F3" },
              text: conteoActual.map(c => c.toString()),
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
          useResizeHandler
          style={{ width: "80%", height: "80%" }}

        />
      </div>
    );
  }

  else if (type === "gebbs") {
    return (
      <div className="flex flex-col p-4 h-full w-full justify-center items-center">
        <h2 className="w-full text-2xl font-bold mb-2">Muestreo por Gibbs</h2>
        <Plot
          data={[
            {
              x: data.muestras.map(p => p.x),
              y: data.muestras.map(p => p.y),
              type: "scatter",
              mode: "markers",
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

  else if (type === "normal") {
    const freqX = data.frecuencias.map(d => d.x);
    const freqY = data.frecuencias.map(d => d.y);
    const theoX = data.teorica.map(d => d.x);
    const theoY = data.teorica.map(d => d.y);

    return (
      <div className="flex flex-col p-4 h-full w-full justify-center items-center">
        <h2 className="w-full text-2xl font-bold mb-2">Distribución Normal</h2>
        <Plot
          data={[
            {
              x: freqX,
              y: freqY,
              type: "bar",
              name: "Muestra simulada",
              marker: { color: "#82ca9d" },
              opacity: 0.7,
              legendgroup: "simulada",
            },
            {
              x: theoX,
              y: theoY,
              type: "scatter",
              mode: "lines",
              name: "Densidad teórica",
              line: { color: "red", width: 2 },
              legendgroup: "teorica",
            }
          ]}
          layout={{
            autosize: true,
            margin: { t: 10, b: 50, l: 50, r: 10 },
            xaxis: { title: { text: "Valor", font: { size: 14 } } },
            yaxis: { title: { text: "Densidad", font: { size: 14 } } },
            showlegend: true,

            legend: {
              x: 0.8,                 // posición horizontal (0 = izquierda, 1 = derecha)
              y: 1.1,                 // posición vertical por encima del gráfico
              xanchor: "center",      // ancla la x de la leyenda en su centro
              yanchor: "bottom",      // ancla la y de la leyenda en su borde inferior
              orientation: "h",       // disponla horizontalmente
              bgcolor: "rgba(255,255,255,0.8)", // fondo semitransparente
              bordercolor: "#c4c4c4ff",
              borderwidth: 1,
              tracegroupgap: 5,
            },

          }}
          useResizeHandler={true}
          style={{ width: "80%", height: "80%" }}
        />
      </div>
    );
    
  }

  else if (type === "bivariada") {
    const muestras = (data?.muestras || []).map(([x, y]) => ({ x, y }));
    const grid = data?.grid || null;
    const stats = data?.stats || {};

    const scatterX = muestras.map((p) => p.x);
    const scatterY = muestras.map((p) => p.y);

    return (
      <div className="flex flex-col justify-center p-4 w-full">
        <h2 className="text-lg font-bold mb-3">Normal Bivariada (3D / 2D)</h2>

        <div className="flex gap-4 w-full">
          {/* Surface 3D + scatter over surface (izquierda) */}
          <div className="flex-1 bg-white rounded shadow p-2">
            <Plot
              data={[
                // superficie teórica
                grid && {
                  type: "surface",
                  x: grid.x,
                  y: grid.y,
                  z: grid.z,
                  showscale: false,
                  opacity: 0.9,
                  colorscale: "Viridis",
                  name: "PDF Teórica",
                },
                // scatter de muestras en 3D (z ~ 0 para visualizar sobre plano)
                {
                  type: "scatter3d",
                  x: scatterX,
                  y: scatterY,
                  z: scatterX.map(() => 0), // pequeñas marcas en z=0 para visualizar
                  mode: "markers",
                  marker: { size: 2.5, color: "black", opacity: 0.6 },
                  name: "Muestras (proyección)",
                },
              ].filter(Boolean)}
              layout={{
                autosize: true,
                margin: { t: 30, b: 40, l: 40, r: 10 },
                scene: {
                  xaxis: { title: "X" },
                  yaxis: { title: "Y" },
                  zaxis: { title: "Densidad" },
                  camera: { eye: { x: 1.5, y: -1.5, z: 1.0 } },
                },
                showlegend: true,
                legend: {
                  x: 0.8,                 // posición horizontal (0 = izquierda, 1 = derecha)
                  y: 0.9,                 // posición vertical por encima del gráfico
                  xanchor: "center",      // ancla la x de la leyenda en su centro
                  yanchor: "bottom",      // ancla la y de la leyenda en su borde inferior
                  orientation: "h",       // disponla horizontalmente
                  bgcolor: "rgba(255,255,255,0.8)", // fondo semitransparente
                  bordercolor: "#c4c4c4ff",
                  borderwidth: 1,
                  tracegroupgap: 5,
                },
              }}
              useResizeHandler
              style={{ width: "100%", height: "100%" }}
            />
          </div>

          {/* Scatter 2D de las muestras con contorno y estadísticas (derecha) */}
          <div className="w-1/2 bg-white rounded shadow p-2 flex flex-col">
            <div className="flex-1">
              <Plot
                data={[
                  {
                    x: scatterX,
                    y: scatterY,
                    type: "scatter",
                    mode: "markers",
                    marker: { color: "skyblue", size: 6, line: { color: "black", width: 0.5 } },
                    name: "Muestras",
                  },
                ]}
                layout={{
                  autosize: true,
                  margin: { t: 30, b: 50, l: 50, r: 10 },
                  xaxis: { title: "X", automargin: true },
                  yaxis: { title: "Y", automargin: true, scaleanchor: "x", scaleratio: 1 },
                  showlegend: false,
                }}
                useResizeHandler
                style={{ width: "100%", height: "100%" }}
              />
            </div>

            <div className="mt-3 p-2 text-sm bg-gray-50 rounded">
              <p><strong>Estadísticas</strong></p>
              <p>Media X: {stats.mean_x?.toFixed(4)}</p>
              <p>Media Y: {stats.mean_y?.toFixed(4)}</p>
              <p>Varianza X: {stats.var_x?.toFixed(4)}</p>
              <p>Varianza Y: {stats.var_y?.toFixed(4)}</p>
              <p>Correlación: {stats.corr?.toFixed(4)}</p>
              <p className="mt-2 text-xs text-gray-500">Muestras mostradas: {muestras.length}</p>
            </div>
          </div>
        </div>
      </div>


    );
  
  }
  return null;
}
