import React from "react";
import DateSuiInput, { DatePropsBaseUncontrolled } from "@splunk/react-ui/Date";

function DateInput(props: {
  value?: string;
  onChange: DatePropsBaseUncontrolled["onChange"];
}) {
  const today = props.value ?? new Date().toISOString().split("T")[0];

  return <DateSuiInput defaultValue={today} onChange={props.onChange} />;
}

export default DateInput;
