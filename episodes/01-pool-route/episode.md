# Episode 01: The Pool Route

Backbone: John Cheever, "The Swimmer". A man swims home through his neighbors' pools and finds his life has gone.

Status: cut v1 rendered 2026-11-20 from `edl.json`. Jamie has not yet given notes on sync. Not published.

## Narration as recorded (Marcus, eleven_v4, 48.85 s)

```
[excited, fast-paced, hyped gaming YouTuber] Did you know?! You can swim home in GTA VI!

[excited] Go to the pool party in Leaf Links at exactly 3:44 PM, and you switch to this guy! He's eight miles from his house, drink in hand! There's a chain of backyard pools the whole way! Swim one, have a drink! Swim one, have a drink! That's the entire gameplay loop, and your character thinks it's an adventure!

[excited, upbeat] Around pool nine, a neighbor says she's sorry about everything that happened! Nothing happened! You've been swimming!

[thrilled, speeding up] Pro tip: this is where it hits! The leaves are turning! You're tired in a way sleep doesn't fix! And you realize it wasn't an afternoon, it was your life! Your daughters grew up! Your friends stopped calling! Somewhere in there you lost the house, and you didn't notice, because the water was nice and somebody always handed you a glass!

[cheerful, bright] You didn't do anything wrong! You just didn't do anything!

[excited, big finish] Final pool: yours! Dark! Locked! Empty! Reward: you finally know how old you are! Like and subscribe!
```

The file Jamie chose is `audio/narration.mp3` (his `poolnarrationGTA.mp3`). Its pause pattern matches this text, but nobody has confirmed by ear that it is this take.

## Pauses measured in the narration

| Pause ends | Line that follows |
|---|---|
| 3.44 | Go to the pool party in Leaf Links... |
| 9.23 | There's a chain of backyard pools... |
| 15.88 | Around pool nine, a neighbor says... |
| 19.45 | Nothing happened! You've been swimming! |
| 21.57 | Pro tip: this is where it hits! |
| 38.84 | You didn't do anything wrong! |
| 41.73 | Final pool: yours! Dark! Locked! Empty! |
| 45.16 | Reward: you finally know how old you are! |
| 47.77 | Like and subscribe! |

Cuts between these are estimated from word counts.

## The swimmer

Fixed line, used word for word:

```
athletic tanned man in his late 30s with longer swept-back dark hair, navy blue swim shorts
```

Young reference still: Midjourney job `c0c2e0b8-f5fd-45bd-9104-88f27d0cbba0`, image 0 (the neighbor shot, him from behind).

Old version, same reference at `--ow 60`:

```
the same broad-shouldered man now aged 75, long swept-back grey-white hair, weathered sun-spotted skin, still a big frame but slack and tired, the same plain navy blue swim shorts
```

Every prompt ended: `--ar 9:16 --v 7 --oref https://cdn.midjourney.com/c0c2e0b8-f5fd-45bd-9104-88f27d0cbba0/0_0.png --p m7522496490742050258`

## Shots and the motion prompt each one got

| Clip file | Still shows | Motion prompt |
|---|---|---|
| hedgefront | he walks at camera through a hedge gap, sunglasses | the man strides confidently toward the camera through the gap in the hedge, grinning, video game camera pulls back in front of him `--motion high` |
| partywalk | from behind, facing the pool party, drink in hand | the man works his way through the pool party with his drink, nodding at guests who wave and cheer, crowd dancing, third-person video game camera follows behind him `--motion high` |
| sip | from behind, cocktail in hand at a pool | the man takes a long sip of his cocktail, then sets off walking toward the pool, third-person video game camera follows behind him `--motion low` |
| hedgejog | from behind, hedge, next pool ahead | the man pushes through the hedge and jogs toward the swimming pool ahead, third-person video game camera follows close behind `--motion high` |
| dive | mid-dive, big splash | the man dives forward into the pool with a huge splash, surfaces and swims away from camera with strong freestyle strokes, third-person video game camera follows behind `--motion high` |
| downsdrink | at the party, glass up | the man downs his cocktail, hands the empty glass to a guest and wades off into the pool, party guests laughing and dancing, video game camera drifts in behind him `--motion low` |
| swimacross | wide pool, him in the water | the man swims freestyle across the pool to the far side, climbs out dripping and jogs on toward the next yard, third-person video game camera tracking behind `--motion high` |
| woman0 | the neighbor alone, sundress and cardigan | static camera, the woman speaks gently to someone off-screen with a sad sympathetic face, small shake of her head, subtle natural movement `--motion low` |
| mansingle | him alone, towel round his neck, smiling | static camera, the man listens to someone off-screen, smiles, tilts his head with a puzzled raised eyebrow, gives a small shrug and a short laugh, subtle natural movement `--motion low` |
| tiredswim | swimming, orange leaves on the water | the man swims slow tired strokes through the leaf-strewn water, fallen leaves drifting on the surface, wind in the bare trees, video game camera slowly follows `--motion low` |
| shiver | sitting hunched at a pool edge, dusk | the man shivers and rubs his arms, dead leaves blow across the empty pool, video game camera slowly arcs a quarter circle around him to his profile `--motion low` |
| orbitA0, orbitA2 | young, sitting at the pool edge from behind | third-person video game camera slowly orbits a full circle around the man sitting alone at the edge of the pool, he stays still and stares ahead, dead leaves drifting, empty yard `--motion high` |
| orbitB1 | old, same pose | same prompt with "the old man" and "the empty pool" `--motion high` |
| oldbowed | old, side on, head down | the old man sits with his head bowed, slowly rubs his face with one hand, dead leaves blow past, video game camera slowly pushes in `--motion low` |
| oldpullback | frail old man at the water | the old man sits motionless, wind lifts his thin grey hair, video game camera slowly rises and pulls back to reveal the whole empty yard `--motion low` |
| olddarkwalk | old, on the path to the house at night | the old man walks slowly, barefoot and stiff, up the path toward the dark house, third-person video game camera follows behind him `--motion low` |
| olddarkstand | old, standing on the lawn at night | the old man stands still looking up at the dark house, breathing slowly, long grass moving in the night wind, video game camera slowly pushes in toward him `--motion low` |
| oldlocked | old, hand on the front door | the old man rattles the locked door handle, leans his shoulder into the door, it does not open, he lets his hand drop to his side, video game camera holds behind him `--motion low` |

`v2/beat6b_emptyroom.png` is a still (the empty room through the window), given a slow drift in the edit.

## What to fix in v2

- Sync on the "swim one, have a drink" montage is a guess.
- Two old-man shots have water in a pool that should be empty (`oldpullback`, and `orbitB1` partly).
- `oldpullback` is the earlier, frailer old man with different shorts. Replace or drop.
- The neighbor reads as a party guest, not a concerned neighbor.
- No captions.
