import { useNavigate } from 'react-router-dom';

const Header = () => {
  const navigate = useNavigate();

  const nom = localStorage.getItem('nom');
  const role = localStorage.getItem('role');

  const isLoggedIn = !!localStorage.getItem('token');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('nom');
    localStorage.removeItem('role');
    navigate('/login'); // Redirige vers page de connexion
  };

  const handleLogin = () => {
    navigate('/login');
  };

  return (
    <header className="flex items-center justify-between bg-gray-800 text-white px-6 py-3 shadow">
      <div className="text-xl font-bold cursor-pointer" onClick={() => navigate('/')}>
        Système POS
      </div>
      <div className="flex items-center space-x-4">
        {isLoggedIn && (
          <>
            <span className="text-sm">{nom} ({role})</span>
            <button
              onClick={handleLogout}
              className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
            >
              Déconnexion
            </button>
          </>
        )}
        {!isLoggedIn && (
          <button
            onClick={handleLogin}
            className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded"
          >
            Connexion
          </button>
        )}
      </div>
    </header>
  );
};

export default Header;
