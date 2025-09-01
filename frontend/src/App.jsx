import { Routes, Route } from "react-router-dom";
import MainMenu from "./pages/MainMenu";
import Layout from "./pages/Layout";
import BernoulliSimulation from "./pages/BernoulliSimulation";
import BinomialSimulation from "./pages/BinomialSimulation";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<MainMenu />} />
      <Route element={<Layout />}> 
        <Route path="/bernoulli" element={<BernoulliSimulation />} />
        <Route path="/binomial" element={<BinomialSimulation />} />
        {/* Más rutas aquí  */}
        <Route path="*" element={<div>Página no encontrada</div>} />
      </Route>
    </Routes>
    // <div>
    //   <Layout/>
    // </div>
  );
}