import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 text-center px-4">
      <h1 className="text-6xl font-bold text-red-600 mb-4">404</h1>
      <h2 className="text-2xl font-semibold mb-2">Page non trouvée</h2>
      <p className="mb-6 text-gray-600">
        La page que vous cherchez n'existe pas ou a été déplacée.
      </p>
      <Link
        to="/"
        className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition"
      >
        Retour à l’accueil
      </Link>
    </div>
  );
};

export default NotFound;
