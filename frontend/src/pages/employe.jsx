import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  consulterProduits,
  acheterProduits,
  verifierStock,
  consulterStockCentral,
  consulterProduitsParMagasin,
  reapprovisionnerMagasin
} from '../api/employe';
import Header from '../components/header';

const Employe = () => {
  const navigate = useNavigate();
  
  useEffect(() => {
    const role = localStorage.getItem('role');
    if (role !== 'employe') {
      navigate(`/${role}`);
    }
  }, [navigate]);

  const [output, setOutput] = useState(' ');

  const afficherProduits = async () => {
    const produits = await consulterProduits();
    if (produits.length > 0) {
      setOutput(
        produits.map(p => `${p.id} - ${p.name} (${p.category}) : ${p.price}$`).join('\n')
      );
    } else {
      setOutput("Aucun produit disponible.");
    }
  };

  const acheter = async () => {
    const magasinId = prompt("ID du magasin :");
    const input = prompt("Produits à acheter (ex: 1-2,3-1 pour acheter 2x id=1, 1x id=3)");
    const liste = input.split(',').map(pair => {
      const [id, q] = pair.split('-');
      return { produit_id: parseInt(id.trim(), 10), quantite: parseInt(q.trim(), 10) };
    });

    const result = await acheterProduits(parseInt(magasinId), liste);
    if (result?.resultats) {
      setOutput(result.resultats.join('\n'));
    } else {
      setOutput("Erreur ou aucun achat effectué.");
    }
  };

  const verifierStockProduit = async () => {
    const produitId = prompt("ID du produit :");
    const magasinId = prompt("ID du magasin :");
    const stock = await verifierStock(parseInt(produitId), parseInt(magasinId));
    if (stock?.quantite !== undefined) {
      setOutput(`${stock.produit} (${stock.magasin}) : ${stock.quantite} en stock`);
    } else {
      setOutput(stock?.message || "Stock introuvable.");
    }
  };

  const afficherStockParMagasin = async () => {
    const magasinId = prompt("ID du magasin :");
    const result = await consulterProduitsParMagasin(parseInt(magasinId));
    if (Array.isArray(result)) {
      setOutput(result.map(p => `${p.produit} : ${p.quantite}`).join('\n'));
    } else {
      setOutput(result.message || "Erreur.");
    }
  };

  const afficherStockCentral = async () => {
    const data = await consulterStockCentral();
    if (Array.isArray(data)) {
      setOutput(data.map(p => `${p.id} - ${p.name} (${p.category}) : ${p.stock_central} en stock central`).join('\n'));
    } else {
      setOutput("Erreur lors de la récupération du stock central.");
    }
  };

  const envoyerDemandeReapprovisionnement = async () => {
    const produitId = prompt("ID du produit :");
    const quantite = prompt("Quantité demandée :");
    const magasinId = prompt("ID du magasin :");
    const res = await reapprovisionnerMagasin(produitId, quantite, magasinId);
    setOutput(res?.message || "Demande effectuée.");
  };
  
  return (
    <>
    <Header />
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">Espace Employé</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
        <button onClick={afficherProduits} className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-3 rounded shadow">
          Afficher tous les produits
        </button>
        <button onClick={acheter} className="bg-green-600 hover:bg-green-700 text-white px-4 py-3 rounded shadow">
          Acheter des produits
        </button>
        <button onClick={verifierStockProduit} className="bg-yellow-400 hover:bg-yellow-500 text-black px-4 py-3 rounded shadow">
          Vérifier le stock d’un produit
        </button>
        <button onClick={afficherStockParMagasin} className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-3 rounded shadow">
          Stock par magasin
        </button>
        <button onClick={afficherStockCentral} className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-3 rounded shadow">
          Voir le stock central
        </button>
        <button onClick={envoyerDemandeReapprovisionnement} className="bg-red-600 hover:bg-red-700 text-white px-4 py-3 rounded shadow">
          Demander un réapprovisionnement
        </button>
      </div>

      <pre className="bg-gray-100 p-4 rounded shadow whitespace-pre-wrap min-h-[150px]">
        {output}
      </pre>
    </div>
    </>
  );
};

export default Employe;
