import React, {useEffect, useState} from 'react';
import ReminderSettings from "./ReminderSettings";
import RepeatSettings from "./RepeatSettings";
import SButton from "./UI/SButton";
import {FormControl, ThemeProvider} from "@mui/material";
import {theme} from "./UI/Theme";


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

    const onChangeNum = (e) => {
        setValue(e.replace(/\D/g, ''))
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
        onChangeNum,
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
    const inf = useInput(true)
    const [isVip, changeVip] = useState(false)

    let disable = !text.inputValid || !date.inputValid || (repeat.value ? !(type.value === "count" ? inf.value || count.inputValid : untilDate.inputValid) : false);

    const repeatSettings = {repeat, range, type, count, untilDate, inf, minDate, isVip}

    const getStatus = () => {
        fetch('https://litetask.ml/api/getStatus', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                '_auth': window.Telegram.WebApp.initData,
            }),
            redirect: 'follow'
        })
            .then(response => response.json())
            // .then(result => console.log(result))
            .then(result => changeVip(result.isVip))
            .catch(error => console.log('error', error))
    }

    const createReminder = () => {
        window.Telegram.WebApp.MainButton.showProgress();

        fetch('https://litetask.ml/api/NewReminder', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                '_auth': window.Telegram.WebApp.initData,
                'data': window.newReminderData
            }),
            redirect: 'follow'
        })
            .then(response => response.json())
            .then(result => console.log(result))
            .catch(error => console.log('error', error))
            .finally(() => {
                window.Telegram.WebApp.MainButton.hideProgress()
            });
    }

    useEffect(() => {
        getStatus()
        window.Telegram.WebApp.expand()
        window.Telegram.WebApp.MainButton
            .setText('Create Reminder')
            .show()
            .onClick(createReminder)
    }, [])

    if (disable)
        window.Telegram.WebApp.MainButton.disable();
    else
        window.Telegram.WebApp.MainButton.enable();

    window.newReminderData = {
        text: text.value,
        date: date.value,
        repeat: repeat.value,
        range: range.value,
        type: type.value,
        count: count.value,
        untilDate: untilDate.value,
        inf: inf.value
    }
    return (
        <ThemeProvider theme={theme}>
            <FormControl style={{display: "flex", flexDirection: "column", justifyContent: "center"}}>
                <ReminderSettings text={text} date={date}/>
                <div style={{marginTop: "10px", display: "flex", position: "relative", alignItems: "center"}}
                >
                    <p className="text" hidden={isVip}>
                        Unfortunately, developers also need something to eat, so repeating is available only after
                        donation. This can be done by entering the command /donate
                    </p>

                    <RepeatSettings
                        {...repeatSettings}
                    />
                </div>
                {/*<SButton*/}
                {/*    disabled={disable}*/}
                {/*    className={disable ? "disabled" : ""}*/}
                {/*    style={{marginTop: "10px"}} variant="contained" onClick={createReminder}>Create Reminder</SButton>*/}
            </FormControl>
        </ThemeProvider>
    );
}

export default NewReminder;
