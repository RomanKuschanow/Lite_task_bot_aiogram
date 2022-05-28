import React from 'react';
import {KeyboardDateTimePicker, MuiPickersUtilsProvider} from "@material-ui/pickers";
import DateFnsUtils from "@date-io/date-fns";
import TextBox from "./UI/TextBox";
import {I18nProvider} from '../i18nProvider'
import translate from "../i18nProvider/translate";
import enLocale from "date-fns/locale/en-US";
import ukLocale from "date-fns/locale/uk";
import ruLocale from "date-fns/locale/ru";

const localeMap = {
  en: enLocale,
  fr: ukLocale,
  ru: ruLocale,
};

function ReminderSettings({text, date, locale, ...props}) {
    return (
        <I18nProvider locale={locale}>
            <div align="center">
                <TextBox
                    style={{width: "100%"}}
                    label={translate('reminderText')}
                    multiline
                    maxRows={5}
                    value={text.value}
                    onChange={(e) => text.onChange(e.target.value)}
                    onBlur={(e) => text.onBlur(e)}
                    helperText={text.isDirty && text.isEmpty ? "Field cannot be empty" : ""}
                />
            </div>
            <div align="center" style={{paddingTop: "10px"}}>
                <MuiPickersUtilsProvider utils={DateFnsUtils} locale={localeMap[locale]}>
                    <KeyboardDateTimePicker style={{width: "100%"}}
                                            label={translate('date')}
                                            value={date.value}
                                            ampm={false}
                                            inputVariant="outlined"
                                            onChange={(Date) => date.onChange(Date)}
                                            format="yyyy.MM.dd HH:mm"
                                            showTodayButton
                    />
                </MuiPickersUtilsProvider>
            </div>
        </I18nProvider>
    );
};

export default ReminderSettings;
