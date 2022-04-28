import MuiToggleButton from "@mui/material/ToggleButton";
import { styled } from "@mui/material/styles";

const TButton = styled(MuiToggleButton)({
    "&.Mui-selected, &.Mui-selected:hover": {
        backgroundColor: '#3f51b4',
        color: "white"
    },
});

export default TButton;