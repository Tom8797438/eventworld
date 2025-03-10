// Protéger les Requêtes API Vue.js avec JWT

import axios from 'axios';
import Cookies from "js-cookie";
import { refreshToken } from './authService';

const instance = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
});

instance.interceptors.request.use((config) => {
    let token = Cookies.get("authToken");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => Promise.reject(error));

// Interceptor : Rafraîchit le token si une requête est rejetée (401 Unauthorized)
instance.interceptors.response.use((response) => response, async (error) => {
    if (error.response && error.response.status === 401) {
        try {
            await refreshToken(); // Essaie de récupérer un nouveau token
            error.config.headers.Authorization = `Bearer ${Cookies.get("authToken")}`;
            return instance(error.config); // Rejoue la requête avec le nouveau token
        } catch (refreshError) {
            return Promise.reject(refreshError);
        }
    }
    return Promise.reject(error);
});

export default instance;
