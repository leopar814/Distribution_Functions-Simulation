import { BlockMath } from "react-katex";

export default function Parametros({ params, fetchData, loading }) {

    return (
        <div className="p-4">
            <h2 className="text-3xl font-bold text-gray-700 mb-4">Parámetros</h2>

            {params.map((p, idx) => (
                <div key={idx} className="mb-4">
                    <label className="block text-xl text-gray-700 ">{p.label}</label>
                    <div className="flex flex-row items-center">
                        <span className={`${p.marker ? "text-lg mr-3" : "" }`}>
                            {p.marker ? <BlockMath math={`${p.marker}=`} /> 
                            : ""}
                        </span>
                        <input
                            type={p.type}
                            step={p.step}
                            min={p.min}
                            max={p.max}
                            value={p.value}
                            onChange={(e) => p.setter(p.type === "number" ? Number(e.target.value) : e.target.value)}
                            className="border p-2 rounded w-full"
                        />
                    </div>
                </div>
            ))}

            {fetchData && (
            <button
                onClick={fetchData}
                disabled={loading}
                className="w-full px-4 py-3 text-blue-800 border-2 border-blue-800 rounded hover:bg-blue-100 disabled:bg-gray-500 disabled:text-gray-200 disabled:border-none"
            >
                {loading ? "Generando..." : "Generar Muestras"}
            </button>
            )}

        </div>
    );
}
