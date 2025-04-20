import { init } from "@splunk/add-on-ucc-framework";
import DateInputClass from "./ucc-ui-extensions/DateInput";
import AdvancedInputsTabClass from "./ucc-ui-extensions/AdvancedInputsTab";

init({
  DateInput: {
    component: DateInputClass,
    type: 'control',
  },
  AdvancedInputsTab: {
    component: AdvancedInputsTabClass,
    type: 'tab',
  },
}).catch((error) => {
  console.error("Could not load UCC", error);
});
