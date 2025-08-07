/**
 * Componente para listar jogadores
 * É como criar uma função que retorna HTML
 */

import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  Alert,
  CircularProgress,
  Box,
} from '@mui/material';
import { Add, Edit, Delete } from '@mui/icons-material';
import { jogadorService, Jogador, JogadorCreate, JogadorUpdate } from '../services/api';
import FormularioJogador from './FormularioJogador';

// Componente principal - é como uma função Python que retorna HTML
const ListaJogadores: React.FC = () => {
  // Estados do componente (como variáveis que, quando mudam, atualizam a tela)
  const [jogadores, setJogadores] = useState<Jogador[]>([]); // Lista de jogadores
  const [loading, setLoading] = useState(true); // Se está carregando
  const [error, setError] = useState<string | null>(null); // Se deu erro
  
  // Estados para o formulário
  const [modalAberto, setModalAberto] = useState(false);
  const [jogadorEditando, setJogadorEditando] = useState<Jogador | undefined>(undefined);
  const [tituloModal, setTituloModal] = useState('');

  // useEffect = executa código quando componente "nasce" (como __init__ no Python)
  useEffect(() => {
    carregarJogadores();
  }, []); // [] = executa apenas uma vez

  // Função para carregar jogadores da API
  const carregarJogadores = async () => {
    try {
      setLoading(true); // Mostra loading
      setError(null); // Limpa erros anteriores
      
      // Chama nossa API (como requests.get() no Python)
      const dados = await jogadorService.listarJogadores();
      
      setJogadores(dados); // Salva os dados no estado
    } catch (err) {
      setError('Erro ao carregar jogadores. Verifique se a API está rodando.');
      console.error('Erro:', err);
    } finally {
      setLoading(false); // Para o loading
    }
  };

  // Função para remover jogador
  const removerJogador = async (id: number, nome: string) => {
    // Confirma antes de deletar
    if (window.confirm(`Tem certeza que deseja remover ${nome}?`)) {
      try {
        await jogadorService.removerJogador(id);
        // Recarrega a lista após deletar
        carregarJogadores();
      } catch (err) {
        setError('Erro ao remover jogador');
        console.error('Erro:', err);
      }
    }
  };

  // Funções para controlar o formulário
  const abrirFormularioNovo = () => {
    setJogadorEditando(undefined);
    setTituloModal('Novo Jogador');
    setModalAberto(true);
  };

  const abrirFormularioEdicao = (jogador: Jogador) => {
    setJogadorEditando(jogador);
    setTituloModal('Editar Jogador');
    setModalAberto(true);
  };

  const fecharFormulario = () => {
    setModalAberto(false);
    setJogadorEditando(undefined);
  };

  const salvarJogador = async (dadosJogador: JogadorCreate | JogadorUpdate) => {
    try {
      if (jogadorEditando) {
        // Editando jogador existente
        await jogadorService.atualizarJogador(jogadorEditando.id, dadosJogador as JogadorUpdate);
      } else {
        // Criando novo jogador
        await jogadorService.criarJogador(dadosJogador as JogadorCreate);
      }
      
      // Recarrega a lista após salvar
      await carregarJogadores();
    } catch (err) {
      console.error('Erro ao salvar jogador:', err);
      throw err; // Re-throw para o formulário mostrar o erro
    }
  };

  // Formatação da data (converte ISO string para formato brasileiro)
  const formatarData = (dataISO: string) => {
    return new Date(dataISO).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  // JSX = HTML + JavaScript (o que será renderizado na tela)
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Cabeçalho */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Gerenciar Jogadores
        </Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={abrirFormularioNovo}
        >
          Novo Jogador
        </Button>
      </Box>

      {/* Exibe erro se houver */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* Exibe loading */}
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
          <Typography sx={{ ml: 2 }}>Carregando jogadores...</Typography>
        </Box>
      ) : (
        /* Tabela de jogadores */
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Nome</TableCell>
                <TableCell>Email</TableCell>
                <TableCell>Telefone</TableCell>
                <TableCell>Posição</TableCell>
                <TableCell>Nível</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Cadastro</TableCell>
                <TableCell>Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {jogadores.length === 0 ? (
                /* Se não tem jogadores */
                <TableRow>
                  <TableCell colSpan={9} sx={{ textAlign: 'center', py: 4 }}>
                    <Typography variant="body1" color="text.secondary">
                      Nenhum jogador encontrado. Que tal adicionar o primeiro?
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : (
                /* Lista os jogadores */
                jogadores.map((jogador) => (
                  <TableRow key={jogador.id}>
                    <TableCell>{jogador.id}</TableCell>
                    <TableCell>{jogador.nome}</TableCell>
                    <TableCell>{jogador.email}</TableCell>
                    <TableCell>{jogador.telefone || '-'}</TableCell>
                    <TableCell>{jogador.posicao_preferida || '-'}</TableCell>
                    <TableCell>{jogador.nivel_habilidade}/10</TableCell>
                    <TableCell>
                      <Chip
                        label={jogador.ativo ? 'Ativo' : 'Inativo'}
                        color={jogador.ativo ? 'success' : 'default'}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>{formatarData(jogador.data_cadastro)}</TableCell>
                    <TableCell>
                      <IconButton
                        size="small"
                        onClick={() => abrirFormularioEdicao(jogador)}
                      >
                        <Edit />
                      </IconButton>
                      <IconButton
                        size="small"
                        color="error"
                        onClick={() => removerJogador(jogador.id, jogador.nome)}
                      >
                        <Delete />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Formulário Modal */}
      <FormularioJogador
        open={modalAberto}
        onClose={fecharFormulario}
        onSave={salvarJogador}
        jogador={jogadorEditando}
        title={tituloModal}
      />
    </Container>
  );
};

export default ListaJogadores;
