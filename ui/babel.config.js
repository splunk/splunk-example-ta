/* eslint-env node */
export default {
  presets: [
    [
      "@splunk/babel-preset",
      {
        runtime: "automatic",
      },
    ],
    "@babel/preset-env",
  ],
};
