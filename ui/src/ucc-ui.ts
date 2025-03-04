import { init } from "@splunk/add-on-ucc-framework";

init().catch((error) => {
  console.error("Could not load UCC", error);
});
