# Automatic hotline checks

Every push to `main` runs **Check Vietnam hotline information**. The workflow can also be started manually from GitHub Actions.

The checker reads the actual contact cards embedded in `index.html`, downloads the Vietnam directory and the five provider profiles on Find A Helpline, and compares:

- Provider listings and telephone numbers, within each provider’s directory entry.
- Official website links.
- Opening hours for Ngày Mai, the National Child Helpline, CSAGA and Peace House, which publish hours in their profiles.

HOPE’s profile does not publish its hours, so this workflow explicitly does not verify that field. Descriptions and clinical suitability still require human review. It never invents replacements or automatically edits contact details.

Results are saved to `status.json` on the `hotline-checks` branch and attached to the Actions run. That branch does not trigger this workflow or change the deployed game. A failed request, changed field or missing provider makes the check fail and publishes a review/unavailable status. The last successful verification date is retained in the report and is never advanced on failure. Newer push results cannot be overwritten by an older run.

The game reads this public report and only shows a verification date when the check passed and the SHA-256 hash matches the exact support content currently loaded. Content deployment dates remain separate from source verification dates. A deployment can still proceed while the source check is running or failing; GitHub Actions and the in-game contact footer show the check result.

No separate credentials are needed. The workflow uses the repository’s temporary `GITHUB_TOKEN` to write its status branch; nothing secret is sent to Find A Helpline or included in the game. The Python checker uses the standard library and only requests the configured public source pages.
