package auth

import (
	"errors"
	"testing"
)

func TestAuthenticate_AcceptsNonEmptyUser(t *testing.T) {
	if err := Authenticate("alice"); err != nil {
		t.Fatalf("Authenticate(alice) returned error: %v", err)
	}
}

func TestAuthenticate_RejectsEmptyUser(t *testing.T) {
	if err := Authenticate("   "); !errors.Is(err, ErrInvalidUser) {
		t.Fatalf("Authenticate(blank) = %v; want ErrInvalidUser", err)
	}
}
