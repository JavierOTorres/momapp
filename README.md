# Sanctuary — vertical slice v0

Idle/tycoon prototype. You keep the sanctuary; undead adventurers rest at your
bonfire, spend souls, and walk back out. You never fight, you never leave.

## Run it

Open `index.html` in a browser. No build step, no dependencies, no network.
Design target is a 390x844 portrait viewport (mobile first); it stays a single
static file so it can be wrapped with Capacitor later without restructuring.

## What v0 contains

- **Souls**, one integer currency, shown with a live per-second rate.
- **The bonfire.** An adventurer arrives every 5s, rests, and pays 1 soul.
  Tapping the fire pays 1 soul per ember; the fire holds 10 embers and refills
  one every 2s, so tapping helps in the first minute and stops mattering after.
- **Skills.** Kindled Flame (+1 soul/rest, 10 x1.5), Word of Sanctuary
  (arrivals -10%, 25 x1.7), Soul Echo (+5% double-pay, cap 50%, 50 x2.0).
- **Build.** The Blacksmith, 200 souls, one time, +2 souls/rest, and he shows up
  beside the fire and hammers.

State lives in memory only — a refresh resets the run. No save, no sound, no art
beyond flat shapes.

## Pacing

Simulated against the spec's cost curves: greedy natural play reaches the
Blacksmith in roughly 9-11 minutes, inside the 8-12 minute target.

## The test

Play ten minutes, close it, then answer: do you want to open it again?
If no, the loop is wrong — change the loop, don't add content.
