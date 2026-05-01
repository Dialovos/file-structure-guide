module github.com/example/myrepo/server

go 1.22

require github.com/example/myrepo/core v0.0.0

// See client/go.mod for the full rationale; remove before tagging.
replace github.com/example/myrepo/core => ../core
