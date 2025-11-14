// FILE: src/App.tsx
import { Routes, Route } from 'react-router-dom';

import BayesianPage from './features/bayesian/components/BayesianPage';
import StatisticalPage from "./features/statistical/components/StatisticalPage";
import SettingsPage from "./features/settings/components/SettingsPage";
import ReliabilityPage from "./features/reliability/components/ReliabilityPage";

function App() {
  const BayesianPageComponent = <BayesianPage />;
  return (
    <Routes>
      <Route path="/" element={ BayesianPageComponent } />
      <Route path="/bayesian" element={ BayesianPageComponent } />
      <Route path="/statistical" element={ <StatisticalPage/> } />
      <Route path="/settings" element={ <SettingsPage/> } />
      <Route path="/reliability-views/:jobId?" element={ <ReliabilityPage/> } />
    </Routes>
  );
}

export default App;