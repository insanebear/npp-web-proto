// FILE: src/App.tsx
import { Routes, Route } from 'react-router-dom';

import BayesianPage from './pages/BayesianPage/BayesianPage';
import StatisticalPage from "./pages/StatisticalPage/StatisticalPage";
import SettingsPage from "./pages/SettingsPage/SettingsPage";
import ReliabilityPage from "./pages/ReliabilityPage/ReliabilityPage";

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