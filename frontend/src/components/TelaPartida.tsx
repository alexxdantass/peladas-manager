import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Container,
  Stack,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  DialogActions,
  Alert,
  List,
  ListItem,
  ListItemText,
  Divider
} from '@mui/material';
import {
  PlayArrow,
  Pause,
  Stop,
  Add as AddIcon,
  Timer,
  Sports,
  SwapHoriz
} from '@mui/icons-material';

const API_BASE_URL = 'http://localhost:8000/api';

interface TelaPartidaProps {
  partidaId: number;
}

interface Partida {
  id: number;
  nome: string;
  nome_time_a: string;
  nome_time_b: string;
  horario_previsto: string;
  horario_inicio: string | null;
  horario_fim: string | null;
  status: string;
  gols_time_a: number;
  gols_time_b: number;
  observacoes: string | null;
  pelada_id: number;
}

interface Gol {
  id: number;
  jogador_nome: string;
  time: string;
  minuto: number;
}

interface Jogador {
  id: number;
  nome: string;
}

export default function TelaPartida({ partidaId }: TelaPartidaProps) {
  const [partida, setPartida] = useState<Partida | null>(null);
  const [gols, setGols] = useState<Gol[]>([]);
  const [jogadores, setJogadores] = useState<Jogador[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Estados do cronômetro
  const [tempoAtual, setTempoAtual] = useState(0);
  const [cronometroAtivo, setCronometroAtivo] = useState(false);
  
  // Estados dos dialogs
  const [dialogGolAberto, setDialogGolAberto] = useState(false);
  const [timeGol, setTimeGol] = useState<'A' | 'B'>('A');
  const [jogadorSelecionado, setJogadorSelecionado] = useState('');

  // Carregar dados da partida
  useEffect(() => {
    carregarDadosPartida();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [partidaId]);

  // Atualizar cronômetro
  useEffect(() => {
    let intervalo: NodeJS.Timeout;
    
    if (cronometroAtivo) {
      intervalo = setInterval(() => {
        setTempoAtual(tempo => tempo + 1);
      }, 1000);
    }
    
    return () => {
      if (intervalo) clearInterval(intervalo);
    };
  }, [cronometroAtivo]);

  const carregarDadosPartida = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${API_BASE_URL}/partidas/${partidaId}/detalhada`);
      
      if (!response.ok) {
        throw new Error(`Erro ao carregar dados da partida: ${response.status}`);
      }
      
      const dados = await response.json();
      console.log('Dados recebidos da API:', dados); // Debug
      
      if (!dados.partida) {
        throw new Error('Dados da partida não encontrados na resposta');
      }
      
      setPartida(dados.partida);
      setGols(dados.gols || []);
      setJogadores(dados.jogadores || []);
      
      // Calcular tempo atual baseado no horário de início
      let tempoCalculado = 0;
      if (dados.partida.horario_inicio) {
        const inicio = new Date(dados.partida.horario_inicio);
        const agora = new Date();
        tempoCalculado = Math.floor((agora.getTime() - inicio.getTime()) / 1000);
      }
      setTempoAtual(tempoCalculado);
      
      // Partida está ativa se tiver horário de início mas não de fim
      const estaAtiva = dados.partida.horario_inicio && !dados.partida.horario_fim;
      setCronometroAtivo(estaAtiva || false);
      
    } catch (err) {
      console.error('Erro ao carregar dados:', err);
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
    } finally {
      setLoading(false);
    }
  };

  const controlarCronometro = async (acao: 'play' | 'pause' | 'reset') => {
    try {
      const response = await fetch(`${API_BASE_URL}/partidas/${partidaId}/cronometro`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ acao }),
      });

      if (!response.ok) {
        throw new Error('Erro ao controlar cronômetro');
      }

      if (acao === 'play') {
        setCronometroAtivo(true);
      } else if (acao === 'pause') {
        setCronometroAtivo(false);
      } else if (acao === 'reset') {
        setCronometroAtivo(false);
        setTempoAtual(0);
      }
      
      // Recarregar dados da partida para atualizar o status na tela
      await carregarDadosPartida();
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao controlar cronômetro');
    }
  };

  const marcarGol = async () => {
    if (!jogadorSelecionado) {
      setError('Selecione um jogador para marcar o gol');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/partidas/${partidaId}/gol-rapido`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          jogador_id: parseInt(jogadorSelecionado),
          time: timeGol,
        }),
      });

      if (!response.ok) {
        throw new Error('Erro ao marcar gol');
      }

      // Recarregar dados
      await carregarDadosPartida();
      
      // Fechar dialog
      setDialogGolAberto(false);
      setJogadorSelecionado('');
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao marcar gol');
    }
  };

  const formatarTempo = (segundos: number): string => {
    const minutos = Math.floor(segundos / 60);
    const segs = segundos % 60;
    return `${minutos.toString().padStart(2, '0')}:${segs.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return (
      <Container>
        <Typography>Carregando partida...</Typography>
      </Container>
    );
  }

  if (error) {
    return (
      <Container>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  if (!partida) {
    return (
      <Container>
        <Alert severity="warning">Partida não encontrada</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 3 }}>
        {/* Header da Partida */}
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h4" gutterBottom>
              {partida.nome_time_a} vs {partida.nome_time_b}
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Data: {new Date(partida.horario_previsto).toLocaleDateString('pt-BR')} | 
              Status: <Chip label={partida.status} color="secondary" />
            </Typography>
          </CardContent>
        </Card>

        <Stack spacing={3}>
          {/* Placar */}
          <Card>
            <CardContent>
              <Typography variant="h3" align="center" gutterBottom>
                {partida.nome_time_a} <span style={{ color: '#1976d2' }}>{partida.gols_time_a}</span>
                {' x '}
                <span style={{ color: '#d32f2f' }}>{partida.gols_time_b}</span> {partida.nome_time_b}
              </Typography>
              
              {/* Cronômetro */}
              <Box display="flex" justifyContent="center" alignItems="center" mt={2}>
                <Timer sx={{ mr: 1 }} />
                <Typography variant="h5" sx={{ mr: 2 }}>
                  {formatarTempo(tempoAtual)}
                </Typography>
                
                <IconButton 
                  onClick={() => controlarCronometro(cronometroAtivo ? 'pause' : 'play')}
                  color="primary"
                  size="large"
                >
                  {cronometroAtivo ? <Pause /> : <PlayArrow />}
                </IconButton>
                
                <IconButton 
                  onClick={() => controlarCronometro('reset')}
                  color="secondary"
                  size="large"
                >
                  <Stop />
                </IconButton>
              </Box>
            </CardContent>
          </Card>

          {/* Ações Rápidas */}
          <Stack direction={{ xs: 'column', md: 'row' }} spacing={3}>
            <Card sx={{ flex: 1 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  <Sports sx={{ mr: 1 }} />
                  Ações Rápidas
                </Typography>
                
                <Stack spacing={2}>
                  <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => {
                      setTimeGol('A');
                      setDialogGolAberto(true);
                    }}
                    fullWidth
                  >
                    Gol Time A ({partida.nome_time_a})
                  </Button>
                  
                  <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => {
                      setTimeGol('B');
                      setDialogGolAberto(true);
                    }}
                    fullWidth
                  >
                    Gol Time B ({partida.nome_time_b})
                  </Button>
                  
                  <Button
                    variant="outlined"
                    startIcon={<SwapHoriz />}
                    fullWidth
                    onClick={() => {
                      alert('Funcionalidade de substituição em desenvolvimento');
                    }}
                  >
                    Substituição
                  </Button>
                </Stack>
              </CardContent>
            </Card>

            {/* Lista de Gols */}
            <Card sx={{ flex: 1 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Gols da Partida
                </Typography>
                
                {gols.length === 0 ? (
                  <Typography variant="body2" color="text.secondary">
                    Nenhum gol marcado ainda
                  </Typography>
                ) : (
                  <List dense>
                    {gols.map((gol, index) => (
                      <React.Fragment key={gol.id}>
                        <ListItem>
                          <ListItemText
                            primary={`${gol.jogador_nome} (Time ${gol.time})`}
                            secondary={`${gol.minuto}'`}
                          />
                        </ListItem>
                        {index < gols.length - 1 && <Divider />}
                      </React.Fragment>
                    ))}
                  </List>
                )}
              </CardContent>
            </Card>
          </Stack>
        </Stack>

        {/* Dialog para marcar gol */}
        <Dialog open={dialogGolAberto} onClose={() => setDialogGolAberto(false)} maxWidth="sm" fullWidth>
          <DialogTitle>
            Marcar Gol - Time {timeGol} ({timeGol === 'A' ? partida.nome_time_a : partida.nome_time_b})
          </DialogTitle>
          <DialogContent>
            <TextField
              select
              label="Jogador"
              value={jogadorSelecionado}
              onChange={(e) => setJogadorSelecionado(e.target.value)}
              fullWidth
              margin="normal"
            >
              {jogadores.map((jogador) => (
                <option key={jogador.id} value={jogador.id}>
                  {jogador.nome}
                </option>
              ))}
            </TextField>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setDialogGolAberto(false)}>
              Cancelar
            </Button>
            <Button onClick={marcarGol} variant="contained">
              Marcar Gol
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </Container>
  );
}
