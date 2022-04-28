import {styled, TextField} from "@mui/material";

const TextBox = styled(TextField)({
    '& label.Mui-focused': {
        color: 'var(--tg-theme-button-color)',
    },

    '& .MuiOutlinedInput-root': {
        '&.Mui-focused fieldset': {
            borderColor: 'var(--tg-theme-button-color)',
        },
    },
});

export default TextBox;