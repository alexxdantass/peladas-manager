import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { AppBar, Toolbar, Typography } from '@mui/material';
import ListaJogadores from './components/ListaJogadores';

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
        </Toolbar>
      </AppBar>

      {/* Conteúdo principal */}
      <ListaJogadores />
    </ThemeProvider>
  );
}

export default App;
