import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api/auth';

const Connexion = () => {
  const [nom, setNom] = useState('');
  const [motDePasse, setMotDePasse] = useState('');
  const [erreur, setErreur] = useState('');
  const navigate = useNavigate();

  const handleConnexion = async (e) => {
    e.preventDefault();
    setErreur('');

    const result = await login(nom, motDePasse);

    if (result.success) {
      switch (result.role) {
        case 'employe':
          navigate('/employe');
          break;
        case 'gestionnaire':
          navigate('/gestionnaire');
          break;
        case 'responsable':
          navigate('/responsable');
          break;
        default:
          setErreur("Rôle inconnu.");
      }
    } else {
      setErreur(result.message || "Échec de la connexion.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="max-w-md w-full bg-white p-8 rounded shadow">
        <h2 className="text-2xl font-bold mb-6 text-center">Connexion</h2>
        <form onSubmit={handleConnexion} className="space-y-4">
          <div>
            <label className="block mb-1 font-medium">Nom d'utilisateur</label>
            <input
              type="text"
              value={nom}
              onChange={(e) => setNom(e.target.value)}
              className="w-full border px-3 py-2 rounded"
              required
            />
          </div>
          <div>
            <label className="block mb-1 font-medium">Mot de passe</label>
            <input
              type="password"
              value={motDePasse}
              onChange={(e) => setMotDePasse(e.target.value)}
              className="w-full border px-3 py-2 rounded"
              required
            />
          </div>
          {erreur && <p className="text-red-500 text-sm">{erreur}</p>}
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
          >
            Se connecter
          </button>
        </form>
      </div>
    </div>
  );
};

export default Connexion;