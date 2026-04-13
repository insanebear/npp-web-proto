import { Routes, Route } from 'react-router-dom';

import BayesianPage from './features/bayesian/components/BayesianPage';
import StatisticalPage from "./features/statistical/components/StatisticalPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={ <BayesianPage /> } />
      <Route path="/bayesian" element={ <BayesianPage /> } />
      <Route path="/statistical" element={ <StatisticalPage/> } />
    </Routes>
  );
}

export default App;