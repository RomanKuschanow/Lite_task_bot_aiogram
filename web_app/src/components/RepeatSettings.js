import React from 'react';
import Switcher from "./UI/Switcher";
import Filter1Icon from '@mui/icons-material/Filter1';
import AvTimerIcon from '@mui/icons-material/AvTimer';
import {FormControlLabel, MenuItem, ToggleButtonGroup, Typography} from "@mui/material";
import TextBox from "./UI/TextBox";
import TButton from "./UI/TButton";
import {KeyboardDatePicker, MuiPickersUtilsProvider} from "@material-ui/pickers";
import DateFnsUtils from "@date-io/date-fns";

const ranges = [
    {
        value: 'day',
        label: 'Day',
    },
    {
        value: 'week',
        label: 'Week',
    },
    {
        value: 'month',
        label: 'Month',
    },
    {
        value: 'year',
        label: 'Year',
    },
];

function RepeatSettings({repeat, range, type, inf, count, untilDate, minDate, ...props}) {

    return (
        <div className="repeat">
            <div className="repeat_part" style={{marginBottom: "10px"}}>
                <FormControlLabel
                    onChange={(e) => repeat.onChange(e)}
                    value={repeat.value}
                    style={{marginLeft: "0", maxHeight: "56px"}}
                    control={<Switcher/>}
                    label={<Typography style={{lineHeight: "0.7"}}>Repeat</Typography>}
                    labelPlacement="top"
                />
                <TextBox
                    style={{width: "100px", marginRight: "10px"}}
                    select
                    onChange={(e) => range.onChange(e)}
                    value={range.value}
                    label="Repeat Range"
                    disabled={!repeat.value}
                >
                    {ranges.map((option) => (
                        <MenuItem key={option.value} value={option.value}>
                            {option.label}
                        </MenuItem>
                    ))}
                </TextBox>
                <ToggleButtonGroup
                    exclusive
                    disabled={!repeat.value}
                    value={type.value}
                    onChange={(e) => type.onChange(e)}
                >
                    <TButton value="count">
                        <Filter1Icon/>
                    </TButton>
                    <TButton value="until">
                        <AvTimerIcon/>
                    </TButton>
                </ToggleButtonGroup>
            </div>
            <div className={type.value === "count" ? "repeat_part" : ""} hidden>
                <FormControlLabel
                    onChange={(e) => inf.onChange(e)}
                    value={inf.value}
                    style={{marginLeft: "0", maxHeight: "56px"}}
                    control={<Switcher/>}
                    label={<Typography style={repeat.value ? {
                        lineHeight: "0.7",
                    } : {
                        lineHeight: "0.7",
                        color: "rgba(0, 0, 0, 0.38)"
                    }}>Infinity</Typography>}
                    labelPlacement="top"
                    disabled={!repeat.value}
                />
                <TextBox
                    style={{width: "100%"}}
                    label="Repeat Count"
                    value={count.value}
                    type="number"
                    onChange={(e) => count.onChange(e)}
                    disabled={!repeat.value || inf.value}
                />
            </div>
            <div className={type.value === "until" ? "repeat_part" : ""} hidden>
                <MuiPickersUtilsProvider utils={DateFnsUtils}>
                    <KeyboardDatePicker style={{width: "100%"}}
                                        label="Date until repeat"
                                        value={untilDate.value}
                                        minDate={minDate}
                                        ampm={false}
                                        inputVariant="outlined"
                                        onChange={(e) => untilDate.onChange(e)}
                                        format="yyyy.MM.dd"
                                        showTodayButton
                                        disabled={!repeat.value}
                    />
                </MuiPickersUtilsProvider>
            </div>
        </div>
    );
};

export default RepeatSettings;