import React from "react";
import ReactDOM from "react-dom";
import { CustomControlBase } from "../../utils/CustomControl.ts";
import DateInput from "./DateInput";

import { DateChangeHandler } from "@splunk/react-ui/Date";

export default class DateInputClass extends CustomControlBase {
  onDateChange: DateChangeHandler = (_event, data) => {
    this.setValue(data.value);
  };

  render() {
    const dateValue = this.data.value;
    const date =
      typeof dateValue === "string" && dateValue.length !== 0
        ? dateValue
        : undefined;

    ReactDOM.render(
      <DateInput value={date} onChange={this.onDateChange} />,
      this.el,
    );
  }
}
