module github.com/example/myrepo/tools

go 1.22

// Dev-time tools. Pinned versions live here so static analysis,
// codegen, and mock generation are reproducible without polluting
// core/client/server's go.sum. Build them via:
//
//   (cd tools && go install honnef.co/go/tools/cmd/staticcheck)
//   (cd tools && go install go.uber.org/mock/mockgen)
require (
	go.uber.org/mock v0.4.0
	honnef.co/go/tools v0.4.7
)
