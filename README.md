<p align="center">
  <img src="assets/app-icon.jpg" alt="Walk With Me app icon" width="112" style="border-radius: 24px;" />
</p>

<h1 align="center">Walk With Me</h1>

<p align="center">
  <strong>Daily walks feel more motivating when someone is walking with you — even from somewhere else.</strong>
</p>

<p align="center">
  <a href="README.md">English</a>&nbsp;&nbsp;·&nbsp;&nbsp;<a href="README.ru.md">Русский</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/iOS-17%2B-000000?logo=apple&logoColor=white" alt="iOS 17+" />
  <img src="https://img.shields.io/badge/UI-SwiftUI-58A6FF" alt="SwiftUI" />
  <img src="https://img.shields.io/badge/Backend-Supabase-3ECF8E?logo=supabase&logoColor=white" alt="Supabase" />
  <img src="https://img.shields.io/badge/Distribution-TestFlight-0D96F6?logo=apple&logoColor=white" alt="TestFlight" />
</p>

`Walk With Me` is an iOS social walking app for two people who want to share a walk remotely. It pairs walkers in a live session, synchronises steps and distance, and preserves completed walks as a small shared history.

<p align="center">
  <img src="assets/IMG_8628.PNG" alt="Walk With Me home screen" width="250" />
</p>

> The production source repository is private. This public case study shares the product, system design, and selected visuals without credentials, user data, or production infrastructure details.

## The Product

Walking alone is easy to postpone. Walking "together" creates a gentle commitment: invite a person, start when both are ready, follow each other's progress, and keep the result as a shared moment.

| Invite a friend | Find a random partner | Keep the memory |
| --- | --- | --- |
| Send an in-app invite by username or pick a recent walker. | Match anonymously without turning a random walk into a social connection. | See personal stats, shared walks, distance, and completed-session history. |

## Visual Story

<p align="center">
  <img src="assets/IMG_8638.PNG" alt="Invite a walker by username or from recents" width="220" />
  <img src="assets/IMG_8639.PNG" alt="Waiting for invited walker to join" width="220" />
</p>

<p align="center"><sub>Invite a person · wait for a second participant</sub></p>

<p align="center">
  <img src="assets/IMG_8642.PNG" alt="Live shared walk progress" width="220" />
  <img src="assets/IMG_8641.PNG" alt="Walker profile with shared statistics" width="220" />
  <img src="assets/IMG_8629.PNG" alt="Personal profile and walking history" width="220" />
</p>

<p align="center"><sub>Walk in real time · see a walking identity · build shared history</sub></p>

## What I Built

- Friend sessions: search by username, invite, accept or decline, and reconnect from recent walkers.
- Anonymous random sessions: no partner identity and no shared relationship history.
- Live progress: `CMPedometer` steps plus `Core Location` distance, synchronised through Supabase Realtime.
- Resilient session lifecycle: waiting, active, ended, expired, recovery after foregrounding, and server-side repair of stale public status.
- Profiles: avatar, walking identity badge, personal statistics, recent activity, and shared stats with a particular walker.
- Privacy controls: last-walk visibility and optional city sharing for random walks.
- Product polish: multilingual UI (`ru` / `en`), thoughtful empty states, invite feedback, end-of-walk summary, image cropping, and cache management.

## Engineering Focus

The hard part of this product is not drawing the screens; it is keeping two devices in agreement while either app can be backgrounded, restarted, or lose connectivity.

```text
CMPedometer / CLLocation
          ↓
WalkingViewModel (@MainActor)
          ↓  debounced, single-flight uploads
Supabase Postgres ─── Realtime ─── both devices update
          ↓
database rules repair public walking state
```

- `walk_sessions` is the server source of truth for session state and progress.
- Progress updates are debounced and single-flight to prevent competing writes.
- On return to the app, local counters reconcile with server progress instead of resetting.
- A database trigger derives `profiles.is_walking_now` from active sessions, so one device failing to finish cleanly does not leave a permanent “Walking now” state.
- Random sessions are explicitly marked and excluded from relationship statistics.

More detail: [architecture overview](architecture/overview.md).

## Stack

| Area | Technology |
| --- | --- |
| App | Swift, SwiftUI, MVVM, Swift Concurrency, Combine |
| Realtime backend | Supabase Auth, Postgres, Realtime, Storage, Edge Functions |
| Motion and place | `CMPedometer`, `CLLocationManager`, `CLGeocoder` |
| Local performance | `UserDefaults`, disk-backed history cache, avatar cache |
| Quality and delivery | RLS policies, TestFlight distribution, crash investigation and release hardening |

## Project Structure

```text
Core/           theme, DI, localisation, formatting, cache policy
Data/           Supabase repositories and platform services
Domain/         profiles, sessions, invites, history and analytics models
Presentation/   SwiftUI features, reusable views and view models
supabase/       schema, RLS policies, triggers and backend setup
```

## Privacy

- No credentials, API keys, backend URLs, or user records are published here.
- Random walks stay anonymous and do not become part of "walked together" profile history.
- Public last-walk time and random-walk city are controlled by the walker.

## Status

The app is actively developed and distributed through TestFlight.

---

<p align="center"><sub>Designed and built as an independent iOS product case study.</sub></p>
