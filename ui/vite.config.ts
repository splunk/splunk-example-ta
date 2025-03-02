// vite.config.ts
import { defineConfig } from "vite";
import { dirname, join, relative, resolve } from "path";
import { fileURLToPath } from "url";
import { readdirSync, statSync, globSync, unlinkSync } from "fs";
import react from "@vitejs/plugin-react";
import checker from "vite-plugin-checker";
import { viteCommonjs } from "@originjs/vite-plugin-commonjs";
import commonjs from "@rollup/plugin-commonjs";
import styledComponentBabelPlugin from "./styled-component-babel-plugin";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const DEBUG = process.env.NODE_ENV !== "production";

const proxyTargetUrl = "http://localhost:8000";

const jsAssetsRegex = /.+\/app\/.+\/js\/build\/custom(\/.+(js(.map)?))/;

function isItStaticAsset(url: string): boolean {
  return jsAssetsRegex.test(url);
}

const entryDir = join(__dirname, "src/ucc-ui-extensions");

/**
 * It looks for all index files in the given directory.
 * @param {string} dir
 * @return {string[]}
 */
function getAllIndexFiles(dir: string): string[] {
  let results: string[] = [];
  const list = readdirSync(dir);
  list.forEach((file) => {
    const filePath = join(dir, file);
    const stat = statSync(filePath);
    if (stat && stat.isDirectory()) {
      results = results.concat(getAllIndexFiles(filePath));
    } else if (file === "index.ts" || file === "index.tsx") {
      results.push(filePath);
    }
  });
  return results;
}

const entryFiles = getAllIndexFiles(entryDir);

if (entryFiles.length === 0) {
  throw new Error(
    "No entry files found. Make sure the entryDir is correct and there are index files in some directory.",
  );
}

// Create input object for multiple entry points
const input: Record<string, string> = {};

entryFiles.forEach((file) => {
  const entryName = relative(entryDir, dirname(file));
  input[entryName] = file;
});

// Add the UCC UI entry point
input["ucc-ui"] = join(__dirname, "src/ucc-ui.ts");

const TA_NAME = "Splunk_TA_Example";
const outputDir = resolve(
  __dirname,
  "../output",
  TA_NAME,
  "appserver/static/js/build",
);

export default defineConfig({
  optimizeDeps: {
    include: [
      "styled-components",
      "@splunk/react-ui",
      "@splunk/themes",
      "@splunk/react-page",
    ],
    esbuildOptions: {
      resolveExtensions: [".js", ".jsx", ".ts", ".tsx"],
      define: {
        global: "globalThis",
      },
    },
  },
  build: {
    outDir: outputDir,
    sourcemap: false,
    minify: false,
    commonjsOptions: {
      include: /node_modules/,
      transformMixedEsModules: true,
      requireReturnsDefault: "auto",
    },
    rollupOptions: {
      input,
      output: {
        format: "es",
        entryFileNames: (chunkInfo) => {
          if (chunkInfo.name === "ucc-ui") {
            return "entry_page.js";
          }
          return Object.keys(input).includes(chunkInfo.name)
            ? "custom/[name].js"
            : DEBUG
              ? "[name].js"
              : "[name].[hash].js";
        },
        // https://github.com/styled-components/styled-components/issues/3700
        interop: "compat",
      },
    },
  },
  plugins: [
    react({
      babel: {
        plugins: [
          [
            "babel-plugin-styled-components",
            {
              displayName: true,
              ssr: false,
            },
          ],
        ],
      },
    }),
    checker({
      typescript: true,
    }),
    // commonjs({
    //   // include: /node_modules/,
    // }),
    {
      name: "clean-specific-files",
      buildStart: async () => {
        // Use glob to find the specific file types
        const files = globSync([
          `${outputDir}/**/*.js`,
          `${outputDir}/**/*.js.map`,
          `${outputDir}/**/*.txt`,
        ]);

        // Delete each file
        files.forEach((file) => {
          try {
            unlinkSync(file);
          } catch (err) {
            console.error(`Error deleting ${file}:`, err);
          }
        });
      },
    },
    // Custom plugin to handle URL rewriting (equivalent to setupMiddlewares)
    {
      name: "url-rewrite-middleware",
      configureServer(server) {
        server.middlewares.use((req, res, next) => {
          if (req.url && isItStaticAsset(req.url)) {
            req.url = req.url.replace(jsAssetsRegex, "$1");
          }
          next();
        });
      },
    },
  ],
  server: {
    proxy: {
      // Configure proxy based on URL pattern
      "/": {
        target: proxyTargetUrl,
        changeOrigin: true,
        bypass: ({ url }) => {
          // Don't proxy static assets
          if (url && isItStaticAsset(url)) {
            return url;
          }
          return null; // Proxy everything else
        },
      },
    },
  },
  resolve: {
    // alias: {
    //   "styled-components": "src/styled-components-shim.js",
    // },
    extensions: [".tsx", ".ts", ".js"],
  },
  experimental: {
    // building dynamic public path for making assets preload work correctly
    renderBuiltUrl(filename, { type }) {
      if (type === "asset") {
        // it should match with the variable set in base.html
        return {
          runtime: `window.__webpack_public_path__ + ${JSON.stringify("assets/" + filename)}`,
        };
      }
    },
  },
});
