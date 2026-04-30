# API specification

Canonical name. No `-v2`, no `-final`, no `-old`. When this spec changes, the
change lives in git history. If you need to reference an older revision, use
`git log` or a tag (`git show v1.2.0:api-spec.md`).

## Endpoints

### `GET /users`

Returns a paginated list of users.

- **Query params**: `limit` (int, default 20), `cursor` (string, optional).
- **Response**: `{ users: User[], next_cursor: string | null }`.

### `POST /users`

Create a new user.

- **Body**: `{ email: string, name: string }`.
- **Response**: `201 Created`, `{ id: string, email: string, name: string }`.

### `GET /users/:id`

Fetch one user by id.

- **Response**: `200 OK` or `404 Not Found`.

## Versioning policy

The API namespace itself is versioned at the URL level (`/v1/users`,
`/v2/users` if a breaking change ever ships). This *spec file* is not. One
`api-spec.md` lives at HEAD; previous shapes live in git history.

## Authentication

All endpoints require a bearer token in the `Authorization` header.

## Rate limits

100 requests per minute per token. `429 Too Many Requests` on overflow.
