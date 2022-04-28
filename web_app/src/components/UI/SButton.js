import Button from "@mui/material/Button";
import { styled } from "@mui/material/styles";

const SButton = styled(Button)({
    "&.MuiButton-root": {
        backgroundColor: 'var(--tg-theme-button-color)',
        width: "100%",
        color: 'var(--tg-theme-button-text-color)',
    },

    "&.Mui-disabled": {
        color: 'rgba(0, 0, 0, 0.26)'
    }
});

export default SButton;