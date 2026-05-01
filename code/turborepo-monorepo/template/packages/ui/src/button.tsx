// Sample component. JIT-consumed: Next.js apps in apps/ read this TS
// source directly through their own bundler. No build step in this package.

export type ButtonProps = {
  children: React.ReactNode;
  onClick?: () => void;
};

export function Button({ children, onClick }: ButtonProps): JSX.Element {
  return <button onClick={onClick}>{children}</button>;
}
