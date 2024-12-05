import React from "react";
import { fireEvent, render } from "@testing-library/react";
import { userEvent } from "@testing-library/user-event";
import DateInput from "./DateInput";

describe("DateInput", () => {
  it("renders with default value and handles date change", async () => {
    const handleChange = jest.fn();
    const user = userEvent.setup();

    const { getByRole } = render(<DateInput onChange={handleChange} />);

    const input = getByRole("combobox");
    expect(input).toBeVisible();

    const newDate = "12/1/2000";

    await user.clear(input);
    await user.type(input, newDate, { skipClick: true });
    // a weird implementation of Date component, it does not work with user.keyboard('[Enter]')
    fireEvent.keyDown(input, { key: "enter", keyCode: 13 });

    expect(input).toHaveValue(newDate);
    expect(handleChange).toHaveBeenCalled();
  });
});
