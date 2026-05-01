import type { StorybookConfig } from "@storybook/react-vite";

/**
 * Storybook 8 main configuration.
 *
 * Auto-discovery picks up every `*.stories.tsx` co-located with its
 * component — no manual registration needed.
 */
const config: StorybookConfig = {
  framework: "@storybook/react-vite",
  stories: [
    "../src/**/*.stories.@(ts|tsx|mdx)",
  ],
  addons: ["@storybook/addon-essentials"],
  docs: { autodocs: "tag" },
  typescript: {
    reactDocgen: "react-docgen-typescript",
  },
};

export default config;
