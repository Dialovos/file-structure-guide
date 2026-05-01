import type { Preview } from "@storybook/react";

/**
 * Global Storybook preview config — runs around every story.
 *
 * Add global decorators (theme provider, router stub, intl provider)
 * here once your component library needs them.
 */
const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
};

export default preview;
