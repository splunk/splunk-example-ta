import React from "react";
import ReactDOM from "react-dom";
import {
  AcceptableFormValueOrNullish,
  ControlData,
  UtilBaseForm,
} from "../../utils/types.ts";
import DateInput from "./DateInput";

import { DateChangeHandler } from "@splunk/react-ui/Date";

type ValueSetter = (newValue: AcceptableFormValueOrNullish) => void;

export default class DateInputClass {
  globalConfig: object;
  el: HTMLElement;
  data: ControlData;
  util: UtilBaseForm;
  setValue: ValueSetter;

  constructor(
    globalConfig: object,
    el: HTMLElement,
    data: ControlData,
    setValue: ValueSetter,
    util: UtilBaseForm,
  ) {
    this.globalConfig = globalConfig;
    this.el = el;
    this.data = data;
    this.util = util;
    this.setValue = setValue;
  }

  onDateChange: DateChangeHandler = (_event, data) => {
    this.setValue(data.value);
  };

  render() {
    ReactDOM.render(<DateInput onChange={this.onDateChange} />, this.el);
  }
}
