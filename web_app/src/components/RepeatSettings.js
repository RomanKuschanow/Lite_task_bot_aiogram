import React from 'react';
import Switcher from "./UI/Switcher";
import Filter1Icon from '@mui/icons-material/Filter1';
import AvTimerIcon from '@mui/icons-material/AvTimer';
import AllInclusiveIcon from '@mui/icons-material/AllInclusive';
import {FormControlLabel, IconButton, InputAdornment, MenuItem, ToggleButtonGroup, Typography} from "@mui/material";
import TextBox from "./UI/TextBox";
import TButton from "./UI/TButton";
import {KeyboardDatePicker, MuiPickersUtilsProvider} from "@material-ui/pickers";
import DateFnsUtils from "@date-io/date-fns";
import {I18nProvider} from '../i18nProvider'
import translate from "../i18nProvider/translate";

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

function RepeatSettings({repeat, range, type, inf, count, untilDate, minDate, isVip, locale, ...props}) {

    const handleClickInf = () => {
        inf.onChange(!inf.value)
    };

    return (
        <I18nProvider locale={locale}>
            <div className={!isVip ? "notVip repeat" : "repeat"}>
                <div className="repeat_part" style={{marginBottom: "10px"}}>
                    <FormControlLabel
                        onChange={(e) => repeat.onChange(e.target.checked)}
                        value={repeat.value}
                        style={{marginLeft: "0", maxHeight: "56px"}}
                        control={<Switcher/>}
                        disabled={!isVip}
                        label={<Typography
                            style={{lineHeight: "0.7", color: "var(--tg-theme-text-color)"}}>Repeat</Typography>}
                        labelPlacement="top"/>
                    <TextBox
                        style={{width: "100px", marginRight: "10px"}}
                        select
                        onChange={(e) => range.onChange(e.target.value)}
                        value={range.value}
                        label={translate('range')}
                        disabled={!repeat.value}
                        className={!repeat.value && isVip ? "disabled" : ""}
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
                        className={!repeat.value && isVip ? "disabled" : ""}
                        value={type.value}
                        onChange={(e, value) => type.onChangeButton(value)}
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
                    <TextBox
                        style={{width: "100%"}}
                        label={translate('count')}
                        value={inf.value ? "Infinity" : count.value}
                        onChange={(e) => count.onChangeNum(e.target.value)}
                        onBlur={(e) => count.onBlur(e)}
                        error={count.isDirty && (count.isEmpty || count.isNotNum)}
                        disabled={!repeat.value}
                        className={!repeat.value && isVip ? "disabled" : ""}
                        InputProps={{
                            readOnly: inf.value,
                            endAdornment:
                                <InputAdornment position="end">
                                    <IconButton className={inf.value ? "inf" : ""}
                                                onClick={handleClickInf}
                                                disabled={!repeat.value}>
                                        <AllInclusiveIcon/>
                                    </IconButton>
                                </InputAdornment>,
                        }}
                        helperText={count.isEmpty && !inf.value && repeat.value ? "Field cannot be empty" : ""}
                    />
                </div>
                <div className={type.value === "until" ? "repeat_part" : ""} hidden>
                    <MuiPickersUtilsProvider utils={DateFnsUtils}>
                        <KeyboardDatePicker style={{width: "100%"}}
                                            label={translate('until')}
                                            value={untilDate.value}
                                            minDate={minDate}
                                            ampm={false}
                                            inputVariant="outlined"
                                            onChange={(e) => untilDate.onChange(e)}
                                            format="yyyy.MM.dd"
                                            showTodayButton
                                            disabled={!repeat.value}
                                            className={!repeat.value && isVip ? "disabled" : ""}
                        />
                    </MuiPickersUtilsProvider>
                </div>
            </div>
        </I18nProvider>
    );
};

export default RepeatSettings;