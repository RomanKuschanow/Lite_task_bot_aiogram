import MuiToggleButton from "@mui/material/ToggleButton";
import {styled} from "@mui/material/styles";

const TButton = styled(MuiToggleButton)({
    "&.MuiToggleButton-root.Mui-selected": {
        backgroundColor: 'var(--tg-theme-button-color)',
        color: "var(--tg-theme-button-text-color)"
    },

    "&.MuiToggleButton-root": {
        color: "var(--tg-theme-hint-color)"
    }
});

export default TButton;