import {styled, TextField} from "@mui/material";

const TextBox = styled(TextField)({
    '& label.Mui-focused': {
        color: '#3f51b4',
    },

    '& .MuiOutlinedInput-root': {
        '&.Mui-focused fieldset': {
            borderColor: '#3f51b4',
        },
    },
});

export default TextBox;