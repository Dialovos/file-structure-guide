// Package server hosts an HTTP/gRPC entry point that uses core to
// answer requests. Like client, it is its own module so the binary
// can ship independently of the library.
package server

import "github.com/example/myrepo/core"

// Handle is a stand-in for a real handler. It demonstrates that the
// server module imports core through the standard module path, the
// same way an external consumer would.
func Handle(name string) string {
	return core.Greet(name)
}
