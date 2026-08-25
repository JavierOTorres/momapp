# Sanctuary — vertical slice v1.1

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
  Depth is where the money is and depth is what kills them.
- **The spiral.** A death costs a permanent `-0.10` survival and halves depth
  rather than resetting it, so dying never restores an adventurer to safety.
  Each death makes the next one likelier. Red pips under every figure count
  the deaths against the three they get.
- **Hollowing.** Three deaths (four with the Herbalist) and they hollow: grey,
  slumped, silent, holding a fire slot forever, announced with an ash burst
  and a line that fades. There are 8 slots, the Blacksmith holds 2 and the
  Herbalist 1, so every hollow eats one of the rest.
- **Rekindling.** `150 x 1.6^n` clears one hollow and returns them at depth 0,
  deaths forgiven. Souls into growth, or souls into repair.
- **Counsel.** Tap a resting adventurer for their depth, deaths, live survival
  odds and next payout. **Send shallow** runs their next expedition one layer
  short: safer, poorer, and no new depth. Tap a hollow to offer them the rite.
- **Vendors are survival, skills are economy.** Blacksmith 200 (+2/rest, +12%
  survival). Herbalist 500 (+8% survival, and they endure a fourth death).

State lives in memory only — a refresh resets the run. No save, no sound, no
art beyond flat shapes.

## Pacing

Simulated before building, every time. v1.1 keeps the patch's `DEATH_PENALTY`
of 0.10 exactly and moves only `base`, which is the dial the spec names: at
0.84 the new spiral runs far too hot (first hollow at 5 minutes, sanctuary
choked by 11). `base 0.98` lands the arc and keeps the slide legible — 92%
fresh, 80% at depth 4 with one death, 70% with two.

| | first hollow | Herbalist | choke | with rekindling | Counsel-heavy |
|---|---|---|---|---|---|
| target | 8-14 min | — | ~25 min | later | delayed, not escaped |
| shipped (median) | 7.2 | 10.5 | 19.0 | 21.5 | chokes at 34, or never |

Two honest gaps. The median first hollow is 7.2 rather than 8-14, though the
run-to-run spread covers it (p10 5.4, p90 13.2), and choke lands at 19-21
rather than 25. Both come from the same place: once deaths scar permanently,
hollows arrive about every two minutes, so the distance from first hollow to
choke is roughly ten minutes whatever the constants. Hitting choke at 25 would
mean pushing the first hollow to ~15, past the top of its own window. The
shape the patch asked for — spiral, doom, and banking as a stall rather than
an escape — holds either way, and a Counsel-heavy player never chokes at all
in half the simulated runs.

## The test

Play twenty minutes.
1. **When someone reached two deaths, did you watch them?**
2. **When they hollowed, did you care?**

Yes then no means the anticipation works and the loss is too cheap. No to the
first means the pips are not readable enough — a presentation problem, not a
balance one.
