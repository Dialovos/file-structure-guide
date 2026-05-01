// Package core holds the stable, shared types and functions consumed
// by the sibling modules (client, server). Anything exported here is
// part of core's public API and is governed by core's own version tag
// (e.g. core/v1.4.2).
package core

// Greet returns a friendly greeting addressed to name. It is the
// single example function in the template; replace it with your real
// public API.
func Greet(name string) string {
	if name == "" {
		name = "world"
	}
	return "hello, " + name
}
