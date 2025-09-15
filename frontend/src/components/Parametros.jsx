export default function Parametros({ params }) {

    return (
        <div className="p-4">
            <h2 className="text-xl font-bold text-gray-700 mb-4">Parámetros</h2>

            {params.map((p, idx) => (
                <div key={idx} className="mb-4">
                    <label className="block text-gray-700 mb-1">{p.label}</label>
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
            ))}
        </div>
    );
}
