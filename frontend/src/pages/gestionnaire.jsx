import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  getRapportConsolide,
  getDashboard,
  getRapports,
  creerRapportPourRegion,
} from "../api/gestionnaire";
import Header from "../components/header";

const Gestionnaire = () => {
  const [rapportConsolide, setRapportConsolide] = useState(null);
  const [dashboard, setDashboard] = useState(null);
  const [rapports, setRapports] = useState([]);
  const [region, setRegion] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  // Chargement initial des données
  useEffect(() => {
    fetchRapportConsolide();
    fetchDashboard();
    fetchRapports();
  }, []);

  
  
  useEffect(() => {
    const role = localStorage.getItem('role');
    if (role !== 'gestionnaire') {
      navigate(`/${role}`);
    }
  }, [navigate]);

  const fetchRapportConsolide = async () => {
    const data = await getRapportConsolide();
    setRapportConsolide(data);
  };

  const fetchDashboard = async () => {
    const data = await getDashboard();
    setDashboard(data);
  };

  const fetchRapports = async () => {
    const data = await getRapports();
    setRapports(data);
  };

  const handleCreerRapport = async () => {
    if (!region.trim()) {
      setMessage("Veuillez saisir une région.");
      return;
    }
    const result = await creerRapportPourRegion(region.trim());
    if (result && result.message) {
      setMessage(result.message);
      setRegion("");
      fetchRapports();
    } else {
      setMessage("Erreur lors de la création du rapport.");
    }
  };

  return (
      <>
      <Header />
    <div className="p-6 max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Espace Gestionnaire</h1>

      {/* Rapport consolidé */}
      <section className="mb-8">
        <h2 className="text-xl font-semibold mb-2">Rapport consolidé des ventes</h2>
        {!rapportConsolide ? (
          <p>Chargement...</p>
        ) : (
          <pre className="bg-gray-100 p-4 rounded max-h-72 overflow-auto whitespace-pre-wrap">
            {JSON.stringify(rapportConsolide, null, 2)}
          </pre>
        )}
      </section>

      {/* Tableau de bord indicateurs */}
      <section className="mb-8">
        <h2 className="text-xl font-semibold mb-2">Indicateurs clés</h2>
        {!dashboard ? (
          <p>Chargement...</p>
        ) : (
          <pre className="bg-gray-100 p-4 rounded max-h-72 overflow-auto whitespace-pre-wrap">
            {JSON.stringify(dashboard, null, 2)}
          </pre>
        )}
      </section>

      {/* Rapports enregistrés */}
      <section className="mb-8">
        <h2 className="text-xl font-semibold mb-2">Rapports enregistrés</h2>
        {rapports.length === 0 ? (
          <p>Aucun rapport trouvé.</p>
        ) : (
          <ul className="list-disc list-inside mb-4">
            {rapports.map((r) => (
              <li key={r.id}>
                Région : <strong>{r.region}</strong> - Total Ventes : {r.total_ventes}
              </li>
            ))}
          </ul>
        )}
        <div className="flex items-center gap-2">
          <input
            type="text"
            placeholder="Nom de la région"
            value={region}
            onChange={(e) => setRegion(e.target.value)}
            className="border rounded px-2 py-1 flex-grow"
          />
          <button
            onClick={handleCreerRapport}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Créer un rapport
          </button>
        </div>
        {message && <p className="mt-2 text-red-600">{message}</p>}
      </section>
    </div>
    </>
  );
};

export default Gestionnaire;
