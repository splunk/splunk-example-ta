import React from "react";
import ReactDOM from "react-dom";
import { CustomControlBase } from "@splunk/add-on-ucc-framework";
import { DateChangeHandler } from "@splunk/react-ui/Date";

const CustomDateInput = React.lazy(() => import("./DateInput"));
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
      <React.Suspense fallback={<div></div>}>
        <CustomDateInput value={date} onChange={this.onDateChange} />
      </React.Suspense>,
      this.el
    );
  }
}
