import React from 'react';
import {KeyboardDateTimePicker, MuiPickersUtilsProvider} from "@material-ui/pickers";
import DateFnsUtils from "@date-io/date-fns";
import TextBox from "./UI/TextBox";


function ReminderSettings({text, date, ...props}) {
    return (
        <div>
            <div align="center">
                <TextBox
                    style={{width: "100%"}}
                    label="Reminder Text"
                    multiline
                    maxRows={5}
                    value={text.value}
                    onChange={(e) => text.onChange(e)}
                    onBlur={(e) => text.onBlur(e)}
                    error={text.isDirty && text.isEmpty}
                />
            </div>
            <div align="center" style={{paddingTop: "10px"}} >
                <MuiPickersUtilsProvider utils={DateFnsUtils}>
                    <KeyboardDateTimePicker style={{width: "100%"}}
                                            label="Date and Time"
                                            value={date.value}
                                            ampm={false}
                                            inputVariant="outlined"
                                            onChange={(value) => date.onChange({target: {value}})}
                                            format="yyyy.MM.dd HH:mm"
                                            showTodayButton
                    />
                </MuiPickersUtilsProvider>
            </div>
        </div>
    );
};

export default ReminderSettings;
