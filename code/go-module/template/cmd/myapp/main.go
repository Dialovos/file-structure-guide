// Command myapp is the example entry point for this module.
//
// It wires together internal/auth and internal/store and prints a
// greeting. Replace with real application logic as you grow.
package main

import (
	"flag"
	"fmt"
	"os"

	"github.com/example/mymodule/internal/auth"
	"github.com/example/mymodule/internal/store"
)

func main() {
	user := flag.String("user", "world", "name of the user to greet")
	flag.Parse()

	if err := auth.Authenticate(*user); err != nil {
		fmt.Fprintf(os.Stderr, "auth failed: %v\n", err)
		os.Exit(1)
	}

	s := store.New()
	s.Save("greeted", *user)

	fmt.Printf("hello, %s\n", *user)
}
