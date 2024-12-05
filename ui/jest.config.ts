import type { Config } from "jest";

export default {
  // Mock
  clearMocks: true,
  restoreMocks: true,
  // env settings
  testEnvironment: "jest-fixed-jsdom",
  setupFilesAfterEnv: ["<rootDir>/tests/jest.setup.ts"],
  // Coverage
  collectCoverage: true,
  collectCoverageFrom: ["src/**/*.{js,jsx,ts,tsx}"],
  coveragePathIgnorePatterns: [
    "/node_modules/",
    /*
         TYPES
         */
    // *.d.ts files
    "\\.d\\.ts$",
    "/types/",
    "\\.types\\.ts$",
  ],
  coverageDirectory: "coverage",
  testEnvironmentOptions: {
    /**
     * @note Opt-out from JSDOM using browser-style resolution
     * for dependencies. This is simply incorrect, as JSDOM is
     * not a browser, and loading browser-oriented bundles in
     * Node.js will break things.
     *
     * Consider migrating to a more modern test runner if you
     * don't want to deal with this.
     */
    customExportConditions: [""],
  },
  errorOnDeprecated: true,
  // moduleNameMapper: {
  //   // Force module uuid to resolve with the CJS entry point, because Jest does not support package.json.exports. See https://github.com/uuidjs/uuid/issues/451
  //   uuid: require.resolve("uuid"),
  //   "\\.(css)$": "<rootDir>/src/mocks/styleMock.js",
  // },
} satisfies Config;
