import {styled, Switch} from "@mui/material";


const Switcher = styled(Switch)({
    '& .MuiSwitch-switchBase.Mui-checked': {
        color: '#3f51b4',
    },

    '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
        backgroundColor: '#3f51b4',
    }
});

export default Switcher;