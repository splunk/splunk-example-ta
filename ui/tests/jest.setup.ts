import "@testing-library/jest-dom";
import "@testing-library/jest-dom/jest-globals";

import { configure } from "@testing-library/react";

/**
 * Configure test attributes
 */
configure({ testIdAttribute: "data-test" });

/**
 * Failing tests if there is some console error during tests
 */
export let consoleError: jest.SpyInstance<
  void,
  Parameters<(typeof console)["error"]>
>;

beforeEach(() => {
  const originalConsoleError = console.error;
  consoleError = jest.spyOn(console, "error");
  consoleError.mockImplementation(
    (...args: Parameters<typeof console.error>) => {
      originalConsoleError(...args);
      throw new Error(
        "Console error was called. Call consoleError.mockImplementation(() => {}) if this is expected.",
      );
    },
  );
});
