/**
 * Serviço para comunicação com a API FastAPI
 * É como criar funções para fazer requests.get(), requests.post() no Python
 */

import axios from 'axios';

// URL base da nossa API FastAPI
const API_BASE_URL = 'http://localhost:8000/api';

// Cria uma instância do axios com configurações padrão
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interface TypeScript para Jogador 
// (como Pydantic schema no Python)
export interface Jogador {
  id: number;
  nome: string;
  email: string;
  telefone?: string;
  posicao_preferida?: string;
  nivel_habilidade: number;
  ativo: boolean;
  data_cadastro: string;
}

// Interface para criar jogador (sem id, ativo, data_cadastro)
export interface JogadorCreate {
  nome: string;
  email: string;
  telefone?: string;
  posicao_preferida?: string;
  nivel_habilidade?: number;
}

// Interface para atualizar jogador (todos os campos opcionais)
export interface JogadorUpdate {
  nome?: string;
  email?: string;
  telefone?: string;
  posicao_preferida?: string;
  nivel_habilidade?: number;
}

// Serviços da API - cada função faz uma requisição HTTP
export const jogadorService = {
  // GET /api/jogadores/ - Lista todos os jogadores
  async listarJogadores(): Promise<Jogador[]> {
    const response = await api.get<Jogador[]>('/jogadores/');
    return response.data;
  },

  // POST /api/jogadores/ - Cria novo jogador
  async criarJogador(jogador: JogadorCreate): Promise<Jogador> {
    const response = await api.post<Jogador>('/jogadores/', jogador);
    return response.data;
  },

  // GET /api/jogadores/{id} - Busca jogador por ID
  async obterJogador(id: number): Promise<Jogador> {
    const response = await api.get<Jogador>(`/jogadores/${id}`);
    return response.data;
  },

  // PUT /api/jogadores/{id} - Atualiza jogador
  async atualizarJogador(id: number, jogador: JogadorUpdate): Promise<Jogador> {
    const response = await api.put<Jogador>(`/jogadores/${id}`, jogador);
    return response.data;
  },

  // DELETE /api/jogadores/{id} - Remove jogador (soft delete)
  async removerJogador(id: number): Promise<{ message: string }> {
    const response = await api.delete(`/jogadores/${id}`);
    return response.data;
  },
};
