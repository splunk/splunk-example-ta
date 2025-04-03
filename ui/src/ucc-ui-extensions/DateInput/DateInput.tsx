import React from "react";
import DateSuiInput, { DateChangeHandler } from "@splunk/react-ui/Date";

function DateInput(props: { value?: string; onChange: DateChangeHandler }) {
  const today = props.value ?? new Date().toISOString().split("T")[0];

  return (
    <DateSuiInput
      className="DateSuiInputClasss"
      defaultValue={today}
      onChange={(...data) => console.log("data", data)}
    />
  );
}

export default DateInput;
