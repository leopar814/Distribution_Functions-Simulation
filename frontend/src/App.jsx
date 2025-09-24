import { Routes, Route } from "react-router-dom";
import MainMenu from "./pages/MainMenu";
import Layout from "./components/Layout";
import BernoulliSimulation from "./pages/distributions/BernoulliSimulation";
import BinomialSimulation from "./pages/distributions/BinomialSimulation";
import ExponentialSimulation from "./pages/distributions/ExponentialSimulation";
import MultinomialSimulation from "./pages/distributions/MultinomialSimulation";
import GebbsSimulation from "./pages/distributions/GebbsSimulation";
import NormalSimulation from "./pages/distributions/NormalSimulation";
import BivariadaSimulation from "./pages/distributions/BivariadaSimulation";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<MainMenu />} />
      <Route element={<Layout />}> 
        <Route path="/bernoulli" element={<BernoulliSimulation />} />
        <Route path="/binomial" element={<BinomialSimulation />} />
        <Route path="/exponential" element={<ExponentialSimulation />} />
        <Route path="/normal" element={<NormalSimulation />} />
        <Route path="/multinomial" element={<MultinomialSimulation />} />
        <Route path="/gebbs" element={<GebbsSimulation />} />
        <Route path="/bivariada" element={<BivariadaSimulation />} />
        {/* Más rutas aquí  */}
        <Route path="*" element={<div>Página no encontrada</div>} />
      </Route>
    </Routes>
  );
}