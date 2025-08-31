// import { useEffect, useState } from "react";
// import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts";

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, LabelList } from "recharts";

export default function DistributionChart({ exitos, fracasos }) {
  const data = [
    { name: "Éxito", value: Number(exitos) },
    { name: "Fracaso", value: Number(fracasos) },
  ];

  return (
    <div className = "p-4">
      <h2 className = "text-lg font-bold mb-2"> Resultados </h2>
      <BarChart width={500} height={300} data={data}>
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

//   const [data, setData] = useState([]);

//   useEffect(() => {
//     fetch(`http://localhost:8000/distribution?type=${type}&mean=0&std=1&n=200`)
//       .then(res => res.json())
//       .then(json => {
//         setData(json.samples.map((val, idx) => ({ x: idx, y: val })));
//       });
//   }, [type]);

//   return (
//     <div className="p-4">
//       <h1 className="text-xl font-bold mb-2">
//         Distribución {type.charAt(0).toUpperCase() + type.slice(1)}
//       </h1>
//       <LineChart width={600} height={300} data={data}>
//         <CartesianGrid strokeDasharray="3 3" />
//         <XAxis dataKey="x" />
//         <YAxis />
//         <Tooltip />
//         <Line type="monotone" dataKey="y" stroke="#8884d8" />
//       </LineChart>
//     </div>
//   );
// }
