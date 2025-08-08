import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { AppBar, Toolbar, Typography, Tabs, Tab, Box } from '@mui/material';
import ListaJogadores from './components/ListaJogadores';
import TelaPartida from './components/TelaPartida';

// Tema do Material-UI (cores, tipografia, etc.)
const theme = createTheme({
  palette: {
    primary: {
      main: '#2e7d32', // Verde escuro
    },
    secondary: {
      main: '#4caf50', // Verde claro
    },
  },
});

function App() {
  const [tabAtual, setTabAtual] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, novoTab: number) => {
    setTabAtual(novoTab);
  };

  return (
    <ThemeProvider theme={theme}>
      {/* CssBaseline = reset CSS global */}
      <CssBaseline />
      
      {/* Barra superior */}
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            ⚽ Peladas Manager
          </Typography>
          <Tabs 
            value={tabAtual} 
            onChange={handleTabChange}
            textColor="inherit"
            indicatorColor="secondary"
            sx={{ ml: 2 }}
          >
            <Tab label="Jogadores" />
            <Tab label="Partida" />
          </Tabs>
        </Toolbar>
      </AppBar>

      {/* Conteúdo principal */}
      <Box sx={{ p: 3 }}>
        {tabAtual === 0 && <ListaJogadores />}
        {tabAtual === 1 && <TelaPartida partidaId={1} />}
      </Box>
    </ThemeProvider>
  );
}

export default App;
