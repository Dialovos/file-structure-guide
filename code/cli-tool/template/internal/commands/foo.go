package commands

import (
	"fmt"

	"github.com/spf13/cobra"
)

// fooCmd is a sample subcommand: `mytool foo`.
//
// Use this file as the template for new subcommands: copy to
// `bar.go`, rename, replace the RunE, register in init().
var fooCmd = &cobra.Command{
	Use:   "foo [name]",
	Short: "Greet someone (sample subcommand)",
	Long:  `foo is a sample subcommand. It prints a greeting to stdout.`,
	Args:  cobra.MaximumNArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		name := "world"
		if len(args) == 1 {
			name = args[0]
		}
		fmt.Fprintf(cmd.OutOrStdout(), "hello, %s\n", name)
		return nil
	},
}

func init() {
	rootCmd.AddCommand(fooCmd)
}
