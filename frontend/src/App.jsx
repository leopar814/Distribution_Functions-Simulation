import { Routes, Route } from "react-router-dom";
import MainMenu from "./pages/MainMenu";
import Layout from "./components/Layout";
import BernoulliSimulation from "./pages/distributions/BernoulliSimulation";
import BinomialSimulation from "./pages/distributions/BinomialSimulation";
import ExponentialSimulation from "./pages/distributions/ExponentialSimulation";
import NormalSimulation from "./pages/distributions/NormalSimulation";
import BivariadaSimulation from "./pages/distributions/BivariadaSimulation";
import MultinomialSimulation from "./pages/distributions/MultinomialSimulation";
import GibbsSimulation from "./pages/distributions/GibbsSimulation";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<MainMenu />} />
      <Route element={<Layout />}> 
        <Route path="/bernoulli" element={<BernoulliSimulation />} />
        <Route path="/binomial" element={<BinomialSimulation />} />
        <Route path="/exponential" element={<ExponentialSimulation />} />
        <Route path="/normal" element={<NormalSimulation />} />
        <Route path="/bivariada" element={<BivariadaSimulation />} />
        <Route path="/multinomial" element={<MultinomialSimulation />} />
        <Route path="/gibbs" element={<GibbsSimulation />} />
        {/* Más rutas aquí  */}
        <Route path="*" element={<div>Página no encontrada</div>} />
      </Route>
    </Routes>
  );
}