import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Alert,
  CircularProgress
} from '@mui/material';
import { Jogador, JogadorCreate, JogadorUpdate } from '../services/api';

// Props = propriedades que o componente recebe do componente pai
interface FormularioJogadorProps {
  open: boolean;                     // Se o modal está aberto
  onClose: () => void;              // Função para fechar o modal
  onSave: (jogador: JogadorCreate | JogadorUpdate) => Promise<void>; // Função para salvar
  jogador?: Jogador;                // Jogador para editar (opcional)
  title: string;                    // Título do modal
}

export default function FormularioJogador({
  open,
  onClose,
  onSave,
  jogador,
  title
}: FormularioJogadorProps) {
  // Estados do formulário
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [posicao, setPosicao] = useState('');
  const [telefone, setTelefone] = useState('');
  const [nivelHabilidade, setNivelHabilidade] = useState(1);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  // Effect: executa quando o jogador prop muda
  useEffect(() => {
    if (jogador) {
      // Se tem jogador, preenche o formulário (modo edição)
      setNome(jogador.nome);
      setEmail(jogador.email);
      setPosicao(jogador.posicao_preferida || '');
      setTelefone(jogador.telefone || '');
      setNivelHabilidade(jogador.nivel_habilidade);
    } else {
      // Se não tem jogador, limpa o formulário (modo criação)
      setNome('');
      setEmail('');
      setPosicao('');
      setTelefone('');
      setNivelHabilidade(1);
    }
    setErro(null);
  }, [jogador]);

  // Função para validar os dados
  const validarDados = (): boolean => {
    if (!nome.trim()) {
      setErro('Nome é obrigatório');
      return false;
    }
    if (nome.trim().length < 2) {
      setErro('Nome deve ter pelo menos 2 caracteres');
      return false;
    }
    if (!email.trim()) {
      setErro('Email é obrigatório');
      return false;
    }
    // Validação básica de email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.trim())) {
      setErro('Email deve ter um formato válido');
      return false;
    }
    return true;
  };

  // Função para lidar com o envio do formulário
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault(); // Previne o comportamento padrão do form
    
    if (!validarDados()) {
      return;
    }

    setLoading(true);
    setErro(null);

    try {
      // Prepara os dados para envio
      const dadosJogador = {
        nome: nome.trim(),
        email: email.trim(),
        posicao_preferida: posicao.trim() || undefined,
        telefone: telefone.trim() || undefined,
        nivel_habilidade: nivelHabilidade
      };

      await onSave(dadosJogador);
      onClose(); // Fecha o modal após salvar
    } catch (error) {
      console.error('Erro ao salvar jogador:', error);
      setErro('Erro ao salvar jogador. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  // Função para limpar e fechar
  const handleClose = () => {
    setNome('');
    setEmail('');
    setPosicao('');
    setTelefone('');
    setNivelHabilidade(1);
    setErro(null);
    onClose();
  };

  return (
    <Dialog 
      open={open} 
      onClose={handleClose}
      maxWidth="sm"
      fullWidth
    >
      <form onSubmit={handleSubmit}>
        <DialogTitle>{title}</DialogTitle>
        
        <DialogContent>
          {erro && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {erro}
            </Alert>
          )}
          
          <TextField
            label="Nome"
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            fullWidth
            required
            disabled={loading}
            helperText="Nome completo do jogador"
            sx={{ mb: 2, mt: 1 }}
          />
          
          <TextField
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            fullWidth
            required
            disabled={loading}
            helperText="Email para contato"
            sx={{ mb: 2 }}
          />
          
          <TextField
            label="Posição Preferida"
            value={posicao}
            onChange={(e) => setPosicao(e.target.value)}
            fullWidth
            disabled={loading}
            helperText="Ex: Atacante, Meio-campo, Zagueiro, Goleiro"
            sx={{ mb: 2 }}
          />
          
          <TextField
            label="Telefone"
            value={telefone}
            onChange={(e) => setTelefone(e.target.value)}
            fullWidth
            disabled={loading}
            helperText="Telefone para contato (opcional)"
            sx={{ mb: 2 }}
          />
          
          <TextField
            label="Nível de Habilidade"
            type="number"
            value={nivelHabilidade}
            onChange={(e) => setNivelHabilidade(Number(e.target.value))}
            fullWidth
            disabled={loading}
            inputProps={{ min: 1, max: 10 }}
            helperText="De 1 (iniciante) a 10 (profissional)"
            sx={{ mb: 2 }}
          />
        </DialogContent>
        
        <DialogActions>
          <Button 
            onClick={handleClose}
            disabled={loading}
          >
            Cancelar
          </Button>
          <Button 
            type="submit"
            variant="contained"
            disabled={loading}
          >
            {loading ? <CircularProgress size={20} /> : 'Salvar'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
