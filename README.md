# Sanctuary — v4.1

Idle/tycoon prototype. You keep the sanctuary; undead adventurers rest at your
bonfire, walk back out into something that will probably kill them, and come
home richer, poorer, or not really at all. You never fight, you never leave.

## Run it

Open `index.html` in a browser. One file, no build step, no dependencies, no
network. Design target is a 390x844 portrait viewport (mobile first); it stays
a static single file so it can be wrapped with Capacitor later. It saves to
localStorage every five seconds and on page hide.

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
- **The strip.** Every adventurer currently below is a marker descending a
  track down the left, carrying their depth and their scars, with ambushes and
  discoveries flashing as they go. Tap one to ring **the bell**: they come home
  immediately and alive, no deeper than they left, and they pay you nothing.
  It costs more every time.
- **Artifacts belong to whoever found them.** A survivor carries their find
  home filthy and it stays theirs — there is no inventory anywhere in the
  game. Clean it from their Counsel card by dragging the grime off, and its
  slot, rarity and curse are all plain. Empty slot, it goes straight on them;
  full slot, you choose, and the one you don't choose burns. A second of
  something they already carry becomes scrap before it reaches them.
- **Curses are visible and worth considering.** One find in five is marked. A
  cursed piece gives more than an honest one and bills a different system: a
  blade that keeps them alive and cuts their pay by two fifths, plate that
  blunts the scar for eight points of survival, a charm that pays and makes
  every death cut deeper.
- **Gear.** Three slots per adventurer, applied to survival, scar and purse.
  What they wear when they die stays at that depth until someone survives a run
  that deep. What they wear when they *hollow* goes to the **reliquary**, a
  shelf by the fire holding three, each labelled with the depth and death count
  of whoever carried it. You can hand one to someone living, once.
- **Vendor craft.** Both vendors take three levels, paid in souls and scrap.
  The smith reforges common to fine and fine to rare, on the wearer, without
  taking it off them. The herbalist lifts curses — roughly at first, costing
  the piece a grade, and cleanly once fully paid for.
- **Letting go.** A hollow can be rekindled — priced by the deepest they ever
  got, `120 + depth x 45`, so a veteran costs and a stranger doesn't — or let
  go for a flat 40 souls: the seat comes back, their things go on the shelf,
  they are written down, and a little ash comes back mid-run. Both prices sit
  on the same card, because the comparison is the decision.
- **Six vendors, four plots.** Blacksmith, Herbalist, Quartermaster,
  Cartographer, Ossuary and Tinker, each with three levels. The ground holds
  four to start and one more per three levels of Kindled Flame, to seven, so
  you cannot have them all. Anything can be pulled down for half its souls.
- **Placement.** A plot inside the light works at full strength and takes a
  seat from the ring; one outside works at 70% and takes no seat. The light
  moves as the fire grows and dies, so the same plot is not always the same
  bargain — a dying fire pulls every vendor out into the dark with it.
  Neighbouring plots pair up, and the pairs are written in the notes.
- **Routing.** With the Cartographer you choose where each rester goes: a
  fragile veteran farmed shallow, a geared newcomer thrown at the next gate.
- **A verb per vendor.** Hammer on the beat, stir a circle, pack a bag, trace
  a route, hold a vigil, break something apart. Each finishes inside five
  seconds; sloppy work gets the base result and good work a small bonus.
  Walking away mid-gesture still completes the job. Cleaning a find uses the
  verb of the place it came from: wipe, scrape, press, cut, thaw, or wipe
  against ash that creeps back at the edges.
- **The Archive.** The keeper's notes, in the book in the top bar. Plain
  entries for every mechanic, locked to their names until it has happened.
- **The road.** Seven named places, two depths each, every one shut behind a
  gate. A gate is tried once per fire against the attempting adventurer's
  gear, depth and scars — not a coin flip. Through it, the place below opens
  and they come back carrying something out of the gate itself. Fail and they
  are thrown back, take a death, and drop what they had. The strip on the left
  is the road; its head opens the map, its markers open the place.
- **The flame.** 0 to 100, decaying always. The living circle feeds it, hollows
  eat it, and only those who can reach a seat feed it fully. At zero the fire
  is out and the run is over.
- **The cycle.** Runs end — at zero, or when you choose from the notes — and
  pay ash scaled by depth reached, souls earned and who is still standing. Ash
  buys structural unlocks that change how the next fire starts. No multipliers.
- **The kept dead.** Anyone who reaches depth 3 gets a name. Everyone who
  hollows is recorded permanently, across every cycle: name, depth, deaths,
  what they were carrying.
- **Offline.** Close it and the fire keeps burning without you, capped at eight
  hours, simulated through the real rules. The return report tells you what it
  cost.
- **Vendors are survival, skills are economy.** Blacksmith 200 (+2/rest, +12%
  survival). Herbalist 500 (+8% survival, and they endure a fourth death).

State lives in memory only — a refresh resets the run. No save, no sound, no
art beyond flat shapes.

## Pacing

Simulated before building, every time. `base 0.98` with a `0.10` death scar
keeps the slide legible — 92% fresh, 80% at depth 4 with one death, 70% with
two — and lands the arc.

| | first hollow | Herbalist | choke | with rekindling | Counsel-heavy |
|---|---|---|---|---|---|
| target | 8-14 min | — | ~25 min | later | delayed, not escaped |
| shipped (median) | 7.2 | 10.5 | 19.0 | 21.5 | chokes at 34, or never |

**v2 needed no retune.** The expectation was that artifacts would push survival
up and slow hollowing, but simulated with typical gear the first hollow moves
from 7.1 to 6.8 minutes, which is inside the noise. Gear is lost on death, so
the scarred adventurers nearest to hollowing are precisely the ones wearing
nothing — the loss rule pays for the survival rule. First artifact drop lands
at 94 seconds of real play, against a target of three minutes.

**v3 fills the hall.** At 45s expeditions against 12s rests only 24% of the
pool was ever home, which is why the sanctuary looked abandoned. At 30/20 it
is 48%, measured over a minute of real play.

**Cursed gear is a real trade.** Simulated, wearing every cursed find earns
about 2% less than burning them all and pushes the choke from 23.4 to 27.1
minutes. Tempting, neither obviously right nor wrong.

**v4 tuning.** The flame is calibrated so an empty sanctuary dies in 45
minutes, a full circle holds it at -0.0004/s (measured live, not just
simulated), and two hollows tip it into decline. A simulated played run ends at
**38 minutes**, inside the 35-50 target; a run where the player buys nothing
ends at 26. Widening the circle to 20 earns 810 souls/minute against 500 and
ends at 35 minutes instead of 38 — burns brighter, dies sooner, as specced.
Gates are set against what is reachable at each cap: gate 1 falls to one fine
weapon, gate 5 needs more than two rare pieces at depth 9, gate 6 needs ash
unlocks behind it.

**v4.1: the Ossuary needed the spec's own fallback.** At level 2 the spec has
hollows stop pulling at the flame entirely. Simulated, that stretched runs from
38 minutes to **136** — the fire effectively stops dying, which is not a run any
more. The spec anticipated this and named the remedy, so the Ossuary halves the
pull instead of removing it: **48.9 minutes**, inside the 35-50 window.

**Let Them Go stays small**, 1 to 2 ash by depth, against roughly 113 for a full
run — under the 15% ceiling even used on every hollow, and doubled by the
Ossuary because that is what the Ossuary is for.

**Blacksmith 3 is not reachable, and the reason matters.** At 2500 souls it
was hit in 0 of 20 simulated hours under greedy play, 2 of 20 when chasing it
deliberately, and 0 of 20 when rekindling above all else. Scrap is not the
constraint — 64 spare at the hour mark — souls are, because the sanctuary
chokes at 22 to 27 minutes and income stops there. A 35-to-45-minute target
cannot coexist with a 25-minute choke: rekindling cannot outrun hollowing
because its price grows 1.6x per use while hollows keep arriving every two
minutes. The prices ship as specced. The fix is a decision about which target
gives — a cheaper level 3, or a rekindle curve that lets a diligent keeper
hold the fire past 35 minutes.

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
