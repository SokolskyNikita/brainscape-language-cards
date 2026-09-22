> Superseded by the completed [full 20,000-card repair](../repair_20260907/README.md). This report describes the original pre-repair sample.

# First-25-card audit

Start with [report.md](report.md). It includes all 40 decks, original examples, findings, and suggested repair directions.

- `review.json`: all 1,000 reviewed cards and their findings. Empty findings means no actionable issue identified in this review.
- `source_manifest.json`: source CSV hashes and card counts.
- `vocabulary_candidates.json`: raw morphology candidates before manual exclusions; do not treat these as confirmed findings.
- `build_report.py`: curated findings and report generation.
- `vocabulary_check.py`: supporting vocabulary inventory check; requires pymorphy3 and NLTK with WordNet data.
- `source_data.py`: reads the existing CSVs through the local Brainscape parser.

To reproduce against unchanged source files, run `python3 audit_first25/vocabulary_check.py`, then `python3 audit_first25/build_report.py` from the project folder. These only write audit outputs. Curated findings use original card positions and must be re-reviewed if source decks change.

The review uses prior decks only for supporting vocabulary, except that the first deck may use any of its own words. This is stricter than some existing fixer-guide instructions. Suggested corrections have not been applied to the source decks.
