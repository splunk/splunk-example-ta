import React from "react";
import ReactDOM from "react-dom";

import { CustomTabBase } from "@splunk/add-on-ucc-framework";

const CustomAdvancedInputsTab = React.lazy(
  () => import("./AdvancedInputsTab.tsx")
);

export default class AdvancedInputsTabClass extends CustomTabBase {
  render(): void {
    ReactDOM.render(
      <React.Suspense fallback={<div></div>}>
        <CustomAdvancedInputsTab />
      </React.Suspense>,
      this.el
    );
  }
}
