# Episode 03: The Long Fish

Backbone: The Old Man and the Sea. Script is in `docs/scripts.md`.

Status: prompts written 2026-11-23. Nothing submitted. No narration yet.

## The character

Fixed line, used word for word in every prompt:

```
thin weathered old fisherman in his seventies, deep-tanned creased neck, white stubble, faded straw hat, patched white shirt with rolled sleeves, bare feet
```

Suffix on every prompt: `--ar 9:16 --v 7 --p m7522496490742050258`

## Step 1: make the reference

```
third-person open-world video game screenshot, seen from behind, thin weathered old fisherman in his seventies, deep-tanned creased neck, white stubble, faded straw hat, patched white shirt with rolled sleeves, bare feet, standing on a weathered wooden dock beside a tiny wooden skiff at dawn, Florida Keys, turquoise shallows, minimap in corner --ar 9:16 --v 7 --p m7522496490742050258
```

Pick the clearest full-body result. Use its image URL as `REF`; every later prompt adds `--oref REF` before `--p`.

## Step 2: the shots

Each prompt starts `third-person open-world video game screenshot,` and includes the fixed line where it says HIM.

| # | Line it covers | Prompt body | Motion prompt |
|---|---|---|---|
| 1 | Did you know?! | the reference still | the old man steps down into the skiff and pushes off from the dock, third-person video game camera follows behind `--motion low` |
| 2 | eighty-four days without a bite | seen from behind, HIM, sitting in a tiny wooden skiff on flat empty water under a white midday sun, fishing line slack over the side | the old man sits still holding a slack line, the skiff rocks gently, nothing happens, video game camera slowly circles `--motion low` |
| 3 | his parents moved him to a better boat | HIM, on the dock at dawn holding a paper coffee cup, watching a big modern sport-fishing boat full of people pull away | the big boat pulls away from the dock, the old man watches it go and sips his coffee `--motion low` |
| 4 | go out farther than anyone | aerial view, a tiny wooden skiff alone on deep blue open ocean, no land in sight, one small figure in a straw hat | video game camera rises high above the tiny skiff on the open ocean `--motion low` |
| 5 | you hook the biggest marlin | seen from behind, HIM, braced in the skiff with a taut fishing line over his shoulder, a huge marlin leaping out of the water ahead | the giant marlin leaps and crashes back into the sea, the line snaps tight, the old man braces, the skiff lurches forward `--motion high` |
| 6 | it tows you for three days | night, seen from behind, HIM, hunched in the skiff under the stars with the line across his back, hands wrapped in rags, the skiff cutting a wake | the skiff is towed steadily through dark water, the old man holds the line across his back, stars overhead, camera follows behind `--motion low` |
| 7 | you start calling it your brother | HIM, leaning over the side of the skiff looking down at the dark shape of an enormous fish swimming just below the surface | the huge fish glides beside the skiff just under the surface, the old man leans over and looks at it `--motion low` |
| 8 | it's longer than the boat | aerial view, the tiny skiff with an enormous marlin lashed alongside, the fish longer than the boat, calm sea | the skiff sails slowly with the huge fish tied alongside, video game camera circles overhead `--motion low` |
| 9 | sharks eat it | HIM, standing in the skiff swinging an oar, shark fins circling the fish tied alongside, churning water | shark fins circle and strike at the fish, the old man swings the oar down at them again and again `--motion high` |
| 10 | you dock at night with a skeleton | night, the skiff tied at an empty dock, a giant fish skeleton with its long bill lashed alongside in the black water, one distant lamp, nobody around | the skeleton rocks gently beside the skiff in the dark water, video game camera slowly pushes in `--motion low` |
| 11 | tourists think it's a shark | morning, seen from behind, a group of tourists in shorts and sun hats on a dock pointing phones at a giant fish skeleton in the water | the tourists point and take photos of the skeleton, laughing, static camera `--motion low` |
| 12 | Go to sleep! | interior of a bare wooden shack, HIM, asleep face down on a narrow cot, arms out, palms up, morning light through the slats | the old man sleeps without moving, dust drifts in the light, video game camera slowly pulls back `--motion low` |

The kid who brings the coffee stays off screen. Shot 3 implies him with the cup.

Shot 11 is a group seen from behind with no faces. If Midjourney refuses to animate it, use the still with a push-in.
