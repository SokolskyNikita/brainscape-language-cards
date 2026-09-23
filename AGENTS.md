# Maintaining the live-course mirror

- This Git repository mirrors only the numbered vocabulary decks in the four
  courses listed in courses.json. Keep the root limited to those course folders,
  audio publication metadata, and the essential maintenance toolkit.
- Read README.md and maintenance/README.md before editing. Do not restore dated
  repair workspaces, test decks, duplicate exports, drafts, or superseded audio.
- Each deck CSV is editable text; its JSON preserves the last verified live card
  IDs, order, structured content, and attachment URLs. Preserve those identities.
- Use maintenance/mirror.py through run.py to check live state; --refresh replaces
  local exports using GET requests only. Do not overwrite unuploaded local edits.
- Preserve the agreed English vocabulary timeline, exact-form scheduling rules,
  reviewed senses, and approved exemptions. Russian translations are unrestricted.
- Keep new drafts and before/after backups outside this published mirror until
  the changes have been uploaded and verified. Git history preserves prior states.
- Audio releases contain only recordings currently attached to mirrored cards.
  Update the index/release after verified changes; do not publish obsolete takes.
- The API client remains outside this repo at ../api-client/ or installed in the
  environment. Do not vendor or publish it as part of card changes.
- Secrets belong in .env or process environment. Never print or commit them.
- Do not alter courses on Brainscape merely to reorganize this mirror.
