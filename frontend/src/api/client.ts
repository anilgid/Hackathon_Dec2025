import axios from 'axios';

// In development, Vite proxys /api to backend. 
// In production, we assume same origin or configured base URL.
const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || '/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const sendMessage = async (message: string) => {
    const response = await api.post('/chat', { message });
    return response.data;
};
