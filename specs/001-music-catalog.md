# Music Catalog — specification

Status: implemented

## Goal

A small web application for cataloguing artists, albums and songs. A user can
create and delete artists, create albums, and maintain the ordered track list
of every album.

## Domain model

- `Artist`: `id`, non-empty `name` (unique, case-insensitive).
- `Album`: `id`, non-empty `title`, `artist`, `release_year` (1900..current year).
- `Song`: `id`, non-empty `title` (unique, case-insensitive).
- `AlbumTrack`: `album`, `song`, `track_number` (> 0).

`AlbumTrack` is an explicit many-to-many association. Therefore the same song
can be included in multiple albums and can have a different track number in
each. An album cannot contain the same song twice, and two songs cannot occupy
the same track number in one album.

## User stories and acceptance criteria

1. The catalogue page lists albums with artist, year and ordered tracks.
2. A user can create an artist; blank and duplicate names are rejected.
3. A user can create an album for an existing artist; invalid years are rejected.
4. A user can add a new or existing song to an album at a free positive track
   number; conflicts are rejected.
5. A user can remove a track or album from the catalogue after confirmation.
6. Loading and API errors are visible and do not destroy the current page state.
7. `GET /api/albums/?search=...` filters by album, artist or song title.

## REST contract

- `GET|POST /api/artists/`, `GET|DELETE /api/artists/{id}/`
- `GET|POST /api/songs/`, `GET|DELETE /api/songs/{id}/`
- `GET|POST /api/albums/`, `GET|DELETE /api/albums/{id}/`
- `POST /api/albums/{id}/tracks/` with `{song_id, track_number}` or
  `{song_title, track_number}`
- `DELETE /api/albums/{id}/tracks/{track_id}/`

Errors use `{field: [messages]}` and standard HTTP status codes.

## Non-functional requirements

- Django ORM and migrations; SQLite for a zero-config demo.
- Vue 3 Composition API, Vite and Pinia.
- Backend and frontend tests run in CI.
- Dependency and static security scans run in CI.
- The local API is rate-limited and responses include browser security headers.
- The complete application starts with `docker compose up --build`.
