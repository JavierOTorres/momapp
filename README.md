# Sanctuary — v5.1

Idle/tycoon prototype. You keep the sanctuary; undead adventurers rest at your
bonfire, walk back out into something that will probably kill them, and come
home richer, poorer, or not really at all. You never fight, you never leave.

## Run it

Open `index.html` in a browser. Double-clicking it is enough — no server, no
build step, no dependencies, no network. Design target is a 390x844 portrait
viewport (mobile first); it stays a static single file so it can be wrapped
with Capacitor. It saves to localStorage every five seconds and on page hide.

The sprite art lives in `assets/` for authoring, but the game does not read it
at runtime: it is baked into `index.html` as data URIs. That is what keeps
double-clicking working — a page opened over `file://` cannot load its own
`assets/` folder in Safari, and where it can, the images come back cross-origin
and taint the canvas. **After changing any art, re-run
`tools/embed_sprites.py`**, or the game will keep drawing the old sprites.
`tools/embed_sprites.py --check` says whether `index.html` is up to date.

Note that `file://` and `http://localhost` are different origins, so a save made
under one is not visible under the other. Pick one and stay on it.

Neither tool in `tools/` is called by the game. See **Sprites** below.

## The first fire

A new player used to arrive into flame decay, hollowing, gear binding, routing,
gates, plots, adjacency, six vendors and ash all at once. The opening is now an
**authored first cycle** rather than a tutorial layer: no modals, no arrows, no
skippable overlay, and every word of teaching is a single line in the keeper's
voice that fades. Three rules hold throughout.

- **The HUD assembles itself.** Every element starts absent — collapsed, not
  greyed — and fades in the moment it first becomes true. The game opens on a
  full-bleed canvas with no top bar, no counts, no tabs and no book.
- **Reveals are gated; input never is.** Anyone who works out an action early
  can take it. The Counsel card, for instance, is tappable from the first
  arrival, long before the sequence points at it.
- **It runs on the first cycle only.** Every fire after the first opens whole.

The game opens on almost nothing: a dark screen, the flame at **15** and
blue-grey, a light radius of a few feet, the keeper alone, and no interface. The
only thing on screen that moves is the fire, and it is the only lit thing on a
dark screen — which is the entire tutorial for the tap.

| Beat | Fires when | What arrives |
|---|---|---|
| 1 Ember | first tap | Tapping adds **1.5 intensity, not souls** — the one time in the game the flame goes up. Ember pips appear after the third tap, once the limit has been felt. |
| 2 Light | intensity 40 | The light widens; the dais, the first columns and the moss come out of the dark. |
| 3 Arrival | intensity 60 | The first adventurer walks in from outside the frame. The soul counter fades in on the first soul actually paid. |
| 4 Skill | third rest | The Skills tab, holding **only Kindled Flame**, and the Archive icon. Buying it grows the fire, widens the light and adds a seat; Word of Sanctuary and Widen the Circle arrive with the purchase. |
| 5 Road | pool reaches 3 | The first expedition leaves and the road bar fades in with it. Nobody goes down before there are three of them. |
| 6 Depth | first return | The flame bar arrives — now there is something to protect — and the returning adventurer **glows faintly until tapped, once, ever**. Soul Echo appears with depth. |
| 7 Find | first artifact | The find, the dusting gesture, and equipping on the same card. |
| 8 Death | first failure | Death pips, on everyone from then on. |
Beats 7 and 8 are the only two driven by what happens down there rather than by a threshold, so either can land first. Each owns its own flag instead of a position in the counter, so neither is swallowed when the other arrives early.

| 9 Hollow | first hollowing | The full moment: the drop, the drain ring, the line. Both prices on tap. Whatever the player does, including nothing, is correct. |
| 10 Build | that hollow resolves | The Archive opens once, unprompted, on the entry about hollowing — then the Build tab, with the plots visible and only the Blacksmith affordable. |

Three places the first cycle cheats, and only the first cycle. The keeper feeds
the fire at **0.55 intensity a second** during beats 1-3, so a player who never
taps still sees somebody arrive inside 90 seconds; the first Kindled Flame costs
**3 souls** instead of 10, so it is affordable on exactly the third rest that
triggers it; and the opening pool carries **+0.07 survival**, which expires the
instant the first one hollows. Everything after that is the ordinary game.

That last one needs its own note, because it does less than it looks like. The
survival cap is 92%, so at depth 0 with no scars the grace is swallowed whole —
the headline number a new player reads on the Counsel card is **92% with it or
without it**. It only bites where the cap is not binding: deep runs and scarred
adventurers, which is exactly where hollowing comes from. Over 150 simulated
first cycles that moves the first hollow from a median of **6.6 minutes** (p10
4.9, p90 9.3) to **8.3** (p10 5.3, p90 11.6), which puts the median inside the
spec's 8-12 minute window. The spread stays wide either way: one live
playthrough landed the first hollow at 4.1 minutes and another at 6.4, both
legitimate low-tail draws rather than a mistuning. Reducing the death scar
instead was tried and is a weaker lever — 0.10 down to 0.06 only reaches a
median of 7.6.

## What it looks like

A ruined human temple, swallowed by forest, kept by animals. The people who
built it are gone and nobody knows why. The fire burns in a cracked stone basin
at the centre of a dais built for larger bodies; broken columns stand at the
edge of the light and fall into the dark as the flame dies, so the building
disappears around you over a run.

The camera sits close. It frames whatever is actually lit — the fire alone at
the opening, the seated ring once there is one — and **pulls back as the light
grows**, so the sanctuary grows into the screen instead of shrinking inside it.
The world has fixed coordinates and the camera absorbs every change in stage
height as the HUD assembles itself, so nothing in the scene moves when a panel
appears.

Every figure is a **head with legs**: a **28 tall by 36 wide** head, a 12x20
body block under it, two 8x6 peg legs with daylight between them, 48 pixels in
all. The head is wider than it is tall and wider than the body on every figure
and every build variation — square heads were why the style did not read. Eyes sit on an inset face plate, lighter than the head and
shaped by species: wide and low for frog, narrow for crow, squared for goat.
Ears, horns and beaks attach outside the plate. Every shape carries the same
3px near-black outline, with no interior weight hierarchy. The keeper is built
the same way and set apart by scale and colour instead — taller, darker, and
nothing under the hood.

Colour is split. **Bodies stay animal-coloured** — browns, greys, greens,
creams — and **garments carry the saturation**: red, gold, violet, teal, moss,
rust. Species gives the silhouette and garment gives the name, so the garment
is picked to be the rarest colour in the circle and never repeats on two of the
same animal. Across 200 simulated rosters of eight, no two members ever shared
both species and garment. The fire is still the brightest thing on screen; it
is no longer the only saturated one.

A hollow keeps its silhouette exactly — same species, same garment shape — and
loses everything else: the face plate goes dark, the eyes become empty sockets,
the garment desaturates while keeping its value, the posture drops, and every
other thing in the scene keeps moving while it does not.

**No text is drawn on the sanctuary scene** except the one-line event messages
and the numbers that float off a payment. Depth, location, plot status and
adjacency all live in cards. Inner and outer plots are told apart by whether
the light reaches them, which was always legible without a label.

The artifacts are human relics, which is why they come up filthy and why
nobody can say what they were for. The item descriptions are guesses.

## Sprites

A species can be drawn from hand-made art instead of from code. Six poses per
species — `stand`, `walk_a`, `walk_b`, `sit`, `rest`, `weary` — under
`assets/sprites/`, named `<species>_<pose>.png`. **Frog and goat are wired up;
cat, dog, crow and rabbit are still code art.** Anything with no files keeps its
code-drawn figure, so the rest drop in one at a time and a missing file is never
worse than the art already there. Adding a species is one key in
`SPRITE_SPECIES`, its six files, its eye sockets in `SOCKETS`, and a re-run of
`tools/embed_sprites.py`.

Nothing that responds to the world is baked into a sprite. The idle bob, the
firelight, the contact shadow, gear overlays, the death pips and depth marks
are all still drawn in code, on top. A sprite's baseline lands exactly where
the code figure's feet land, so nothing about positioning changes when a
species switches over.

Pose follows state: walking alternates `walk_a` and `walk_b` every 250ms,
desynchronised per figure; standing with no seat is `stand`; seated is `rest`,
or `sit` while a find or a choice is waiting on them; two deaths or more
overrides stand and sit with `weary`. Hollows have no art yet and are derived
from the sit pose — drained to the hollow colour, sockets over the eyes, tilted
a few degrees, no bob. Real hollow sprites will be a manifest change.

Sprites come out of image generation framed inconsistently, which in game reads
as the figure changing size and hopping every time it changes pose.
`tools/normalize_sprites.py` fixes that: it finds the alpha bounding box,
scales the content to a uniform **height** (never a uniform bounding box —
widths must stay free or a wide sitting pose gets squashed), centres it, and
sits its bottom edge on a fixed baseline. It reports before and after bounding
boxes so alignment is checked numerically rather than by eye.

It also erases disconnected specks under `--min-blob` (default 48px) before
measuring. Background removal leaves them, and a speck is not cosmetic here: a
stray dot below the feet drags the bounding box down, so the figure gets scaled
to fit and then hung in the air with the speck sitting on the baseline. That is
exactly what `goat_walk_a` arrived with — two 10px flecks, five rows clear of
the hoof, inflating its height from 219 to 235.

    pip install Pillow

    # frog: upright poses to a common height, sit and rest left at their own
    python3 tools/normalize_sprites.py \
        assets/sprites_src/frog_{stand,walk_a,walk_b,weary}.png -o assets/sprites
    python3 tools/normalize_sprites.py \
        assets/sprites_src/frog_{sit,rest}.png -o assets/sprites --no-scale

    # goat: one height for all six, raised to keep the horns above the figure
    python3 tools/normalize_sprites.py \
        assets/sprites_src/goat_*.png -o assets/sprites --height 198

Two knobs decide how a species is framed, and both are per species.

`--no-scale` aligns the baseline without rescaling, for poses that are
legitimately shorter and squatter. The frog's sit and rest need it. The goat's
do not: all six goat poses were drawn at one scale, and its crouch is already in
the art — `goat_rest` drops 11% skull-to-foot while its horns keep the overall
height the same, so uniform scaling preserves the crouch on its own.

`--height` is what matches one species to another, and it is **not** the same
number for each. The code art keeps a constant 48px figure and lets ears and
horns stick out above it — that is why goats get a `lift` of 9. Sprites follow
the same rule, so the measurement that must match across species is *skull top
to feet*, not total silhouette. The frog's raised eye domes sit 8.3% above its
skull; the goat's horns sit 16.1% above its own. That 7.3% gap is the whole
adjustment: 185 x 1.073 = 198. The result:

| pose | skull-to-foot |
|---|---|
| frog stand | 44.4px |
| goat stand, walk_a, walk_b | 44.1px |
| goat sit, weary | 43.8px |
| goat rest | 40.0px (crouched, as drawn) |

All twelve share a baseline exactly.

Then bake the result into the single file:

    python3 tools/embed_sprites.py

Raw art lives in `assets/sprites_src/`, normalized output in `assets/sprites/`,
and the copy the game actually draws from is the `SPRITE_DATA` block at the
bottom of `index.html`. It is generated — never hand-edit it. Only the species
listed in `SPRITE_SPECIES` get embedded, so art for a species that is not wired
up yet costs nothing; it still resolves to its `assets/sprites/` path, which
works when the folder is served, so new art can be tried before it is baked in.
Twelve poses cost 550KB of art and 734KB encoded, putting `index.html` at 915KB.
All six species would land around 2.7MB — fine for a file read off disk, but if
it ever needs to come down, the `lit` overlays in `derivePose` are the cheapest
thing to drop.

## The loop

- **Souls**, one integer currency, with an honest trailing-60s average rate.
- **The bonfire.** After the first cycle it opens at full flame. A recruit
  arrives every 5s until the pool holds **8** —
  12 with Widen the Circle fully paid, 14 behind the Wider Fire unlock. The
  light seats **5**, rising to 8. Each guest takes a seat, pays on sitting
  down, rests 20s, then leaves for a **30-second expedition**. Fewer and
  larger: at twenty figures nobody was individually recognisable.
- **Depth.** Survive and depth goes up by one, and a rest pays
  `perRest x (1 + depth/2)` — a depth 4 veteran is worth three fresh arrivals.
  Depth is where the money is and depth is what kills them.
- **The spiral.** A death costs a permanent `-0.10` survival and halves depth
  rather than resetting it, so dying never restores an adventurer to safety.
  Each death makes the next one likelier. Red pips under every figure count
  the deaths against the three they get.
- **Hollowing is a moment, not a condition.** Three deaths (four with the
  Herbalist) and they drop, drain of colour and stop. **They remain for 30
  seconds** — 60 with the Ossuary at 2 — while a ring drains around them on the
  ground, the only countdown in the game. Tap inside that window and both
  actions are offered side by side. Let it expire and they stand and walk into
  the dark on their own: the seat frees, the name enters the kept dead, and the
  ash is paid anyway. **Never more than three on screen at once**; a fourth
  makes the oldest leave immediately. Nothing accumulates, so there is no wall
  of grey and nothing to administrate.
- **Rekindling.** `150 x 1.6^n` clears one hollow and returns them at depth 0,
  deaths forgiven. Souls into growth, or souls into repair.
- **Counsel.** Tap a resting adventurer for their depth, deaths, live survival
  odds and next payout. **Send shallow** runs their next expedition one layer
  short: safer, poorer, and no new depth. Tap a hollow to offer them the rite.
- **The road bar.** A compact horizontal strip under the status line, one band
  per location, a marker per adventurer sinking through their band as they
  travel and flashing at ambushes and discoveries. Tapping it opens the map.
  Tap a marker to ring **the bell**: they come home immediately and alive, no
  deeper than they left, and they pay you nothing. It costs more every time.
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
  are thrown back, take a death, and drop what they had. The bar under the
  status line is the road; tapping it opens the map, its markers open the
  place.
- **The flame.** 0 to 100, decaying always. The living circle feeds it and only
  those who can reach a seat feed it fully; the ones out on the road feed it at
  a third. **Each hollowing takes a one-time bite** of `5 + peak depth x 0.25`,
  so the fire lurches when someone goes instead of dragging on a background
  count. At zero the fire is out and the run is over.
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

No sound. Everything on the canvas is flat shapes and outlines, drawn by hand
in the file.

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
pull instead of removing it: **48.9 minutes**, inside the 35-50 window. *v5
removed the continuous pull altogether, so this level had nothing left to sell;
it now buys time to decide instead — the window doubles from 30 seconds to 60.*

**v5: the flame pressure had to be rebuilt from scratch.** Hollows used to
accelerate decay continuously, and that background drag was the run's whole
pressure. Nothing accumulates now, so it is gone. The spec's suggested
replacement — a flat 6-intensity spike per hollowing — gave 23-to-33-minute
runs, well short of the window. Grid-searching hearth value against spike size
lands on `HEARTH 0.0074`, `5 + peak x 0.25`: a median of **40.2 minutes** over
40 simulated runs, 15 hollowings, 18,600 souls earned — close enough to v4.1
that the ash unlock costs need no rebalancing. Measured live, a spike on a
peak-8 adventurer takes 7 points off the bar, which is the "clearly felt,
roughly 5%" the spec asked for.

**A full circle does hold the fire.** Measured in game at eight alive and five
seats, the flame *gains* 0.47 intensity a minute; at four home and four on the
road it sits at -0.18, effectively flat. With all eight out it loses 0.98 a
minute. The pressure is that they are on the road, not that the circle is
small.

**v5.1's pacing, measured.** Beats 1-3 land at **25 seconds** for someone who
taps and about **82** for someone who never does, against the spec's 90-second
ceiling. The full ten-beat sequence, played live end to end: beat 4 at 37s,
beat 5 at 47s, the flame bar and depth at 80s, the first find at 81s, the first
death at 3.2m, the first hollow at 4.1m and Build at 4.6m — a low-tail run; the
simulated median puts beat 9 at 8.3 minutes.

**v5.1 needed one balance change, and it was the seat.** Beat 4 promises that
buying the first Kindled Flame "adds a seat", and it did not: the seat term
floored `flame level / 2`, so level 1 bought nothing visible but a wider light.
Rounding it instead gives the first purchase a seat and shifts every odd level
one earlier. Re-simulated over 40 runs that moves the run from 40.2 to **37.9
minutes** — still inside the 35-50 window, so nothing else was retuned.

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

Hand it to someone who has never seen it and say nothing at all. **At ten
minutes, do they know what the game is about without having asked anything?**
Any question they ask is a missing beat.

Then, still:

One full cycle on a phone. **Can you tell every single one of them apart
without tapping anything?** If not, the roster is still too large, however good
the figures look. That is why the pool came down from twenty to eight and why
garment colour is assigned to stay unique rather than rolled at random.

The older test still stands underneath it. Play twenty minutes.
1. **When someone reached two deaths, did you watch them?**
2. **When they hollowed, did you care?**

Yes then no means the anticipation works and the loss is too cheap. No to the
first means the pips are not readable enough — a presentation problem, not a
balance one.
