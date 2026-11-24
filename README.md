# DID YOU KNOW?!

A shorts format. A breathless gaming-tips narrator gives real-sounding directions to a hidden mission in a big open-world crime game. The mission turns out to be the whole plot of a great novel or film. The narrator says the saddest true thing in the book out loud, delighted, and never notices. The reward is always insultingly small.

House voice, settled with Jamie on 2026-11-19: **literary ennui in an excited explainer voice.** The devastating line is said plainly and chirpily, not hidden in UI jokes. The narrator never names the book and never slows down.

## State (2026-11-24)

- **Episode 01, The Pool Route:** published, per Jamie on 2026-11-22. Which cut, which platforms and how it performed are not recorded here yet.
- **Episode 02, The Weekend in the City:** next up, chosen by Jamie on 2026-11-22. Script locked, narration generated (no take picked), Midjourney prompts written in `episodes/02-weekend-in-the-city/prompts.md`. No stills yet.
- **Ten more scripts** are in the house voice and ready to produce: `docs/scripts.md`. Jamie's pick after episode 02 is The Long Fish (The Old Man and the Sea).
- **Episode 03, The Long Fish:** stills generated for all twelve shots on 2026-11-23, none picked. See `episodes/03-the-long-fish/prompts.md`.
- Everything else is a premise. See `docs/backlog.md`.
- **Machines:** BIG (Omarchy laptop, `omarchy`) is set up at `~/Work/DID-YOU-KNOW` with media root `~/did-you-know-media/`; episode 01's footage is still only on BEAST.

## Where things are

| Thing | Location |
|---|---|
| Episode 01 source clips, stills, audio, cuts | BEAST: `C:\Users\JAMIE K\Downloads\poolroute_stills\` |
| Midjourney moodboard | "GTA VI", code `--p m7522496490742050258` |
| Narrator voice | ElevenLabs "Marcus", voice id `y0s2ExEMuum3muUnA6Zd`, model `eleven_v4` |
| ElevenLabs flow with all takes | flow id `9eDcpVFUonoeSINbsbkk` |
| Current scripts | `docs/scripts.md` |
| Full idea bank and earlier drafts | Claude doc "DID YOU KNOW?! — Things You Missed in GTA VI" |

Media is not committed. `.gitignore` excludes video, audio and images.

## Pipeline that worked for episode 01

1. **Script.** 160 to 200 words gives 45 to 60 seconds at the hyped pace. Get Jamie's yes before any image.
2. **Narration.** ElevenLabs, Marcus. Put an excited direction tag at the head of every paragraph and end the sad lines with exclamation marks. Full stops on sad lines make the voice slow down and act the sadness, which kills the joke. Two takes cost about 2,200 credits (roughly $0.40).
3. **Stills.** Midjourney with the moodboard. See "Character lock" below.
4. **Motion.** Midjourney "Animate manually" on each chosen still, one motion prompt per shot, written for that picture. Append `--motion low` or `--motion high`. Each job returns four 5.2 s clips at 464x832.
5. **Picks.** Jamie hearts one clip per shot in Midjourney. Download the hearted ones.
6. **Edit.** `tools/silences.sh` finds the pauses in the narration. Write an EDL (`episodes/NN/edl.json`) with a cut on each pause, then `tools/build_cut.py` renders it with the HUD.
7. **Verify.** File exists, non-zero, decodes, 1080x1920, duration matches narration, has audio. Then a person watches it.

## Character lock

The moodboard alone gives a different man in every shot. What fixed it:

- Midjourney **version 8 does not support `--oref`**. Use `--v 7 --oref <url of one good still> --p <moodboard>`.
- For an aged version of the same man, keep the same reference and add `--ow 60` plus the age in text ("the same broad-shouldered man now aged 75, long swept-back grey-white hair, the same plain navy blue swim shorts"). Text alone gave a different, frailer man in different shorts.
- An image prompt at `--iw 2` copies the reference too closely and ignores the text.
- Keep one fixed description line in every prompt. Shoot from behind where possible: it reads as a third-person game camera and hides face drift.
- The board pulls men toward bodybuilders and women toward glamour. Say so in the prompt if you want otherwise.

## Things Midjourney refused or got wrong

- **It would not animate a shirtless man and a woman in one frame.** Five attempts across four stills and three prompts vanished with no error. Covering it as two single shots (her, then him) animated first time and cut better.
- It ignores "no lights" and "no water" about half the time. Generate extra and pick.
- Text in images is garbage. All HUD and captions go on in the edit.

## The edit

- Cut on the narration's pauses. `silences.sh` gives them; inside a paragraph, estimate by word count.
- HUD is deliberately minimal: a mission card on the first shot, a small minimap, a health bar that drains and an ENNUI bar that fills. Jamie's note: heavy HUD jokes read as parody. It should look like real footage of someone playing the game wrong.
- The best cut in episode 01 is a match cut: the young man sitting at the pool with the camera circling, straight to the old man in the same pose.
- Clips are 464x832, so the 1080x1920 output is an upscale and looks soft full screen.

## Known gaps

- No captions yet.
- No word-level timing; fast montage cuts are estimated.
- "Leaf Links" in the episode 01 narration came from pre-release fan guides. Check it exists in the released game before posting.
- Never checked how the HUD sits under TikTok and Shorts interface chrome.

## Quick start

```
# pauses in a narration file
tools/silences.sh path/to/narration.mp3

# render an episode
python3 tools/build_cut.py episodes/01-pool-route/edl.json \
    --media "C:/Users/JAMIE K/Downloads/poolroute_stills" \
    --out poolroute_cut_v2.mp4
```

Needs `ffmpeg`, Python 3 and Pillow.
