# Architecture Overview

## Layers

```text
Presentation
  SwiftUI screens, reusable components, view models

Domain
  Profile, walk session, invitation, history, and analytics models

Data
  Supabase repository, location, pedometer, avatar, analytics, and cache services

Core
  Dependency injection, app theme, formatting, localization, error mapping, cache policy
```

## State Ownership

`walk_sessions` is the source of truth for whether a walk is waiting, active, or ended.

`profiles.is_walking_now` is maintained as a public, denormalized field. A database trigger recomputes it when a session changes, so the UI does not rely only on one device successfully sending a final update.

The client uses local state for responsive UI, but reconciles with Supabase after launch, foregrounding, and realtime events.

## Realtime Flow

```text
Pedometer / Location
    -> WalkingViewModel
    -> debounced single-flight progress upload
    -> walk_sessions
    -> Supabase Realtime
    -> both clients update UI
```

## Privacy Rules

- Friend sessions may contribute to shared relationship statistics.
- Random sessions are marked as random and excluded from relationship history.
- A user controls whether their last-walk time is visible to others.
- The public walking badge is derived from active sessions rather than treated as an independent client-only truth.

