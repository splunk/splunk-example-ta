import React from "react";
import { CustomTabBase } from "../../utils/CustomTab.ts";
import ReactDOM from "react-dom";
import { AdvancedInputsTab } from "./AdvancedInputsTab.tsx";

export default class AdvancedInputsTabClass extends CustomTabBase {
  render(): void {
    ReactDOM.render(<AdvancedInputsTab />, this.el);
  }
}
