// Protéger les Requêtes API Vue.js avec JWT

import axios from 'axios';
import { refreshToken } from './authService';

const instance = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
});

instance.interceptors.request.use(async (config) => {
    let token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => Promise.reject(error));

instance.interceptors.response.use((response) => response, async (error) => {
    if (error.response.status === 401) {
        await refreshToken();
        error.config.headers.Authorization = `Bearer ${localStorage.getItem('access_token')}`;
        return axios(error.config);
    }
    return Promise.reject(error);
});

export default instance;
