import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  consulterStockCentral,
  mettreAJourProduit,
  getDemandesReapprovisionnement,
  approuverReapprovisionnement,
  refuserReapprovisionnement,
  supprimerReapprovisionnement,
  getProduitsParMagasin,
  getAlertesRupture
} from '../api/responsable';
import Header from '../components/header';

const Responsable = () => {
  const [stockCentral, setStockCentral] = useState([]);
  const [demandes, setDemandes] = useState([]);
  const [alertes, setAlertes] = useState([]);
  const [produitsMagasin, setProduitsMagasin] = useState([]);
  const [magasinId, setMagasinId] = useState('');
  const navigate = useNavigate();
  useEffect(() => {
    const role = localStorage.getItem('role');
    if (role !== 'responsable') {
      navigate(`/${role}`);
    }
  }, [navigate]);

  const chargerDonnees = async () => {
    const stock = await consulterStockCentral();
    const reappros = await getDemandesReapprovisionnement();
    const alertesRupture = await getAlertesRupture();
    setStockCentral(stock);
    setDemandes(reappros);
    setAlertes(alertesRupture);
  };

  const handleUpdate = async (produitId) => {
    const champ = prompt("Champ à modifier (name, price, etc.)");
    const valeur = prompt("Nouvelle valeur :");
    if (!champ || !valeur) return;
    const result = await mettreAJourProduit(produitId, champ, valeur);
    alert(result.message);
    chargerDonnees();
  };

  const handleProduitsMagasin = async () => {
    if (!magasinId) return;
    const produits = await getProduitsParMagasin(magasinId);
    setProduitsMagasin(produits);
  };

  useEffect(() => {
    chargerDonnees();
  }, []);

  return (
    <>
    <Header />
    <div className="p-6 space-y-8">
      <h1 className="text-3xl font-bold">Espace Responsable</h1>

      <section>
        <h2 className="text-xl font-semibold mb-2">Stock Central</h2>
        <ul className="bg-gray-100 p-4 rounded">
          {stockCentral.map(p => (
            <li key={p.id} className="mb-2 flex justify-between">
              <span>{p.name} - Stock: {p.stock_central}</span>
              <button className="bg-blue-500 text-white px-3 py-1 rounded" onClick={() => handleUpdate(p.id)}>
                Modifier
              </button>
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2 className="text-xl font-semibold mb-2">Demandes de Réapprovisionnement</h2>
        <ul className="bg-gray-100 p-4 rounded">
          {demandes.map(d => (
            <li key={d.id} className="mb-2">
              {d.produit} pour {d.magasin} - {d.quantite} unités - Approuvé : {d.approuved ? '✅' : '❌'}
              <div className="space-x-2 mt-1">
                {!d.approuved && (
                  <>
                    <button onClick={() => approuverReapprovisionnement(d.id).then(chargerDonnees)} className="bg-green-500 text-white px-2 py-1 rounded">Approuver</button>
                    <button onClick={() => refuserReapprovisionnement(d.id).then(chargerDonnees)} className="bg-yellow-500 text-black px-2 py-1 rounded">Refuser</button>
                  </>
                )}
                <button onClick={() => supprimerReapprovisionnement(d.id).then(chargerDonnees)} className="bg-red-500 text-white px-2 py-1 rounded">Supprimer</button>
              </div>
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2 className="text-xl font-semibold mb-2">Produits par Magasin</h2>
        <div className="flex space-x-2 mb-2">
          <input
            type="number"
            placeholder="ID du magasin"
            value={magasinId}
            onChange={e => setMagasinId(e.target.value)}
            className="border px-2 py-1 rounded"
          />
          <button onClick={handleProduitsMagasin} className="bg-blue-600 text-white px-4 py-1 rounded">
            Voir
          </button>
        </div>
        <ul className="bg-gray-100 p-4 rounded">
          {produitsMagasin.map(p => (
            <li key={p.produit_id}>{p.nom} : {p.quantite} en stock</li>
          ))}
        </ul>
      </section>

      <section>
        <h2 className="text-xl font-semibold mb-2">Alertes de Rupture</h2>
        <ul className="bg-red-100 p-4 rounded">
          {alertes.map(a => (
            <li key={a.id}>
              {a.produit} : seuil {a.seuil} - à surveiller
            </li>
          ))}
        </ul>
      </section>
    </div>
    </>
  );
};

export default Responsable;