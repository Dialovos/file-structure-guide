module github.com/example/myrepo/client

go 1.22

require github.com/example/myrepo/core v0.0.0

// Local development across sibling modules: until core is tagged and
// pushed, point the require above at the working copy on disk.
//
// REMOVE THIS BEFORE PUBLISHING / TAGGING client. A published module
// with an active replace directive is unresolvable for downstream
// consumers. Prefer `go.work` at the repo root for local development
// once you have a stable workflow.
replace github.com/example/myrepo/core => ../core
