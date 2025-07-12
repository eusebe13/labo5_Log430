import axios from 'axios';

const BASE_URL = import.meta.env.VITE_DOCKER_API_URL || 'http://localhost:8000/api/v1';

// Obtenir un rapport consolidé des ventes
export const getRapportConsolide = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/gestionnaire/rapports/consolide`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération du rapport consolidé :", error.response?.data || error);
    return null;
  }
};

// Tableau de bord des performances des magasins
export const getDashboard = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/gestionnaire/dashboard`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération du tableau de bord :", error.response?.data || error);
    return null;
  }
};

// Voir tous les rapports de tendance existants
export const getRapports = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/gestionnaire/rapports`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des rapports :", error.response?.data || error);
    return [];
  }
};

// Générer un rapport pour une région
export const creerRapportPourRegion = async (region) => {
  try {
    const response = await axios.post(`${BASE_URL}/gestionnaire/rapports`, { region });
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la création du rapport :", error.response?.data || error);
    return null;
  }
};
