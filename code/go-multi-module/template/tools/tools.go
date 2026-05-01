//go:build tools

// Package tools pins the development-time tools used across the
// repo. The build tag keeps the imports out of regular builds; the
// blank imports are enough to satisfy `go mod tidy` so the tool
// versions persist in go.sum.
//
// To install a tool, cd into this directory and run:
//
//   go install honnef.co/go/tools/cmd/staticcheck
//   go install go.uber.org/mock/mockgen
package tools

import (
	_ "go.uber.org/mock/mockgen"
	_ "honnef.co/go/tools/cmd/staticcheck"
)
