// Package client is a minimal example of a public package — code that
// external consumers may import via
// github.com/example/mymodule/pkg/client. Putting public surface under
// pkg/ is one of two common Go conventions; the other is to put it at
// the module root. Pick a side and stay consistent.
package client

// Client is a stub client. Real implementations would carry
// configuration (base URL, auth, timeouts) here.
type Client struct {
	BaseURL string
}

// New returns a Client pointed at the supplied base URL.
func New(baseURL string) *Client {
	return &Client{BaseURL: baseURL}
}

// Greet returns a friendly greeting. Demonstrates a public method on
// the public Client type.
func (c *Client) Greet(name string) string {
	if name == "" {
		name = "world"
	}
	return "hello, " + name
}
