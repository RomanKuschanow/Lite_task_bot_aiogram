import {styled, Switch} from "@mui/material";


const Switcher = styled(Switch)({
    '& .MuiSwitch-switchBase.Mui-checked': {
        color: 'var(--tg-theme-button-color)',
    },

    '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
        backgroundColor: 'var(--tg-theme-button-color)',
    }
});

export default Switcher;