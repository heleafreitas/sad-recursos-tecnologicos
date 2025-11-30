import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://helenapi.perronedev.com.br/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const recursosService = {
  listarTodos: async () => {
    const response = await api.get('/recursos');
    return response.data;
  },
};

export const recomendacoesService = {
  gerar: async (respostas) => {
    const response = await api.post('/recomendacoes', respostas);
    return response.data;
  },
};

export const metodologiaService = {
  obter: async () => {
    const response = await api.get('/metodologia');
    return response.data;
  },
};

export default api;