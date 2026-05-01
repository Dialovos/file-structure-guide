// Shared ESLint config consumed by every workspace via:
//   "extends": ["@my-monorepo/eslint-config"]
// Keep rules conservative; let individual packages add stricter rules
// in their own .eslintrc as needed.

module.exports = {
  root: false,
  env: {
    browser: true,
    node: true,
    es2022: true,
  },
  extends: ["eslint:recommended"],
  parserOptions: {
    ecmaVersion: 2022,
    sourceType: "module",
  },
  rules: {
    "no-unused-vars": ["warn", { argsIgnorePattern: "^_" }],
  },
  ignorePatterns: ["dist/", ".next/", "node_modules/"],
};
