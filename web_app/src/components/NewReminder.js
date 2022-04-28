import React, {useEffect, useState} from 'react';
import ReminderSettings from "./ReminderSettings";
import RepeatSettings from "./RepeatSettings";
import SButton from "./UI/SButton";
import {FormControl} from "@mui/material";


const useValidation = (value, validations) => {
    const [isEmpty, setEmptyError] = useState(false)
    const [isInvalidDate, setInvalidDateError] = useState(false)
    const [isNotNum, setIsNotNumError] = useState(false)
    const [inputValid, setInputValid] = useState(false)

    useEffect(() => {
        for (const validation in validations) {
            switch (validation) {
                case 'isEmpty':
                    value ? setEmptyError(false) : setEmptyError(true);
                    break;
                case 'isInvalidDate':
                    value !== "Invalid Date" ? setInvalidDateError(false) : setInvalidDateError(true);
                    break;
                case 'isNotNum':
                    const reNum = /^\d*$/;
                    reNum.test(String(value)) ? setIsNotNumError(false) : setIsNotNumError(true);
                    break;
            }
        }
    }, [value])

    useEffect(() => {
        if (isEmpty || isInvalidDate || isNotNum)
            setInputValid(false)
        else
            setInputValid(true)
    }, [isEmpty, isInvalidDate, isNotNum])

    return {
        isEmpty,
        isInvalidDate,
        isNotNum,
        inputValid
    }
}


const useInput = (initialValue, validations) => {
    const [value, setValue] = useState(initialValue)
    const [isDirty, setDirty] = useState(false)
    const valid = useValidation(value, validations)

    const onChange = (e) => {
        setValue(e)
    }

    const onChangeButton = (e) => {
        if (e) {
            setValue(e)
        }
    }

    const onBlur = (e) => {
        setDirty(true)
    }

    return {
        value,
        onChange,
        onChangeButton,
        onBlur,
        isDirty,
        ...valid
    }
}

function NewReminder() {
    const date = useInput(new Date(), {'isInvalidDate': true});
    let minDate = new Date().setDate(date.value.getDate() + 1)
    const text = useInput("", {'isEmpty': true})
    const repeat = useInput(false)
    const range = useInput('day');
    const type = useInput('count');
    const count = useInput('', {'isEmpty': true, 'isNotNum': true})
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
            <SButton
                disabled={!text.inputValid || !date.inputValid || (repeat.value ? !(type.value === "count" ? inf.value || count.inputValid : untilDate.inputValid) : false)}
                style={{marginTop: "10px"}} variant="contained">Create Reminder</SButton>
        </FormControl>
    );
};

export default NewReminder;
