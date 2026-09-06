# Legal documents

`documents.json` is the shared Russian/English source for the public pages and
the offline documents bundled with the iOS app. Run `python3 scripts/build_legal.py`
after edits. Copy the JSON to the private app's
`WalkWithMe/Resources/legal-documents.json` before releasing the same revision.

GitHub Pages: Settings > Pages > Deploy from a branch > main > / (root).
The site contains no app source, account records, credentials or third-party scripts.

Public contact: dianakuchaeva@hotmail.com.

Production configuration recorded on 2026-09-06: Supabase AWS region `eu-west-1`
(Ireland), Free Plan, with no automatic project backups. Before release, the
developer should confirm provider agreements and any changed log/backup retention, test production account deletion,
and check the target countries' consent and age requirements. The documents
describe the reviewed code; they are not a verification of production settings
or a guarantee of legal compliance or App Store approval. Configure App Privacy
in App Store Connect separately. Changes to processing require updating both
the published and bundled documents.

The Terms supplement Apple's Standard EULA; do not paste them into the custom
EULA field as a replacement license agreement.
