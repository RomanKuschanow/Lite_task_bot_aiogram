import React, {useEffect, useState} from 'react';
import ReminderSettings from "./ReminderSettings";
import RepeatSettings from "./RepeatSettings";
import SButton from "./UI/SButton";
import {FormControl} from "@mui/material";


const useValidation = (value, validations) => {
    const [isEmpty, setEmptyError] = useState(true)
    const [isValidDate, setValidDateError] = useState(false)

    useEffect(() => {
        for (const validation in validations) {
            switch (validation) {
                case 'isEmpty':
                    value ? setEmptyError(false) : setEmptyError(true)
                    break;
                case 'isValidDate':
                    const re = /^(\d{4}).(\d{2}).(\d{2}) (\d{2}):(\d{2})$/;
                    re.test(String(value)) ? setValidDateError(false) : setValidDateError(true);
                    break;
            }
        }
    }, [value])

    return {
        isEmpty,
        isValidDate
    }
}


const useInput = (initialValue, validations) => {
    const [value, setValue] = useState(initialValue)
    const [isDirty, setDirty] = useState(false)
    const valid = useValidation(value, validations)

    const onChange = (e) => {
        setValue(e.target.value)
    }

    const onBlur = (e) => {
        setDirty(true)
    }

    return {
        value,
        onChange,
        onBlur,
        isDirty,
        ...valid
    }
}

function NewReminder() {
    const date = useInput(new Date(), {'isEmpty': true, 'isValidDate': true});
    let minDate = new Date().setDate(date.value.getDate() + 1)
    const text = useInput("", {'isEmpty': true})
    const repeat = useInput(false)
    const range = useInput('day');
    const type = useInput('count');
    const count = useInput('', {'isEmpty': true})
    const untilDate = useInput(minDate, {'isEmpty': true, 'isValidDate': true});
    const inf = useInput(false)

    const repeatSettings = {repeat, range, type, count, untilDate, inf, minDate}


    return (
        <FormControl style={{display: "flex", flexDirection: "column", justifyContent: "center"}}>
            <ReminderSettings text={text} date={date}/>
            <div style={{marginTop: "10px"}}>
                <RepeatSettings
                    {...repeatSettings}
                />
            </div>
            <SButton style={{marginTop: "10px"}} variant="contained">Create Reminder</SButton>
        </FormControl>
    );
};

export default NewReminder;
