import React from "react";
import ReactDOM from "react-dom";
import { CustomTabBase } from "@splunk/add-on-ucc-framework";
import { AdvancedInputsTab } from "./AdvancedInputsTab.tsx";

export default class AdvancedInputsTabClass extends CustomTabBase {
  render(): void {
    ReactDOM.render(<AdvancedInputsTab />, this.el);
  }
}
