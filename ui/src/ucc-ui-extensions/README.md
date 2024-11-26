# How to bundle a new UI extension

1. Create a new directory in `ui/src/ucc-ui-extensions` with the name of your extension.
2. Add your extension's files to the directory.
3. Add your default export to the `ui/src/ucc-ui-extensions/index.js` file. This the only file that will be included in the final bundle with all their dependencies.
4. Add the following in your service in globalConfig.json

```json
{
  // ...
  "type": "custom",
  "options": {
    "src": "FolderName",
    "type": "external"
  }
}
```