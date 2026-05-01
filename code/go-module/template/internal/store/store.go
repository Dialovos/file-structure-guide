// Package store contains a tiny in-memory key/value store used as a
// stand-in for a real persistence layer. Private to this module.
package store

import "sync"

// Store is a goroutine-safe in-memory key/value store.
type Store struct {
	mu   sync.RWMutex
	data map[string]string
}

// New returns an empty Store.
func New() *Store {
	return &Store{data: make(map[string]string)}
}

// Save stores value under key, overwriting any previous value.
func (s *Store) Save(key, value string) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.data[key] = value
}

// Load returns the value stored under key and whether it was present.
func (s *Store) Load(key string) (string, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	v, ok := s.data[key]
	return v, ok
}
