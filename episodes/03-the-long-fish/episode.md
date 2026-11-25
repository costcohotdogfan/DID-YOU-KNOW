# Episode 03: The Long Fish

Backbone: Ernest Hemingway, "The Old Man and the Sea".

Status: cut v1 (`long_fish_cut_v1.mp4`) rendered and technically verified on 2026-11-24; awaiting Jamie's watch/listen. Media lives on BIG under `/home/jamiecostco/did-you-know-media/03-the-long-fish/`.

## Narration as recorded (Marcus, eleven_v4, 50.96 s)

Generated via ElevenLabs Flow `9eDcpVFUonoeSINbsbkk` (node `EcH8a1PYxOByBQwug3Ms`), voice Marcus (`y0s2ExEMuum3muUnA6Zd`), model `eleven_v4`, two takes (`2,158` credits total / `1,079` per take, ~$0.39):

```
[excited, fast-paced, hyped gaming YouTuber] Did you know?! GTA VI has a fishing mission that 99% of players quit before the fish shows up!

[excited] Take the smallest boat in the Leonida Keys! You're old! Your luck stat is zero! You've gone eighty-four days without a bite! You used to have a kid who fished with you, but his parents moved him to a better boat! He still brings you coffee! He's the only one who does!

[thrilled, speeding up] Day eighty-five, go out farther than anyone! You hook the biggest marlin in the game! Pro tip: there's no reel-in button! It tows you for three days! Your hands open up! You start calling it your brother! It's the best friend you've had in years, and the mission is to kill it!

[excited, upbeat] You win! It's longer than the boat! Now head home! Sharks eat it! All of it! You fight them with an oar! You dock at night with a skeleton, and nobody's awake!

[cheerful, bright] Next morning, tourists think it's a shark!

[excited, big finish] Reward: nothing! You did everything right, and nobody saw! Go to sleep! Like and subscribe!
```

`audio/take1.mp3` (`50.96 s`, `833,443` bytes, `44100 Hz` mono mp3 `128 kbps`, decodes cleanly) is copied to `audio/narration.mp3` for cut v1 because every paragraph and sentence break aligns cleanly with a distinct measured silence. `audio/take2.mp3` (`50.16 s`, `820,904` bytes, `44100 Hz` mono mp3 `128 kbps`, decodes cleanly) is kept alongside it. Neither take has been listened to by a human yet.

## Pauses measured in `audio/take1.mp3`

Measured with `tools/silences.sh` (both default `-32 dB / 0.22 s` and `-30 dB / 0.14 s` pass):

| Pause ends | Line that follows |
|---|---|
| 2.18 | GTA VI has a fishing mission... |
| 6.22 | Take the smallest boat in the Leonida Keys! |
| 8.60 | You're old! Your luck stat is zero! You've gone eighty-four days without a bite! |
| 13.28 | You used to have a kid who fished with you, but his parents moved him to a better boat! |
| 18.25 | He's the only one who does! |
| 19.95 | Day eighty-five, go out farther than anyone! |
| 22.41 | You hook the biggest marlin in the game! Pro tip: there's no reel-in button! |
| 26.47 | It tows you for three days! Your hands open up! |
| 29.47 | You start calling it your brother! It's the best friend you've had in years, and the mission is to kill it! |
| 34.53 | You win! It's longer than the boat! |
| 36.68 | Now head home! |
| 37.57 | Sharks eat it! All of it! You fight them with an oar! |
| 40.60 | You dock at night with a skeleton, and nobody's awake! |
| 43.34 | Next morning, tourists think it's a shark! |
| 45.44 | Reward: nothing! You did everything right, and nobody saw! |
| 46.79 | Go to sleep! |
| 49.16 | Go to sleep! (short pre-beat) / Like and subscribe! (`49.96`) |

`45.44 s` is used as `ennui_full_at` (`Reward: nothing!`). Because each raw Midjourney clip is `5.208 s`, longer beats inside Paragraph 2 (`Take the smallest boat...` / `He's the only one who does!`) and Paragraph 6 cut cleanly on measured pauses across matching angles without reusing the same clip back-to-back.

## The fisherman

Character reference still: Midjourney job `a1b6f500-3491-4746-9688-dba4ea1616b0`, image `1` (`https://cdn.midjourney.com/a1b6f500-3491-4746-9688-dba4ea1616b0/0_1.png`, `--oref https://s.mj.run/6BjigTV-YyQ`, moodboard `--p m7522496490742050258` / `--profile fbuppxl`).

## Shots, Midjourney motion jobs, and Jamie's winning takes

All 13 animated Midjourney jobs returned four `5.208 s` clips at `464x832` (`24 fps`). Jamie's 1-based picks map to 0-based files under `clips/`:

| Clip file | Still picked | Video job ID | Pick (1-based) | Motion prompt submitted |
|---|---|---|---|---|
| `clips/s01_0.mp4` | `1-2` (`a1b6f500` idx 1) | `843c9187-30e4-4b31-a85a-f1273574b528` | `1-1` | `the old fisherman stands on the weathered wooden dock beside the skiff, takes a slow drag of his cigar and looks out over the turquoise water, gentle ripples and breeze in his white shirt, third-person video game camera slowly orbits --motion low` |
| `clips/s02_0.mp4` | `2-2` (`349f885c` idx 1) | `f74676bd-4317-4285-a65d-a2d4d76bb913` | `2-1` | `the old fisherman sits still in the small wooden skiff with the cigar in his mouth, squinting out over the flat sunlit water, the skiff rocks gently on calm swells, third-person video game camera slowly drifts --motion low` |
| `clips/s03_1.mp4` | `3-4` (`40bf8853` idx 3) | `5056c3b2-080a-4d1a-a4ab-bbbdf41cdc07` | `3-2` | `the old fisherman stands on the wooden dock holding his paper coffee cup and raises it for a slow sip as the big white sport-fishing boat and pink boat idle in the harbor behind him, third-person video game camera slowly pushes in --motion low` |
| `clips/s04_2.mp4` | `4-4` (`6f432b3d` idx 3) | `5a5ff3db-9c94-42ad-b6d4-c7fbfcb87f4a` | `4-3` | `high aerial video game camera slowly rises and drifts above the tiny wooden skiff cutting forward through choppy deep blue ocean swells, whitecaps rolling past --motion low` |
| `clips/s05_2.mp4` | `5-3` (`d9ef1b43` idx 2) | `bdc3d5f4-f811-4751-8ce3-124ca851f9ae` | `5-3` | `the giant blue marlin crashes back down into the sea in a huge burst of white spray, the fishing line snaps tight and the tiny wooden skiff lurches forward as the old man braces, third-person video game camera follows behind --motion high` |
| `clips/s06_0.mp4` | `6-1` (`60f422f2` idx 0) | `5b35b70c-0a87-4faf-b7fd-ca8e839ca3e6` | `6-1` | `at night under the stars, the tiny wooden skiff is towed steadily forward cutting a foaming wake through dark water while the old fisherman grips the boat sides with his rope-wrapped hands, third-person video game camera follows behind --motion low` |
| `clips/s07_2.mp4` | `7-2` (`7153fb49` idx 1) | `d9c81db6-7c70-4521-a68d-b9e2b6279c7a` | `7-3` | `the enormous dark blue marlin glides smoothly through the clear turquoise water right alongside the wooden skiff while the old fisherman leans over the rail watching it, water shimmering, video game camera gently tracks --motion low` |
| `clips/s08_2.mp4`, `clips/s08_3.mp4` | `8-1` (`37d617db` idx 0) | `2beafd0f-5dba-4ca2-b8a8-93fa00b3fec7` | `8-3`, `8-4` | `aerial video game camera slowly circles overhead as the tiny wooden skiff with the enormous blue marlin lashed to its side drifts smoothly across sunlit turquoise ocean swells --motion low` |
| `clips/s09_0.mp4` | `9v2-1` (`db804453` idx 0, `--ow 45`) | `7b7ce761-e842-44f6-80c1-4d75b5b8ebfa` | `9-1` | `third-person video game camera circles around the old fisherman standing in the tiny wooden skiff in deep open ocean as he swings his wooden oar down at dark sharks circling and striking the giant marlin in foaming blue waves --motion high` |
| `clips/s10_1.mp4` | `10v2-1` (`f249b3b3` idx 0) | `a0097fef-9eb7-4af7-8b74-3dec51562c02` | `10-2` | `third-person video game camera slowly orbits around the tiny wooden skiff tied to the quiet night dock as the giant bleached white marlin skeleton rocks gently in the dark rippling water under warm dock lights --motion low` |
| `clips/s11b_1.mp4` | `11-4` (`83c8c14e` idx 3) | `42d00aa9-05c9-47a7-aa7a-d660b0dfe360` | `11-2` | `third-person video game camera slowly circles past the sunny Florida Keys dock as tourists point and take photos of the giant marlin skeleton resting in the clear shallow water beside the wooden skiff --motion low` |
| `clips/s12_3.mp4` | `12-2` (`82598e1c` idx 1) | `cce3b81b-afb0-405d-adce-f5abb483e60a` | `12-4` | `the old fisherman lies completely still asleep on the cot in the weathered wooden shack, faint dust motes drifting through shafts of morning sunlight, video game camera very slowly pulls back --motion low` |

Alternate Shot 11 still `11-2` (`83c8c14e` idx 1, chrome marlin sculpture) was also animated as job `e02aabe1-8a91-45fe-b479-0c2dc4e9a706` (`clips/s11a_0..3.mp4`).

## Known notes in cut v1

- `clips/s04_2.mp4` (from still `4-4`) has a small baked-in minimap at the extreme bottom-left edge below our GTA VI HUD vitals capsule (`y = 1280..1548`).
- Jamie's pick `11-2` was mapped to `clips/s11b_1.mp4` (take 2 of the natural bone skeleton in the water beside the skiff, matching Shot 10). `clips/s11a_1.mp4` (take 2 of the chrome sculpture on the dock) is also on disk if Jamie wants to swap.
- Cut v1 renders at `1080x1920`, `30 fps`, `h264` + `aac` (`50.96 s`, `106,178,219` bytes), decodes cleanly end-to-end; no human has watched or listened yet.
- No captions yet.
