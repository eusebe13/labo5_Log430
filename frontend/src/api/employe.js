import axios from 'axios';

const BASE_URL = import.meta.env.VITE_DOCKER_API_URL || 'http://localhost:8000/api/v1';

/**
 * Récupère tous les produits disponibles dans tous les magasins.
 */
export const consulterProduits = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/employe/produits`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des produits :", error);
    return [];
  }
};

/**
 * Récupère les produits disponibles dans un magasin spécifique.
 * @param {number} magasinId
 */
export const consulterProduitsParMagasin = async (magasinId) => {
  try {
    const response = await axios.get(`${BASE_URL}/employe/magasin/${magasinId}/produits`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des produits du magasin :", error);
    return [];
  }
};

/**
 * Vérifie le stock d’un produit dans un magasin.
 * @param {number} produitId
 * @param {number} magasinId
 */
export const verifierStock = async (produitId, magasinId) => {
  try {
    const response = await axios.get(`${BASE_URL}/employe/stock/${produitId}/magasin/${magasinId}`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la vérification du stock :", error);
    return null;
  }
};

/**
 * Récupère l’état complet du stock central.
 */
export const consulterStockCentral = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/employe/stockcentral/produits`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la consultation du stock central :", error);
    return [];
  }
};

/**
 * Effectue un achat de plusieurs produits pour un magasin donné.
 * @param {number} magasinId
 * @param {Array<{ produit_id: number, quantite: number }>} produits
 */
export const acheterProduits = async (magasinId, produits) => {
  try {
    const response = await axios.post(`${BASE_URL}/employe/acheter/${magasinId}`, produits);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de l'achat des produits :", error.response?.data || error);
    return null;
  }
};

/**
 * Envoie une demande de réapprovisionnement immédiate pour un magasin.
 * @param {number} produitId
 * @param {number} quantite
 * @param {number} magasinId
 */
export const reapprovisionnerMagasin = async (produitId, quantite, magasinId) => {
  try {
    const response = await axios.post(`${BASE_URL}/employe/reapprovisionner/produit/${produitId}/quantite/${quantite}/magasin/${magasinId}`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la demande de réapprovisionnement :", error.response?.data || error);
    return null;
  }
};
