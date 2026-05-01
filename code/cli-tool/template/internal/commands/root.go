// Package commands wires up the cobra command tree for `mytool`.
//
// One file per top-level subcommand. Each subcommand registers
// itself with rootCmd in its own init().
package commands

import (
	"github.com/spf13/cobra"
)

// version is overridden at build time via -ldflags.
var version = "0.0.1-dev"

var rootCmd = &cobra.Command{
	Use:   "mytool",
	Short: "mytool — example CLI scaffolded from the cli-tool guideline",
	Long: `mytool is an example single-binary CLI that demonstrates the layout
recommended by code/cli-tool/.

Replace this Long description, the Use string, and the subcommands
under internal/commands/ with your own.`,
	Version:       version,
	SilenceUsage:  true,
	SilenceErrors: true,
}

// Execute is the entry point invoked from cmd/mytool/main.go.
func Execute() error {
	return rootCmd.Execute()
}
