package commands

import (
	"fmt"

	"github.com/spf13/cobra"
)

// barCmd is a second sample subcommand: `mytool bar`. It also
// shows how to declare a flag.
var barCmd = &cobra.Command{
	Use:   "bar",
	Short: "Print a counter (sample subcommand with a flag)",
	RunE: func(cmd *cobra.Command, _ []string) error {
		count, err := cmd.Flags().GetInt("count")
		if err != nil {
			return err
		}
		for i := 0; i < count; i++ {
			fmt.Fprintf(cmd.OutOrStdout(), "bar #%d\n", i+1)
		}
		return nil
	},
}

func init() {
	barCmd.Flags().IntP("count", "n", 1, "how many times to print")
	rootCmd.AddCommand(barCmd)
}
