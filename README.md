# Walk With Me: Daily Walks

> An iOS social walking app for people who want to walk together from different places.

`Walk With Me` pairs two people in a shared walking session, displays steps and distance in near real time, and turns finished walks into a lightweight shared history.

The production repository is private. This case study documents the product decisions, architecture, and selected implementation samples without exposing credentials, production infrastructure, or user data.

## Highlights

- SwiftUI application using MVVM and feature-oriented organization
- Supabase Auth, Postgres, Realtime, Storage, and Edge Functions
- Friend invitations by username and anonymous random walks
- Live step and distance updates with Core Motion and Core Location fallback
- Recovery of walk progress after backgrounding or reopening the app
- Profile history, walking identity, avatars, localization, and privacy controls
- TestFlight distribution and release hardening

## Product Problem

Walking can be more motivating when it feels shared, even when two people are not in the same place. The app focuses on a small ritual: start a walk with a friend, see each other's progress, then keep the result as a shared memory.

## Core Flows

### Invite a walker

1. Search for a person by username.
2. Create an in-app invitation.
3. The invited person accepts or declines from the home screen.
4. Both people enter an active session and see progress updates.

### Random walk

1. A user joins the first available random session or creates a waiting one.
2. The partner remains anonymous.
3. Random sessions do not create relationship history or expose the partner's identity.

### Finish a walk

1. The app flushes the latest local progress.
2. The session becomes `ended`.
3. The backend recomputes public walking state.
4. Both profiles receive an end-of-walk summary and the walk appears in history.

## Architecture

```text
SwiftUI Views
    |
ViewModels (@MainActor)
    |
Repository / Services
    |
Supabase: Auth + Postgres + Realtime + Storage
```

The project is organized around `Core`, `Data`, `Domain`, and `Presentation`, with feature folders inside the presentation layer. More detail: [architecture/overview.md](architecture/overview.md).

## Reliability Work

- Single-flight, debounced progress uploads prevent overlapping writes during live tracking.
- Session recovery uses server-stored progress as a baseline after an app restart.
- Walking status is derived and repaired server-side from session state to avoid stale `Walking now` badges.
- Async location updates verify the active session and user before changing UI state.
- Avatar, profile, history, and invite caches reduce unnecessary network requests while keeping network refresh paths explicit.

## Screens

Screenshots will be added here.

| Home | Active Walk | Profile | Invite |
| --- | --- | --- | --- |
| `assets/home.png` | `assets/active-walk.png` | `assets/profile.png` | `assets/invite.png` |

## Stack

- SwiftUI
- Swift Concurrency and Combine
- MVVM
- Supabase Auth, Postgres, Realtime, Storage, and Edge Functions
- Core Motion (`CMPedometer`)
- Core Location (`CLLocationManager`, `CLGeocoder`)
- UserDefaults and disk-backed caches
- Russian and English localization

## Selected Samples

The `code-samples` directory is reserved for sanitized, standalone samples from the project. No production keys, user records, or Supabase project details are included.

## Privacy and Security

- Credentials and environment configuration are not included in this repository.
- The production app stores only the data needed for the account, sessions, progress, and optional avatar.
- Random walking sessions are designed to remain anonymous in relationship history.

## Status

The app is in active product development and distributed through TestFlight.

