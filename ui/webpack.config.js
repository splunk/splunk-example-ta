import path from "path";

import ForkTsCheckerWebpackPlugin from "fork-ts-checker-webpack-plugin";
import { fileURLToPath } from "node:url";
import { readdirSync, statSync } from "node:fs";
import { dirname, join, relative } from "node:path";
import { invariant } from "es-toolkit";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const proxyTargetUrl = "http://localhost:8000";

const jsAssetsRegex = /.+\/app\/.+\/js\/build\/custom(\/.+(js(.map)?))/;

function isItStaticAsset(url) {
  const isItAsset = jsAssetsRegex.test(url);
  if (isItAsset) {
    const isItCustomJs = url.includes("js/build/custom");
    return !isItCustomJs;
  }
  return isItAsset;
}

const entryDir = join(__dirname, "src/ucc-ui-extensions");

/**
 * It looks for all index files in the given directory.
 * @param {string} dir
 * @return {string[]}
 */
function getAllIndexFiles(dir) {
  /**
   * @type {string[]}
   */
  let results = [];
  const list = readdirSync(dir);
  list.forEach((file) => {
    const filePath = join(dir, file);
    const stat = statSync(filePath);
    if (stat && stat.isDirectory()) {
      results = results.concat(getAllIndexFiles(filePath));
    } else if (file === "index.ts") {
      results.push(filePath);
    }
  });
  return results;
}

const entryFiles = getAllIndexFiles(entryDir);

invariant(
  entryFiles.length > 0,
  "No entry files found. Make sure the entryDir is correct and there are index files in some directory.",
);

/**
 * @param {Record<string, string>} acc - The accumulator object.
 * @param {string} file - The file path.
 * @returns {Record<string, string>} The updated accumulator object.
 */
const entry = entryFiles.reduce((acc, file) => {
  const entryName = relative(entryDir, dirname(file));
  acc[entryName] = file;
  return acc;
}, {});

const TA_NAME = "Splunk_TA_Example";
const outputPath = path.resolve(
  __dirname,
  "../output",
  TA_NAME,
  "appserver/static/js/build/custom",
);

export default {
  entry: entry,
  output: {
    path: outputPath,
    filename: (pathData) =>
      pathData.chunk.name in entry ? "[name].js" : "[name].[contenthash].js",
    chunkFilename: "[name].[contenthash].js",
    library: "[name]",
  },
  module: {
    rules: [
      {
        test: /.tsx?$/,
        use: [
          {
            loader: "babel-loader",
            // options: {
            //   presets: [
            //     "@babel/preset-env",
            //     "@babel/preset-react",
            //     "@babel/preset-typescript",
            //   ],
            // },
          },
        ],
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
  resolve: {
    extensions: [".tsx", ".ts", ".js"],
  },
  plugins: [new ForkTsCheckerWebpackPlugin()],
  devtool: "source-map",
  devServer: {
    hot: false,
    proxy: [
      {
        target: proxyTargetUrl,
        context(pathname) {
          return !isItStaticAsset(pathname);
        },
      },
    ],
    setupMiddlewares: (middlewares, devServer) => {
      devServer.app.use((req, res, next) => {
        if (isItStaticAsset(req.url)) {
          req.url = req.url.replace(jsAssetsRegex, "$1");
        }
        next();
      });

      return middlewares;
    },
  },
};
