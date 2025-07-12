// api/auth.js
import axios from 'axios';

const BASE_URL = import.meta.env.VITE_DOCKER_API_URL // || 'http://localhost:8000/api/v1';

export const login = async (username, password) => {
  try {
    const response = await axios.post(`${BASE_URL}/connexion`, {
      nom: username,
      mot_de_passe: password,
    });

    const { token, nom, role } = response.data;

    // Sauvegarde dans localStorage
    localStorage.setItem('token', token);
    localStorage.setItem('nom', nom);
    localStorage.setItem('role', role);

    return {
      success: true,
      nom,
      role,
      token,
    };
  } catch (error) {
    console.error("Erreur lors de la connexion :", error.response?.data || error);
    return {
      success: false,
      message: error.response?.data?.detail || "Erreur de connexion",
    };
  }
};

export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('nom');
  localStorage.removeItem('role');
};

export const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const getCurrentUser = () => {
  const token = localStorage.getItem('token');
  const nom = localStorage.getItem('nom');
  const role = localStorage.getItem('role');
  if (token && nom && role) {
    return { token, nom, role };
  }
  return null;
};

export const isLoggedIn = () => {
  return !!localStorage.getItem('token');
};
