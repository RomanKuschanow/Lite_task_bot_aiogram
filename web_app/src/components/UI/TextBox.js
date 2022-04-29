import {styled, TextField} from "@mui/material";

const TextBox = styled(TextField)({
    '& label.Mui-active': {
        color: "var(--tg-theme-text-color)",
    },
    
    '& label.Mui-focused': {
        color: 'var(--tg-theme-button-color)',
    },

    '& .MuiOutlinedInput-root.Mui-active': {
        color: "var(--tg-theme-text-color)",

        '&.Mui-focused fieldset': {
            borderColor: 'var(--tg-theme-button-color)',
        },
    },
});

export default TextBox;