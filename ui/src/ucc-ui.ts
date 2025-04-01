import { init } from "@splunk/add-on-ucc-framework";
import DateInput from "./ucc-ui-extensions/DateInput/DateInput";

init(DateInput).catch((error) => {
  console.error("Could not load UCC", error);
});
