const js = require("@eslint/js");
const globals = require("globals");

// Globals dipasang pada `window` oleh main.js (window.X = ...) & dirujuk
// bogel (tanpa "window.") dari fail sama/lain — arkitektur sedia ada
// zymnotes ialah <script> biasa (bukan ES modules), bukan bug.
const windowAttachedGlobals = {
  ZymStore: "readonly",
  ZymSettings: "readonly",
  HzMindmap: "readonly",
  HzSparkleRebindNoteAudio: "readonly",
  HzZhMode: "readonly",
  __HZ_CHIP_FLIP_LOGS__: "readonly",
  __labStartQuiz: "readonly",
  hzApplyTheme: "readonly",
  hzPreparePaperAccordions: "readonly",
};

module.exports = [
  js.configs.recommended,
  { ignores: ["node_modules/**"] },
  {
    // Fail konfigurasi root (eslint.config.js, stylelint.config.js, dll.) — CommonJS Node
    files: ["*.config.js"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "commonjs",
      globals: { ...globals.node },
    },
  },
  {
    files: ["assets/js/**/*.js"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "script",
      globals: {
        ...globals.browser,
        ...windowAttachedGlobals,
        gtag: "readonly", // Google Analytics (gtag.js, dimuat via <script> di HTML)
      },
    },
    rules: {
      "no-unused-vars": ["warn", { args: "none", varsIgnorePattern: "^_" }],
      "no-empty": ["error", { allowEmptyCatch: true }],
    },
  },
  {
    files: ["sw.js"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "script",
      globals: { ...globals.serviceworker },
    },
  },
  {
    files: ["scripts/**/*.mjs"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module",
      globals: { ...globals.node },
    },
    rules: {
      "no-unused-vars": ["warn", { args: "none", varsIgnorePattern: "^_" }],
    },
  },
  {
    files: ["scripts/**/*.js"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "commonjs",
      globals: { ...globals.node },
    },
    rules: {
      "no-unused-vars": ["warn", { args: "none", varsIgnorePattern: "^_" }],
    },
  },
];
