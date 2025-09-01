import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, LabelList } from "recharts";

export default function DistributionChart({ type, data }) {
  if (type == "bernoulli") {
    const localData = [
      { name: "Éxito", value: Number(data.exitos) },
      { name: "Fracaso", value: Number(data.fracasos) },
    ];

    return (
      <div className = "p-4">
        <h2 className = "text-lg font-bold mb-2"> Resultados </h2>
        <BarChart width={500} height={300} data={localData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#8884d8">
            <LabelList dataKey="value" position="top" />
          </Bar>
        </BarChart>
      </div>
    );
  }
  else if (type == "binomial") {
    console.log("DATA BINOMIAL:", data);

    return (
      <div className="p-4">
        <BarChart width={600} height={300} data={data.frecuencias}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="x" label={{ value: "Número de éxitos", position: "insideBottom", offset: -5 }} />
          <YAxis label={{ value: "Frecuencia", angle: -90, position: "insideLeft" }} />
          <Tooltip />
          <Bar dataKey="y" fill="#82ca9d">
            <LabelList dataKey="y" position="top" />
          </Bar>
        </BarChart>
      </div>
    );

  }
}

