// Package auth contains authentication primitives that are private to
// this module. The Go compiler enforces that nothing outside
// github.com/example/mymodule can import this package.
package auth

import (
	"errors"
	"strings"
)

// ErrInvalidUser is returned when the supplied user identifier is empty
// or malformed.
var ErrInvalidUser = errors.New("auth: invalid user")

// Authenticate is a stub authenticator. Replace with real logic
// (OAuth, JWT, session lookup, etc.) as the project grows.
func Authenticate(user string) error {
	if strings.TrimSpace(user) == "" {
		return ErrInvalidUser
	}
	return nil
}
