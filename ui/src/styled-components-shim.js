import * as styledComponents from "styled-components/dist/styled-components.browser.esm.js";

// Make sure the default export works as expected
const styled = styledComponents.default;

// Add each property from the original module to the default export
Object.assign(styled, styledComponents);

export default styled;
export * from "styled-components/dist/styled-components.browser.esm.js";
