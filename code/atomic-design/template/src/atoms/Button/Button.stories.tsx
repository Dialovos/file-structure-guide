import type { Meta, StoryObj } from "@storybook/react";

import { Button } from "./Button";

/**
 * Storybook 8 (CSF3) stories for the Button atom.
 *
 * Each story is a reproducible visual state. Add new variants here
 * before adding them to the component itself; stories are the spec.
 */
const meta: Meta<typeof Button> = {
  title: "Atoms/Button",
  component: Button,
  args: {
    children: "Click me",
  },
  argTypes: {
    variant: {
      control: { type: "radio" },
      options: ["primary", "secondary", "danger"],
    },
  },
};

export default meta;

type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: { variant: "primary" },
};

export const Secondary: Story = {
  args: { variant: "secondary" },
};

export const Danger: Story = {
  args: { variant: "danger", children: "Delete" },
};
