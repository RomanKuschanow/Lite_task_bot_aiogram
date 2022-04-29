import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
    palette: {
        type: window.Telegram.WebApp.themeParams.text_color === '#ffffff' ? 'dark' : 'light',
    },
});