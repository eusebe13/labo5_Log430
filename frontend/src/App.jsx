import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Connexion from './pages/connexion';
import Employe from './pages/employe';
import Gestionnaire from './pages/gestionnaire';
import Responsable from './pages/responsable';
import NotFound from './pages/notfound';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Connexion />} />
        <Route path="/login" element={<Connexion />} />
        <Route path="/employe" element={<Employe />} />
        <Route path="/gestionnaire" element={<Gestionnaire />} />
        <Route path="/responsable" element={<Responsable />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;
