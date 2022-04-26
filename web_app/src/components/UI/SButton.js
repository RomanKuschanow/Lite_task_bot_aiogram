import Button from "@mui/material/Button";
import { styled } from "@mui/material/styles";

const SButton = styled(Button)({
    "&.MuiButton-root": {
        backgroundColor: '#3f51b4',
        width: "100%"
    },
});

export default SButton;