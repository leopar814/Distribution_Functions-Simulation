import { useState } from "react";
import 'katex/dist/katex.min.css';
import Header from "../../components/Header";
import DistributionChart from "../../components/DistributionChart";

export default function LDA() {
    const [file, setFile] = useState(null);
    const [K, setK] = useState(5);
    const [iterations, setIterations] = useState(300);
    const [alpha, setAlpha] = useState("");
    const [beta, setBeta] = useState(0.01);
    const [loading, setLoading] = useState(false);
    const [modelInfo, setModelInfo] = useState(null);
    const [viewMode, setViewMode] = useState(null);
    const [selectedIdTopic, setSelectedIdTopic] = useState(0);
    const [selectedIdDoc, setSelectedIdDoc] = useState(0);
    const [topicData, setTopicData] = useState(null);
    const [documentData, setDocumentData] = useState(null);
    const [allTopics, setAllTopics] = useState(null);
    const [allDocuments, setAllDocuments] = useState(null);
    const [matrixTheta, setMatrixTheta] = useState(null);
    const [matrixPhi, setMatrixPhi] = useState(null);
    
    // Estados para controlar visualización de gráficas
    const [showChart, setShowChart] = useState({});

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile && selectedFile.type === "text/plain") {
            setFile(selectedFile);
        } else {
            alert("Por favor selecciona un archivo .txt válido");
        }
    };

    const uploadAndTrain = async () => {
        if (!file) {
            alert("Por favor selecciona un archivo primero");
            return;
        }

        setLoading(true);
        try {
            const formData = new FormData();
            formData.append("file", file);

            const uploadRes = await fetch("http://localhost:8000/lda/upload", {
                method: "POST",
                body: formData,
            });

            if (!uploadRes.ok) {
                throw new Error("Error al subir el archivo");
            }

            const alphaParam = alpha ? `&alpha=${alpha}` : "";
            const trainRes = await fetch(
                `http://localhost:8000/lda/train?K=${K}&iterations=${iterations}${alphaParam}&beta=${beta}`
            );

            if (!trainRes.ok) {
                throw new Error("Error al entrenar el modelo");
            }

            const trainData = await trainRes.json();

            const infoRes = await fetch("http://localhost:8000/lda/info");
            const infoData = await infoRes.json();

            setModelInfo(infoData);
            alert(`Modelo entrenado exitosamente!\n${trainData.message}`);
        } catch (err) {
            console.error(err);
            alert(`Error: ${err.message}`);
        } finally {
            setLoading(false);
        }
    };

    const viewAllTopics = async () => {
        if (!modelInfo) {
            alert("Primero debes entrenar el modelo");
            return;
        }

        try {
            const res = await fetch("http://localhost:8000/lda/topics?top_n=15");
            const data = await res.json();
            setAllTopics(data);
            setViewMode("all-topics");
            setShowChart({});
        } catch (err) {
            alert(`Error: ${err.message}`);
        }
    };

    const viewTopicDetails = async () => {
        if (!modelInfo) {
            alert("Primero debes entrenar el modelo");
            return;
        }

        try {
            const res = await fetch(`http://localhost:8000/lda/topic/${selectedIdTopic}?top_n=20`);
            const data = await res.json();
            setTopicData(data);
            setViewMode("topic");
            setShowChart({});
        } catch (err) {
            alert(`Error: ${err.message}`);
        }
    };

    const viewDocumentDetails = async () => {
        if (!modelInfo) {
            alert("Primero debes entrenar el modelo");
            return;
        }

        try {
            const res = await fetch(`http://localhost:8000/lda/document/${selectedIdDoc}`);
            const data = await res.json();
            setDocumentData(data);
            setViewMode("document");
            setShowChart({});
        } catch (err) {
            alert(`Error: ${err.message}`);
        }
    };

    const viewAllDocuments = async () => {
        if (!modelInfo) {
            alert("Primero debes entrenar el modelo");
            return;
        }

        try {
            const res = await fetch("http://localhost:8000/lda/documents/summary?limit=50");
            const data = await res.json();
            setAllDocuments(data);
            setViewMode("all-documents");
            setShowChart({});
        } catch (err) {
            alert(`Error: ${err.message}`);
        }
    };

    const viewMatrixTheta = async () => {
        if (!modelInfo) {
            alert("Primero debes entrenar el modelo");
            return;
        }

        try {
            const res = await fetch("http://localhost:8000/lda/matrices/theta?limit=100");
            const data = await res.json();
            setMatrixTheta(data);
            setViewMode("theta");
        } catch (err) {
            alert(`Error: ${err.message}`);
        }
    };

    const viewMatrixPhi = async () => {
        if (!modelInfo) {
            alert("Primero debes entrenar el modelo");
            return;
        }

        try {
            const res = await fetch("http://localhost:8000/lda/matrices/phi?limit_words=50");
            const data = await res.json();
            setMatrixPhi(data);
            setViewMode("phi");
        } catch (err) {
            alert(`Error: ${err.message}`);
        }
    };

    const toggleChart = (id) => {
        setShowChart(prev => ({
            ...prev,
            [id]: !prev[id]
        }));
    };

    const renderContent = () => {
        if (!viewMode) {
            return (
                <div className="flex items-center justify-center h-full">
                    <p className="text-xl text-gray-500">
                        {modelInfo 
                            ? "Selecciona una opción para visualizar los resultados..."
                            : "Carga un archivo y entrena el modelo para comenzar..."
                        }
                    </p>
                </div>
            );
        }

        switch (viewMode) {
            case "all-topics":
                return (
                    <div className="h-full overflow-y-auto">
                        <h3 className="text-2xl font-bold mb-4">Todos los Tópicos</h3>
                        {allTopics?.topics.map((topic) => (
                            <div key={topic.topic_id} className="mb-6 p-4 bg-white rounded shadow relative">
                                <div className="flex justify-between items-center mb-2">
                                    <h4 className="text-xl font-semibold text-blue-600">
                                        Tópico {topic.topic_id}
                                    </h4>
                                    <button
                                        onClick={() => toggleChart(`topic-${topic.topic_id}`)}
                                        className="bg-indigo-500 text-white px-3 py-1 rounded text-sm hover:bg-indigo-600"
                                    >
                                        {showChart[`topic-${topic.topic_id}`] ? "Ver Tabla" : "Ver Gráfica"}
                                    </button>
                                </div>
                                
                                {showChart[`topic-${topic.topic_id}`] ? (
                                    <div className="h-96">
                                        <DistributionChart 
                                            type="lda-topic-words"
                                            data={{
                                                words: topic.words.map(w => w.word),
                                                probabilities: topic.words.map(w => w.probability)
                                            }}
                                        />
                                    </div>
                                ) : (
                                    <div className="grid grid-cols-2 gap-2">
                                        {topic.words.map((word, idx) => (
                                            <div key={idx} className="flex justify-between text-sm">
                                                <span className="font-medium">{word.word}</span>
                                                <span className="text-gray-600">{word.percentage}%</span>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                );

            case "topic":
                return (
                    <div className="h-full overflow-y-auto">
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="text-2xl font-bold">
                                Tópico {topicData?.topic_id}
                            </h3>
                            <button
                                onClick={() => toggleChart('single-topic')}
                                className="bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600"
                            >
                                {showChart['single-topic'] ? "Ver Tabla" : "Ver Gráfica"}
                            </button>
                        </div>

                        {showChart['single-topic'] ? (
                            <div className="h-[500px]">
                                <DistributionChart 
                                    type="lda-topic-words"
                                    data={{
                                        words: topicData.words.map(w => w.word),
                                        probabilities: topicData.words.map(w => w.probability)
                                    }}
                                />
                            </div>
                        ) : (
                            <div className="space-y-2">
                                {topicData?.words.map((word) => (
                                    <div key={word.rank} className="flex justify-between p-2 bg-white rounded">
                                        <span className="font-medium">
                                            {word.rank}. {word.word}
                                        </span>
                                        <div className="flex items-center gap-4">
                                            <span className="text-gray-600">{word.percentage}%</span>
                                            <div className="w-32 bg-gray-200 rounded-full h-2">
                                                <div
                                                    className="bg-blue-500 h-2 rounded-full"
                                                    style={{ width: `${word.percentage * 10}%` }}
                                                />
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                );

            case "document":
                return (
                    <div className="h-full overflow-y-auto">
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="text-2xl font-bold">
                                Documento {documentData?.doc_id}
                            </h3>
                            <button
                                onClick={() => toggleChart('single-document')}
                                className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
                            >
                                {showChart['single-document'] ? "Ver Tabla" : "Ver Gráfica"}
                            </button>
                        </div>

                        <div className="mb-4 p-4 bg-blue-50 rounded">
                            <p className="font-semibold">
                                Tópico Dominante: Tópico {documentData?.dominant_topic}
                            </p>
                            <p className="text-gray-700">
                                Probabilidad: {(documentData?.dominant_probability * 100).toFixed(2)}%
                            </p>
                        </div>

                        {showChart['single-document'] ? (
                            <div className="h-[400px]">
                                <DistributionChart 
                                    type="lda-document-topics"
                                    data={{
                                        topics: documentData.topics.map(t => `Tópico ${t.topic_id}`),
                                        probabilities: documentData.topics.map(t => t.probability)
                                    }}
                                />
                            </div>
                        ) : (
                            <div className="space-y-3">
                                {documentData?.topics.map((topic) => (
                                    <div key={topic.topic_id} className="p-3 bg-white rounded shadow">
                                        <div className="flex justify-between items-center mb-2">
                                            <span className="font-medium">Tópico {topic.topic_id}</span>
                                            <span className="text-gray-600">{topic.percentage}%</span>
                                        </div>
                                        <div className="w-full bg-gray-200 rounded-full h-3">
                                            <div
                                                className="bg-green-500 h-3 rounded-full"
                                                style={{ width: `${topic.percentage}%` }}
                                            />
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                );

            case "all-documents":
                return (
                    <div className="h-full overflow-y-auto">
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="text-2xl font-bold">
                                Resumen de Documentos ({allDocuments?.showing} de {allDocuments?.num_docs})
                            </h3>
                            <button
                                onClick={() => toggleChart('all-documents')}
                                className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
                            >
                                {showChart['all-documents'] ? "Ver Lista" : "Ver Gráfica"}
                            </button>
                        </div>

                        {showChart['all-documents'] ? (
                            <div className="h-[500px]">
                                <DistributionChart 
                                    type="lda-documents-distribution"
                                    data={{
                                        documents: allDocuments.documents.map(d => `Doc ${d.doc_id}`),
                                        dominant_topics: allDocuments.documents.map(d => d.dominant_topic),
                                        probabilities: allDocuments.documents.map(d => d.dominant_probability)
                                    }}
                                />
                            </div>
                        ) : (
                            <div className="space-y-3">
                                {allDocuments?.documents.map((doc) => (
                                    <div key={doc.doc_id} className="p-3 bg-white rounded shadow">
                                        <div className="flex justify-between items-center mb-2">
                                            <span className="font-semibold">Documento {doc.doc_id}</span>
                                            <span className="text-sm text-gray-600">
                                                Dominante: Tópico {doc.dominant_topic} ({(doc.dominant_probability * 100).toFixed(1)}%)
                                            </span>
                                        </div>
                                        <div className="flex gap-2 text-sm">
                                            {doc.top_topics.map((topic, idx) => (
                                                <span key={idx} className="bg-blue-100 px-2 py-1 rounded">
                                                    T{topic.topic_id}: {topic.percentage}%
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                );

            case "theta":
                return (
                    <div className="h-full overflow-y-auto">
                        <h3 className="text-2xl font-bold mb-4">
                            Matriz THETA (Documentos × Tópicos)
                        </h3>
                        <p className="text-sm text-gray-600 mb-4">
                            {matrixTheta?.dimensions.documents} documentos × {matrixTheta?.dimensions.topics} tópicos
                            (mostrando {matrixTheta?.dimensions.showing})
                        </p>
                        <div className="overflow-x-auto">
                            <table className="min-w-full bg-white border text-sm">
                                <thead className="bg-gray-100">
                                    <tr>
                                        <th className="border p-2">Doc</th>
                                        {Array.from({ length: modelInfo.K }).map((_, i) => (
                                            <th key={i} className="border p-2">T{i}</th>
                                        ))}
                                    </tr>
                                </thead>
                                <tbody>
                                    {matrixTheta?.matrix.map((row) => (
                                        <tr key={row.doc_id}>
                                            <td className="border p-2 font-medium">{row.doc_id}</td>
                                            {row.distribution.map((val, idx) => (
                                                <td
                                                    key={idx}
                                                    className="border p-2 text-center"
                                                    style={{
                                                        backgroundColor: `rgba(59, 130, 246, ${val})`
                                                    }}
                                                >
                                                    {val.toFixed(4)}
                                                </td>
                                            ))}
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                );

            case "phi":
                return (
                    <div className="h-full overflow-y-auto">
                        <h3 className="text-2xl font-bold mb-4">
                            Matriz PHI (Tópicos × Palabras)
                        </h3>
                        <p className="text-sm text-gray-600 mb-4">
                            {matrixPhi?.dimensions.topics} tópicos × {matrixPhi?.dimensions.vocab_size} palabras
                            (mostrando top {matrixPhi?.dimensions.showing_words} por tópico)
                        </p>
                        {matrixPhi?.matrix.map((topic) => (
                            <div key={topic.topic_id} className="mb-6 p-4 bg-white rounded shadow">
                                <h4 className="text-lg font-semibold mb-3 text-purple-600">
                                    Tópico {topic.topic_id}
                                </h4>
                                <div className="grid grid-cols-3 gap-2 text-sm">
                                    {topic.top_words.map((word, idx) => (
                                        <div key={idx} className="flex justify-between">
                                            <span className="font-medium">{word.word}</span>
                                            <span className="text-gray-600">{word.probability.toFixed(5)}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                );

            default:
                return null;
        }
    };

    return (
        <div className="flex flex-col items-center min-h-screen bg-gray-50">
            <Header
                distributionName={"LDA - Latent Dirichlet Allocation"}
                formula={"p(\\mathbf{w}, \\mathbf{z}, \\theta, \\phi | \\alpha, \\beta) = \\prod_{k=1}^{K} p(\\phi_k | \\beta) \\prod_{d=1}^{D} p(\\theta_d | \\alpha) \\prod_{n=1}^{N_d} p(z_{d,n} | \\theta_d) p(w_{d,n} | \\phi_{z_{d,n}})"}
            />

            <div className="w-[95vw] h-fit m-4 bg-white shadow-lg rounded-lg p-6 grid grid-cols-3 gap-4">
                {/* Panel izquierdo */}
                <div className="col-span-1 flex flex-col gap-4">
                    {/* Panel 1: Cargar archivo */}
                    <div className="bg-gray-100 p-4 rounded shadow">
                        <h3 className="font-bold text-lg mb-3">1. Cargar Corpus</h3>
                        <input
                            type="file"
                            accept=".txt"
                            onChange={handleFileChange}
                            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                        />
                        {file && <p className="text-sm text-green-600 mt-2">✓ {file.name}</p>}
                    </div>

                    {/* Panel 2: Parámetros */}
                    <div className="bg-gray-100 p-4 rounded shadow">
                        <h3 className="font-bold text-lg mb-3">2. Parámetros del Modelo</h3>
                        <div className="space-y-3">
                            <div>
                                <label className="block text-sm font-medium mb-1">
                                    Número de Tópicos (K)
                                </label>
                                <input
                                    type="number"
                                    min="2"
                                    value={K}
                                    onChange={(e) => setK(Number(e.target.value))}
                                    className="w-full border px-3 py-2 rounded"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium mb-1">
                                    Iteraciones
                                </label>
                                <input
                                    type="number"
                                    min="50"
                                    step="50"
                                    value={iterations}
                                    onChange={(e) => setIterations(Number(e.target.value))}
                                    className="w-full border px-3 py-2 rounded"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium mb-1">
                                    Alpha (opcional, default: 50/K)
                                </label>
                                <input
                                    type="number"
                                    step="0.01"
                                    value={alpha}
                                    onChange={(e) => setAlpha(e.target.value)}
                                    placeholder="Auto"
                                    className="w-full border px-3 py-2 rounded"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium mb-1">
                                    Beta
                                </label>
                                <input
                                    type="number"
                                    step="0.001"
                                    value={beta}
                                    onChange={(e) => setBeta(Number(e.target.value))}
                                    className="w-full border px-3 py-2 rounded"
                                />
                            </div>
                        </div>
                        <button
                            onClick={uploadAndTrain}
                            disabled={loading || !file}
                            className="w-full mt-4 bg-blue-600 text-white font-semibold py-2 px-4 rounded hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
                        >
                            {loading ? "Entrenando..." : "Entrenar Modelo"}
                        </button>
                    </div>

                    {/* Panel 3: Info del modelo */}
                    {modelInfo && (
                        <div className="bg-green-50 p-4 rounded shadow">
                            <h3 className="font-bold text-lg mb-2">✓ Modelo Cargado</h3>
                            <div className="text-sm space-y-1">
                                <p><strong>Documentos:</strong> {modelInfo.num_docs}</p>
                                <p><strong>Vocabulario:</strong> {modelInfo.vocab_size}</p>
                                <p><strong>Tópicos (K):</strong> {modelInfo.K}</p>
                                <p><strong>Entropía promedio:</strong> {modelInfo.avg_entropy}</p>
                            </div>
                        </div>
                    )}

                    {/* Panel 4: Visualización de tópicos */}
                    {modelInfo && (
                        <div className="bg-gray-100 p-4 rounded shadow">
                            <h3 className="font-bold text-lg mb-3">Ver Tópicos</h3>
                            <button
                                onClick={viewAllTopics}
                                className="w-full bg-purple-600 text-white py-2 px-4 rounded hover:bg-purple-700 mb-2"
                            >
                                Todos los Tópicos
                            </button>
                            <div className="flex gap-2">
                                <input
                                    type="number"
                                    min="0"
                                    max={modelInfo.K - 1}
                                    value={selectedIdTopic}
                                    onChange={(e) => setSelectedIdTopic(Number(e.target.value))}
                                    className="flex-1 border px-3 py-2 rounded"
                                    placeholder="ID"
                                />
                                <button
                                    onClick={viewTopicDetails}
                                    className="bg-indigo-600 text-white py-2 px-4 rounded hover:bg-indigo-700"
                                >
                                    Ver Tópico
                                </button>
                            </div>
                        </div>
                    )}

                    {/* Panel 5: Visualización de documentos */}
                    {modelInfo && (
                        <div className="bg-gray-100 p-4 rounded shadow">
                            <h3 className="font-bold text-lg mb-3">Ver Documentos</h3>
                            <button
                                onClick={viewAllDocuments}
                                className="w-full bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700 mb-2"
                            >
                                Todos los Documentos
                            </button>
                            <div className="flex gap-2">
                                <input
                                    type="number"
                                    min="0"
                                    max={modelInfo.num_docs - 1}
                                    value={selectedIdDoc}
                                    onChange={(e) => setSelectedIdDoc(Number(e.target.value))}
                                    className="flex-1 border px-3 py-2 rounded"
                                    placeholder="ID"
                                />
                                <button
                                    onClick={viewDocumentDetails}
                                    className="bg-teal-600 text-white py-2 px-4 rounded hover:bg-teal-700"
                                >
                                    Ver Doc
                                </button>
                            </div>
                        </div>
                    )}

                    {/* Panel 6: Matrices */}
                    {modelInfo && (
                        <div className="bg-gray-100 p-4 rounded shadow">
                            <h3 className="font-bold text-lg mb-3">Ver Matrices</h3>
                            <button
                                onClick={viewMatrixTheta}
                                className="w-full bg-orange-600 text-white py-2 px-4 rounded hover:bg-orange-700 mb-2"
                            >
                                Docs × Tópicos
                            </button>
                            <button
                                onClick={viewMatrixPhi}
                                className="w-full bg-pink-600 text-white py-2 px-4 rounded hover:bg-pink-700"
                            >
                                Tópicos × Palabras
                            </button>
                        </div>
                    )}
                </div>

                {/* Panel derecho: Visualización */}
                <div className="col-span-2 bg-gray-100 p-4 rounded shadow overflow-hidden">
                    {renderContent()}
                </div>
            </div>
        </div>
    );
}