import MuiToggleButton from "@mui/material/ToggleButton";
import { styled } from "@mui/material/styles";

const TButton = styled(MuiToggleButton)({
    "&.Mui-selected, &.Mui-selected:hover, &.Mui-active": {
        backgroundColor: 'var(--tg-theme-button-color)',
        color: "var(--tg-theme-button-text-color)"
    },
});

export default TButton;