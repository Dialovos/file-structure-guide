import type { ButtonHTMLAttributes, FC, ReactNode } from "react";

export type ButtonVariant = "primary" | "secondary" | "danger";

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  children: ReactNode;
}

/**
 * Button — atomic primitive.
 *
 * Knows nothing about molecules or organisms. Variants are prop-driven
 * so the same atom serves every level above.
 */
export const Button: FC<ButtonProps> = ({
  variant = "primary",
  children,
  type = "button",
  ...rest
}) => {
  return (
    <button type={type} data-variant={variant} {...rest}>
      {children}
    </button>
  );
};
