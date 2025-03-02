import { init } from "@splunk/add-on-ucc-framework";

init()
  .then(() => {
    console.log("It is running1");
  })
  .catch((e) => {
    console.error(e);
  });
