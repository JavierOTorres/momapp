# Sanctuary — vertical slice v2

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
- **The strip.** Every adventurer currently below is a marker descending a
  track down the left, carrying their depth and their scars, with ambushes and
  discoveries flashing as they go. Tap one to ring **the bell**: they come home
  immediately and alive, no deeper than they left, and they pay you nothing.
  It costs more every time.
- **Artifacts.** Survivors drag things back — 12% a run, +3% per layer, capped
  at 45%. Finds land filthy in a tray of 6; fill it and the next one is left
  where it lay. Drag across a find to **dust** it, and its form, material and
  glyph surface: the slot, the rarity, and whether it is cursed. All three lie
  about a quarter of the time.
- **Testing and being wrong.** At the fire, sound it to narrow the slot, heat
  it for rarity, bleed it for the curse. Each test costs more than the last on
  that piece and more again if it looks valuable. Name it whenever you like —
  there is no confirmation and no safety net. A cursed ring filed as blessed
  does exactly what it truly is to whoever you hand it to, and the label only
  corrects itself after three expeditions.
- **Gear.** Three slots per adventurer, effects applied to their survival,
  their scar, and their purse. What they wear when they die stays at that
  depth until someone survives a run that deep; what they wear when they
  hollow is gone.
- **The Archive.** A third tab. Plain-language entries for every mechanic,
  locked to their names until the thing has happened to you.
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

**One balance target is not met.** Guessing every artifact outearns testing
them by roughly a third over 30 simulated minutes, and does not cost
measurably more hollows, so testing does not yet pay for itself in aggregate.
Its value is targeted rather than average — knowing one specific ring is
cursed before handing it to a depth 6 veteran — and an aggregate simulation
cannot see that. Worth watching in play before moving the numbers.

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
