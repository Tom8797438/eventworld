//Connection du Frontend Vue.js à l’API Django

import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/token/';

export async function login(username, password) {
    const response = await axios.post(API_URL, { username, password });
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    return response.data;
}

export async function refreshToken() {
    const response = await axios.post(`${API_URL}refresh/`, {
        refresh: localStorage.getItem('refresh_token'),
    });
    localStorage.setItem('access_token', response.data.access);
}

export function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
}
