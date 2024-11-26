import React from "react";
import DateSuiInput, { DatePropsBaseUncontrolled } from "@splunk/react-ui/Date";

function DateInput(props: { onChange: DatePropsBaseUncontrolled["onChange"] }) {
  const today = new Date().toISOString().split("T")[0];

  return <DateSuiInput defaultValue={today} onChange={props.onChange} />;
}

export default DateInput;
