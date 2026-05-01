// Package client is a thin wrapper around core suitable for
// consumers who want a high-level API. It is its own Go module, so
// it can ship at a different cadence than core.
package client

import "github.com/example/myrepo/core"

// SayHello formats a greeting via core.Greet. The indirection is
// intentional: it demonstrates the cross-module dependency.
func SayHello(name string) string {
	return core.Greet(name)
}
