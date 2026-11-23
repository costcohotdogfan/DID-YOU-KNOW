# Episode 02: Midjourney prompts

Written 2026-11-22. Nothing here has been submitted.

## The character

He is an adult, early twenties. Do not prompt him younger: the hotel scene needs a grown man, and so does the format (every playable character in this kind of game is an adult).

The running visual joke is that he is dressed for a New York winter in a Florida crime game.

Fixed line, used word for word in every prompt:

```
lanky young man in his early twenties, tousled brown hair with one grey streak, red hunting cap worn backwards, long tan wool overcoat, scarf, carrying a battered suitcase
```

Every prompt ends with the suffix:

```
--ar 9:16 --v 7 --p m7522496490742050258
```

## Step 1: make the reference

Run this first, pick the clearest full-body result, and use its image URL as `REF` in everything below.

```
third-person open-world video game screenshot, seen from behind, lanky young man in his early twenties, tousled brown hair with one grey streak, red hunting cap worn backwards, long tan wool overcoat, scarf, carrying a battered suitcase, standing outside a train station in a hot sunny Florida city, palm trees, everyone else in shorts --ar 9:16 --v 7 --p m7522496490742050258
```

Then every later prompt adds `--oref REF` before `--p`. Version 8 does not accept `--oref`, which is why these are version 7.

## Step 2: the shots

Each prompt starts `third-person open-world video game screenshot,` and includes the fixed line where it says HIM.

| # | Shot | Prompt body | Motion prompt for Animate manually |
|---|---|---|---|
| 1 | Arrival | seen from behind, HIM, walking out of a train station into a chaotic sunny Florida street, a car on the kerb, palm trees, people in shorts staring at his coat | the man walks out into the street and stops, looks left and right, traffic and pedestrians rush past, third-person video game camera follows behind him `--motion high` |
| 2 | The carjacking | HIM, standing on a sunny street pointing an accusing finger at a carjacker who is half way into a convertible, the driver on the pavement, both staring at him | the man wags his finger at the carjacker, says something, then turns and walks away, the carjacker and the driver watch him go `--motion low` |
| 3 | The payphone | HIM, in the foreground at an old payphone with the receiver to his ear, behind him a police chase tearing down the street, squad cars, smoke | police cars race past in the background, the man listens to the phone, then slowly hangs up without speaking `--motion high` |
| 4 | The piano bar | interior of a pink art deco hotel bar at night, a crowd applauding a piano player, HIM, the only person seated with his arms crossed, scowling | the crowd claps and cheers, the piano player bows, the man stays seated with his arms crossed and shakes his head `--motion low` |
| 5a | Hotel room, him | cheap hotel room at night, HIM, sitting on the very edge of a made bed still in his overcoat and cap, hands on his knees, looking at the floor, talking | static camera, the man sits on the edge of the bed in his coat, talks quietly, gestures a little with one hand, looks at the floor `--motion low` |
| 5b | Hotel room, her | cheap hotel room at night, a bored young woman in a green dress and jacket standing by the door with her handbag, looking at her watch | static camera, the woman checks her watch, sighs and looks at the door `--motion low` |
| 6 | After the punch | cheap hotel room at night, top-down, HIM, lying on his back on the carpet in his overcoat holding his stomach, cap fallen beside him | the man lies still on the carpet, third-person video game camera drifts in a slow idle circle above him `--motion low` |
| 7 | The pond | seen from behind, HIM, sitting alone on a park bench facing an empty city pond at dusk, no birds, no people | the man sits still on the bench, wind moves the water, video game camera slowly pushes in `--motion low` |
| 8 | The carousel | heavy rain, HIM, soaked, sitting on a bench smiling, a lit carousel turning in the background | the carousel turns in the rain, the man sits soaked and smiling, video game camera slowly lifts up and away `--motion low` |

Shots 5a and 5b are singles on purpose. In episode 01 Midjourney refused five times to animate a man and a woman in one frame, and the two singles animated first time.

The little sister on the carousel is described, never shown. Keep her out of frame.

## HUD for the edit

Three touches only: the mission card "DON'T GO HOME" on shot 1, a phony meter, and the ennui bar. `tools/build_cut.py` has the card and the ennui bar. The phony meter is not built.

## Narration

Two hyped takes of the locked script are in the ElevenLabs flow (`9eDcpVFUonoeSINbsbkk`), generated 2026-11-20. Nobody has picked one or checked them by ear.

Open question: the script says "the prep school upstate". If it changes to "college upstate" to match an adult character, the narration needs one more run.
