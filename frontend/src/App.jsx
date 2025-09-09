import { Routes, Route } from "react-router-dom";
import MainMenu from "./pages/MainMenu";
import Layout from "./pages/Layout";
import BernoulliSimulation from "./pages/distributions/BernoulliSimulation";
import BinomialSimulation from "./pages/distributions/BinomialSimulation";
import ExponentialSimulation from "./pages/distributions/ExponentialSimulation";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<MainMenu />} />
      <Route element={<Layout />}> 
        <Route path="/bernoulli" element={<BernoulliSimulation />} />
        <Route path="/binomial" element={<BinomialSimulation />} />
        <Route path="/exponential" element={<ExponentialSimulation />} />
        {/* Más rutas aquí  */}
        <Route path="*" element={<div>Página no encontrada</div>} />
      </Route>
    </Routes>
  );
}