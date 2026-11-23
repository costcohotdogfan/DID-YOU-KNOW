# Rules for agents working in this repo

Global rules live in the HQ repo's AGENTS.md. These are the ones specific to this format.

## Before spending

- Nothing paid runs without Jamie's click. Price it first, in dollars.
- Midjourney on the subscription is the default for stills and motion. A video job costs several times an image job in fast hours, so animate only stills Jamie has hearted.
- No Seedance HD.

## Content lines

- The swimmer and every other character is original. Do not prompt for Rockstar's actual characters, logos or HUD art, and do not prompt for a real actor's likeness. Describe a type.
- No real people in any shot.
- The narrator never names the source book or film.

## Reporting

- Say which is true for each step: instruction written, job submitted, or output verified.
- "Verified" for media means: file exists, non-zero size, decodes end to end, and matches the spec for dimensions, duration and audio. Report the numbers. If no one has watched it, say that too.
- A Midjourney job that shows "Starting..." has not succeeded. Check that the clip exists.

## Failures

- Smallest justified fix, retry once, then stop and report the exact error. Do not redesign the pipeline around a failure.
- If Midjourney silently drops a job twice, stop retrying that image and say so.

## Housekeeping

- Project state lives in README.md. Update the State section at every handoff.
- No side notes files. Remove guidance that has been disproven instead of adding to it.
- Media is not committed. Keep it in the episode's folder on BEAST and record the path in README.md.
