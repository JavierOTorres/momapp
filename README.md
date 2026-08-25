# Sanctuary — vertical slice v1

Idle/tycoon prototype. You keep the sanctuary; undead adventurers rest at your
bonfire, walk back out into something that will probably kill them, and come
home richer, poorer, or not really at all. You never fight, you never leave.

## Run it

Open `index.html` in a browser. One file, no build step, no dependencies, no
network. Design target is a 390x844 portrait viewport (mobile first); it stays
a static single file so it can be wrapped with Capacitor later.

## The loop

- **Souls**, one integer currency, with an honest trailing-60s average rate.
- **The bonfire.** A recruit arrives every 5s until the pool holds 12. Each
  guest takes a slot, pays on sitting down, rests 12s, then leaves for a
  **45-second expedition**.
- **Depth.** Survive and depth goes up by one, and a rest pays
  `perRest x (1 + depth/2)` — a depth 4 veteran is worth three fresh arrivals.
  Die and depth resets to zero and a death is recorded. Depth is where the
  money is and depth is what kills them.
- **Hollowing.** Three deaths (four with the Herbalist) and they hollow: grey,
  slumped, silent, holding a fire slot forever. There are 8 slots, the
  Blacksmith holds 2 and the Herbalist 1, so every hollow eats one of the rest.
- **Rekindling.** `150 x 1.6^n` clears one hollow and returns them at depth 0,
  deaths forgiven. Souls into growth, or souls into repair.
- **Counsel.** Tap a resting adventurer for their depth, deaths, live survival
  odds and next payout. **Send shallow** runs their next expedition one layer
  short: safer, poorer, and no new depth. Tap a hollow to offer them the rite.
- **Vendors are survival, skills are economy.** Blacksmith 200 (+2/rest, +12%
  survival). Herbalist 500 (+8% survival, and they endure a fourth death).

State lives in memory only — a refresh resets the run. No save, no sound, no
art beyond flat shapes.

## Pacing, and the one deviation from the spec

Simulated before building, and the spec's survival numbers did not survive it.
At 0.60 base survival with -0.06 per depth, 40% of shallow runs kill; across a
pool of 12 on 45-second cycles that manufactures a hollow roughly every minute
and fully hollows the sanctuary by minute 10 — long before the Herbalist that
is supposed to answer it. No cost tuning reaches the spec's own targets,
because the hollow rate is set by cycle length and pool size, not by prices.

`0.84 base, -0.05 per depth` keeps the shape (base + vendor bonuses - depth,
same 0.15/0.92 clamps) and lands the targets. Every other number is the
spec's: pool 12, threshold 3/4, vendors 200/500, 45s expeditions, unchanged
skill curves.

| | first hollow | Herbalist | choke | with rekindling | banking shallow |
|---|---|---|---|---|---|
| target | 6-10 min | 12-18 min | ~20 min | later | — |
| spec constants | 2.9 | never | 9.6 | 9.6 | — |
| shipped | 6.2 | 12.1 | 21.7 | 27.2 | never chokes |

## The test

Play for twenty minutes, past the first hollow.
**When the first one hollowed, did you care?**
If no, the punishment is too abstract — make the loss more visible, not more
frequent.
