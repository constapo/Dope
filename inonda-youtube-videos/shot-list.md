# Inonda – AI shot list for all 20 videos

Planning document only: **nothing here has been generated and no credits have been spent.**
Generation follows the credit rule in `/CLAUDE.md`: price first, your approval per batch,
one test clip before any batch.

Built from the B-roll notes in `scripts/v01.md`–`v20.md`.

## How to read it

Every shot is one of three kinds:

| Tag | Meaning | Costs AI credits? |
|---|---|---|
| **AI** | Generic B-roll an AI video model can make: materials, defects, tools, hands at work, Cyprus homes. | Yes – 1 clip each |
| **FILM** | Must be real footage you shoot: the owner on camera, real Inonda jobs, real clients, real before/after. Faking these with AI would mislead viewers, and the scripts themselves say "genuine footage only". | No |
| **GFX** | Text, icons, checklists, subscribe animations, end screens – made in the video editor. | No |
| **REUSE** | Reuses another AI clip from the same video. | No |

Rules for every **AI** shot:
- 5 seconds, 16:9, no on-screen text, no logos, no brand names.
- **Hands and tools only – no faces.** AI people must never look like Inonda staff or clients.
- Add a small on-screen "illustration" label wherever an AI shot could be mistaken for a real
  Inonda job (the scripts already ask for this in video 13).
- Append the shared style below to every prompt.

**Shared style (append to every AI prompt):**
> Photorealistic, handheld documentary look, natural Mediterranean daylight, warm slightly
> desaturated tones, shallow depth of field, typical Cyprus home (white render, flat roofs,
> 1990s ceramic tiles, aluminium windows), no faces, no on-screen text, no logos.

Then append the **realism guard** from the Realism standard below.

## Realism standard (applies to every AI shot)

The goal is footage a viewer takes for real handheld phone/camera B-roll, never "AI video".

**Prompting**
- **Camera height and angle (owner rule):** always handheld phone at chest/hand height
  (about 1.2–1.5 m), level horizon, looking slightly down at the floor or straight at the work,
  as a person standing in the room would film it. Never top-down, overhead, from the ceiling,
  drone, crane or floor-level. Add to every prompt: "filmed handheld on a smartphone at chest
  height, level horizon, standing eye-line, slightly downward angle".
- **Never drawings, cartoons, animation or illustrated stand-ins** — not even for previews.
  A preview uses real photos/clips or one approved real-looking test clip.
- **One subject, one action, one camera move per clip.** Where a shot below lists several
  actions separated by ";" or ",", generate only the first one by default. Splitting it into
  more clips needs your approval, because it costs more.
- Describe it like a camera operator, not an artist: real lens (35mm or 50mm), real light
  source (window daylight, overcast sky, low sun), real camera move (slow handheld push-in,
  slight hand shake, static tripod).
- Ordinary, lived-in detail: slight dust, scuffs, uneven grout, real-world clutter at the
  frame edge. No showroom perfection, no glossy CGI surfaces.
- Real Cyprus materials and fittings: white-rendered concrete, terrazzo or 1990s ceramic
  tiles, aluminium windows, solar water heaters, flat roofs.
- Use the most photoreal video model the service offers, never "fast", "draft" or
  stylised models.

**Append to every prompt (realism guard):**
> Shot on a real camera, natural imperfect lighting, realistic physics and textures,
> real-world scale, subtle handheld movement. Avoid: CGI, 3D render, cartoon, illustration,
> oversaturated colours, glowing light, slow-motion, warped hands, extra fingers, melting
> objects, garbled text, watermarks.

**Reject the clip (do not use it, do not pay to "fix" it blindly) if you see:**
- Hands with wrong finger counts, tools merging into hands, objects morphing or melting.
- Water, paint or sealant that flows unnaturally (upwards, sideways, like gel).
- Visible garbled text, signs, labels or logos.
- Plastic/CGI-looking surfaces, impossible light, warped walls or tiles.
- Anything that looks like a real person's face.

The test clip is checked against this list before you're asked to approve the look. A
rejected test clip is reported to you with the reason; it is not regenerated without your
approval.

## Totals

| Video | Title (short) | AI | FILM | GFX |
|---|---|---|---|---|
| 01 | Bathroom renovation, old to new | 13 | 3 | 2 |
| 02 | Old apartment to modern rental | 12 | 3 | 2 |
| 03 | Kitchen renovation on a budget | 11 | 3 | 3 |
| 04 | Leaking roof or terrace repair | 12 | 2 | 2 |
| 05 | Damp walls and mould in winter | 11 | 3 | 2 |
| 06 | Roof & terrace before the rainy season | 11 | 2 | 1 |
| 07 | Salt air damage on coastal homes | 11 | 3 | 1 |
| 08 | Keeping a Cyprus house cool | 11 | 3 | 1 |
| 09 | What drives bathroom renovation cost | 9 | 4 | 2 |
| 10 | Repair or replace: boilers, windows, floors | 10 | 3 | 3 |
| 11 | Mistakes hiring a contractor | 8 | 3 | 3 |
| 12 | How to read a renovation quote | 8 | 4 | 3 |
| 13 | Holiday home maintenance while abroad | 11 | 3 | 1 |
| 14 | Cheap upgrades for landlords | 11 | 2 | 2 |
| 15 | Pre-purchase inspection checklist | 11 | 3 | 2 |
| 16 | Seasonal maintenance calendar | 12 | 2 | 2 |
| 17 | Job of the week (real case study) | 3 | 8 | 2 |
| 18 | 10 quick home repairs | 11 | 3 | 2 |
| 19 | Behind the scenes at Inonda | 3 | 7 | 1 |
| 20 | A job that went wrong (real case study) | 0 | 8 | 2 |
| **All** | | **189** | **72** | **39** |

189 AI clips ≈ 15.8 minutes of generated footage. **Price this before approving** – the
cost depends on which service (Artlist, Higgsfield, paid ElevenLabs) and which model.

Suggested order: video 01 test clip (V01-01) → approve look → rest of video 01 → review →
videos 02–16 and 18 in batches you approve. Videos 17, 19 and 20 are real case studies and
should be filmed, not generated.

---

## Video 01 – Full Bathroom Renovation in Cyprus: Old to New
Narration: `audio/Inonda_Video01_narration_Emma.mp3` (7:10)

| ID | Section | Type | Shot |
|---|---|---|---|
| V01-01 | Hook | AI | Slow push-in close-up on a cracked, chipped beige wall tile beside a shower, grout stained dark. |
| V01-02 | Hook | AI | Camera tilts up to a bathroom ceiling corner with a brown damp stain, peeling paint and black mould spots. |
| V01-03 | Hook | AI | Overhead shot of an old shower tray, murky water draining very slowly around a corroded drain grate. |
| V01-04 | Hook | AI | Quick dolly-in reveal of the same bathroom renovated: light-grey large porcelain tiles, walk-in glass shower, floating vanity, warm LED mirror. |
| V01-05 | Intro | FILM | Owner standing in the doorway of the old bathroom. |
| V01-06 | Intro | AI | Wide establishing shot of a white-rendered Cyprus apartment block street in morning sun. |
| V01-07 | Survey | AI | Hand pressing a moisture meter against a stained bathroom wall, display reading high. |
| V01-08 | Survey | AI | Torch beam tracing old galvanised pipework inside an opened wall cavity. |
| V01-09 | Strip-out | AI | Hands laying protective floor sheeting in a hallway, then a chisel lifting old wall tiles, dust in the light. |
| V01-10 | Plumbing | AI | Close-up of a pressure-test gauge on new copper/PEX supply pipes, needle holding steady. |
| V01-11 | Waterproofing | AI | Roller applying grey waterproof membrane on a shower floor; brush pressing reinforcing tape into the wall corner. |
| V01-12 | Tiling | AI | Notched trowel combing adhesive on a wall, a large tile pressed in, spirit level placed on top. |
| V01-13 | Tiling | AI | Slow close-up of a smooth white sealant bead being run along a shower corner. |
| V01-14 | Fixtures | AI | New chrome tap turned on over a white basin, clear water running; shower running onto clean tiles. |
| V01-15 | Fixtures | FILM | Owner doing the walkthrough. |
| V01-16 | Cost & end | FILM | Owner on camera; final reveal of the real finished bathroom. |
| V01-17 | Mid CTA | GFX | Subscribe lower third over V01-12. |
| V01-18 | End | GFX | End screen: next video "Old apartment to modern rental". |

## Video 02 – Old Cyprus Apartment to Modern Rental
Narration: `audio/Inonda_Video02_narration_Emma.mp3`

| ID | Section | Type | Shot |
|---|---|---|---|
| V02-01 | Hook | AI | Dim, dated living room with brown furniture and closed shutters, dust in a thin beam of light. |
| V02-02 | Hook | AI | Same room renovated and bright: white walls, light floor, shutters open, natural light pouring in. |
| V02-03 | Intro | AI | Exterior of a 1980s Cyprus apartment block with balconies, slow pan to a front door. |
| V02-04 | Intro | FILM | Owner walking in through the door. |
| V02-05 | Walkthrough | AI | Close-up of an old electrical consumer unit with dated fuses, torch light across it. |
| V02-06 | Walkthrough | AI | Hand struggling to close an old aluminium window that sticks and leaves a gap. |
| V02-07 | Damp | AI | Bubbling, flaking paint over a damp patch on a corner wall, slow push-in. |
| V02-08 | Electrics/plumbing | AI | Hands fitting a modern consumer unit; then an outdoor AC unit being mounted on a bracket. |
| V02-09 | Floors & walls | AI | Paint roller laying fresh white paint on a wall, then large floor tiles laid on adhesive. |
| V02-10 | Floors & walls | AI | Hands swapping old kitchen cabinet doors for new matt white fronts. |
| V02-11 | Finishing | AI | Light switches flicked on in a finished living room; roller blinds lowered. |
| V02-12 | Finishing | AI | Phone held up photographing a bright, staged living room for a rental listing. |
| V02-13 | Cost/montage | FILM | Real finished apartment, room by room. |
| V02-14 | End | AI | Close-up of a key turning in a new front-door lock. |
| V02-15 | Walkthrough | FILM | Owner with notebook and moisture meter. |
| V02-16 | Mid CTA / End | GFX | Subscribe animation; end screen. |
| V02-17 | End | GFX | End screen card. |

## Video 03 – Kitchen Renovation on a Budget
Narration: `audio/Inonda_Video03_narration_Emma.mp3`

| ID | Section | Type | Shot |
|---|---|---|---|
| V03-01 | Hook | AI | Tired 1990s kitchen: worn wood-effect cabinets, chipped laminate worktop, old tiles. |
| V03-02 | Hook | AI | Same kitchen updated: new door fronts, light worktop, tiled splashback, under-cabinet lights. |
| V03-03 | Intro | FILM | Owner in the kitchen opening cupboards, pointing at worn surfaces. |
| V03-04 | What can stay | AI | Torch under a sink showing a swollen, water-damaged cabinet base. |
| V03-05 | What can stay | AI | Hand opening and closing drawers, checking runners; tape measure along a wall. |
| V03-06 | Where to save | AI | Screwdriver fitting a new cabinet door; old handles swapped for modern ones. |
| V03-07 | Where to save | AI | Small roller painting a cabinet door; new splashback tiles pressed into adhesive. |
| V03-08 | Where to spend | AI | Worktop samples laid side by side on a table; close-up of a quality mixer tap. |
| V03-09 | Where to spend | AI | Soft-close hinge and drawer runner close-ups; a socket tester plugged into a kitchen socket. |
| V03-10 | Order of work | GFX | Order-of-work graphic. |
| V03-11 | Order of work | AI | Quick sequence: old units removed, new wiring in an open wall, a worktop being lowered into place. |
| V03-12 | Quotes | AI | Hidden old pipe discovered behind a removed cabinet, torch light on it. |
| V03-13 | Quotes | FILM | Owner pointing at an itemised quote line. |
| V03-14 | Cost/end | FILM | Real finished kitchen, angles and details. |
| V03-15 | Cost | AI | Slow pan across a finished budget kitchen, morning light. |
| V03-16 | Mid CTA / End | GFX | Subscribe animation; end screen. |
| V03-17 | End | GFX | End screen card. |

## Video 04 – Leaking Roof or Terrace: Full Repair Process
Narration: `audio/Inonda_Video04_narration_Emma.mp3`

| ID | Section | Type | Shot |
|---|---|---|---|
| V04-01 | Hook | AI | Brown water stain on a white ceiling, a drip falling into a plastic bucket. |
| V04-02 | Hook | AI | Heavy rain hitting a flat Cyprus roof terrace, water pooling. |
| V04-03 | Hook | AI | Quick shot of a freshly coated, dry grey-white roof surface in sunshine. |
| V04-04 | Intro | AI | Wide shot of a sun-baked flat roof with hairline cracks and dried ponding marks, solar heater in background. |
| V04-05 | Inspection | AI | Moisture meter pressed against a stained ceiling. |
| V04-06 | Inspection | AI | Hose gently flooding a small taped-off area of terrace for a water test. |
| V04-07 | Diagnosis | AI | Gloved hand clearing leaves and silt from a blocked roof drain outlet. |
| V04-08 | Diagnosis | FILM | Owner pointing at the defect. |
| V04-09 | Preparation | AI | Pressure washer cleaning a flat roof; scraper lifting old flaking coating. |
| V04-10 | Preparation | AI | Trowel filling a crack with repair mortar. |
| V04-11 | Waterproofing | AI | Brush applying primer; reinforcement fabric pressed into a wall-to-roof corner. |
| V04-12 | Waterproofing | AI | Roller applying liquid waterproofing membrane; detail brushed around a drain outlet and a pipe. |
| V04-13 | Finish & test | AI | Ruler standing in shallow flood-test water on a finished terrace. |
| V04-14 | Prevention/End | FILM | Real dry ceiling below a repaired terrace. |
| V04-15 | Mid CTA / End | GFX | Subscribe animation; end screen. |
| V04-16 | End | GFX | End screen card. |

## Video 05 – Damp Walls and Mould in Winter
Narration: `audio/Inonda_Video05_narration_Emma.mp3`

| ID | Section | Type | Shot |
|---|---|---|---|
| V05-01 | Hook | AI | Handheld shot of a bedroom corner with black mould spots, a cloth wiping it. |
| V05-02 | Hook | AI | Same corner with mould spots back, winter light from the window. |
| V05-03 | Who we are | FILM | Owner walking into a real house room. |
| V05-04 | Who we are | AI | Quick cuts: toolbox opening, moisture meter switched on. |
| V05-05 | Why damp | AI | Exterior of typical Cyprus houses and apartment blocks on a grey winter day. |
| V05-06 | Why damp | AI | Steam rising from a kettle; clothes drying on an indoor rack beside a cold wall. |
| V05-07 | Three kinds | AI | Macro of fine black mould spotting on painted plaster. |
| V05-08 | Three kinds | AI | Ceiling stain with a tide-mark edge. |
| V05-09 | Three kinds | AI | Flaking plaster low on an old stone wall with white salt deposits. |
| V05-10 | Condensation fixes | AI | Extractor fan spinning in a bathroom; window opened briefly; dehumidifier running. |
| V05-11 | Penetrating damp | AI | Cracked render and failed sealant around a window frame; overflowing blocked downpipe. |
| V05-12 | Cleaning mould | AI | Gloved hand cleaning mould with a cloth; paint peeling over a damp patch. |
| V05-13 | CTA / specialist | FILM | Presenter/owner to camera; owner photographing a wall. |
| V05-14 | Mid CTA | FILM | Presenter to camera. |
| V05-15 | Mid CTA / End | GFX | Red-cross overlay; end card. |
| V05-16 | End | GFX | Subscribe end card. |

## Video 06 – Prepare Your Roof and Terrace for the Rainy Season
Narration: `audio/Inonda_Video06_narration_Emma.mp3`

| ID | Section | Type | Shot |
|---|---|---|---|
| V06-01 | Hook | AI | Dry sunny flat roof with solar water heater, blue sky. |
| V06-02 | Hook | AI | Same roof on a rainy day, water pooling around a drain. |
| V06-03 | Why now | FILM | Owner on a safe terrace. |
| V06-04 | Why now | AI | Wide rooftop shot with solar water heater and water tanks. |
| V06-05 | Safety | AI | Stable ladder being footed and secured against a wall; camera pans to a parapet edge. |
| V06-06 | Water paths | AI | Close-up of a clogged drain outlet; gloved hand clearing leaves. |
| V06-07 | Water paths | AI | Bucket of water poured on a terrace, flowing to an outlet; downpipe running to the ground. |
| V06-08 | Surface & joints | AI | Blistered, cracked roof membrane close-up; gap where roof meets parapet wall. |
| V06-09 | Surface & joints | AI | Sealant gun laying a fresh bead around the base of a solar heater frame. |
| V06-10 | Repair options | AI | Patch repair with reinforcement mesh; liquid waterproofing rolled on. |
| V06-11 | Repair options | AI | Finished, freshly waterproofed terrace in sun. |
| V06-12 | Apartment blocks | AI | Bucket under a drip in a stairwell; phone photographing a ceiling stain. |
| V06-13 | CTAs | FILM | Presenter to camera (mid and end). |
| V06-14 | Mid CTA | REUSE | Reuse V06-11 under the subscribe animation (no new clip). |
| V06-15 | End | GFX | End card. |


## Video 07 – Salt Air and Sea-View Damage on Coastal Properties
Narration: `audio/Inonda_Video07_narration_Emma.mp3`

| ID | Section | Type | Shot |
|---|---|---|---|
| V07-01 | Hook | AI | Golden-hour sea view from a balcony, camera pans down to rust stains and flaking paint on the railing base. |
| V07-02 | Why salt | AI | Waves breaking on a Cyprus shoreline; salt crust on a window pane. |
| V07-03 | Why salt | AI | Wide shot of white coastal homes facing the sea. |
| V07-04 | Why salt | FILM | Owner on a coastal street or balcony. |
| V07-05 | Safety & structure | AI | Rusty railing base where it meets concrete; balcony soffit with rust stains. |
| V07-06 | Safety & structure | AI | Spalled concrete with exposed rusted rebar; a hand tapping gently on concrete (nobody leaning on railings). |
| V07-07 | Water out | AI | Cracked sealant around an aluminium window; salt-crusted door threshold. |
| V07-08 | Water out | AI | Cracked render with orange rust bleed. |
| V07-09 | Metalwork | AI | Pitted aluminium frame with white powdery corrosion; rusty gate hinge. |
| V07-10 | Metalwork | AI | AC outdoor unit with corroded fins; corroded outdoor light fitting. |
| V07-11 | Coatings | AI | Hose rinsing salt off a window and railing; painter wire-brushing a railing. |
| V07-12 | Coatings | AI | Wooden pergola with peeling varnish in strong sun. |
| V07-13 | CTAs/planning | FILM | Presenter to camera; owner taking notes on a balcony. |
| V07-14 | Before/after | FILM | Real before/after of a repainted railing. |
| V07-15 | End | GFX | End card. |

## Video 08 – Keeping a Cyprus House Cool in Summer
Narration: `audio/Inonda_Video08_narration_Emma.mp3`

| ID | Section | Type | Shot |
|---|---|---|---|
| V08-01 | Hook | AI | Harsh midday sun on a flat roof, heat haze shimmering. |
| V08-02 | Hook | AI | Hand fanning with a magazine in a hot living room, AC unit running above. |
| V08-03 | How heat gets in | FILM | Owner on camera. Thermal images only if you own the camera – no AI or stock thermal shots. |
| V08-04 | How heat gets in | AI | Strong afternoon sun hitting a west-facing wall of a Cyprus house. |
| V08-05 | Roof | AI | Roller applying a reflective white coating over a dark roof surface. |
| V08-06 | Roof | AI | Insulation boards being laid on a flat roof; solar heater and tanks behind. |
| V08-07 | Shading | AI | External roller shutters closing in bright sun; awning over a south window. |
| V08-08 | Shading | AI | Pergola with a climbing vine casting dappled shade; tree shading a west wall. |
| V08-09 | Windows | AI | Old single-glazed window with daylight visible through a gap; worn rubber seal. |
| V08-10 | Windows | AI | Hands fitting a modern double-glazed window into an opening. |
| V08-11 | Walls & ventilation | AI | Window open at night with curtains moving in a breeze; ceiling fan turning. |
| V08-12 | Walls & ventilation | AI | Sealant gun closing a gap around a window frame. |
| V08-13 | AC / CTAs | FILM | Presenter to camera (mid and end). |
| V08-14 | Mid CTA | FILM | Quote document on a table (blurred). |
| V08-15 | End | GFX | End card. |

## Video 09 – What Drives the Cost of a Bathroom Renovation
Narration: `audio/Inonda_Video09_narration_Emma.mp3`

| ID | Section | Type | Shot |
|---|---|---|---|
| V09-01 | Hook | AI | Two different bathrooms mid-renovation, quick cuts: bare walls, exposed pipes. |
| V09-02 | Hook / end | FILM | Owner to camera in a bathroom (hook and end). |
| V09-03 | Intro | FILM | Owner with notepad and tape measure; real montage of past Inonda work (script: genuine only). |
| V09-04 | Driver 1 | AI | Old toilet and basin being removed; close-up of waste pipes in an open floor. |
| V09-05 | Driver 1 | GFX | Floor-plan sketch with arrows (toilet moved). |
| V09-06 | Driver 2 | FILM | Stripped walls, damp, membrane – the script says "shot on a real job, not stock". |
| V09-07 | Mid CTA | AI | Damp patch on a bathroom ceiling corner. |
| V09-08 | Driver 3 | AI | Tile samples laid side by side; large-format tile being cut with a rail cutter. |
| V09-09 | Driver 3 | AI | Close-ups of chrome taps and shower fittings; handwritten spec list on a clipboard. |
| V09-10 | Driver 4 | AI | Bags of materials carried up a stairwell; waste bags loaded into a skip. |
| V09-11 | Driver 4 | AI | Sequence of hands at work: plumber, electrician, tiler (no faces). |
| V09-12 | Budget | AI | Tape measure, notepad and calculator on a table beside a printed itemised quote. |
| V09-13 | Budget | AI | Slow pan across a finished modern bathroom. |
| V09-14 | Owner | FILM | Owner to camera, finished bathroom. |
| V09-15 | End | GFX | End screen. |

## Video 10 – Repair or Replace? Boilers, Windows and Flooring
Narration: `audio/Inonda_Video10_narration_Emma.mp3`

| ID | Section | Type | Shot |
|---|---|---|---|
| V10-01 | Hook | AI | Old wall boiler with a corroded fitting; condensation between window panes; cracked floor tile. |
| V10-02 | Intro | FILM | Owner in a living room with boiler, window and floor behind. |
| V10-03 | Intro | GFX | Four icons appearing. |
| V10-04 | Boilers | AI | Close-up of a corroded boiler pipe fitting; thermostat dial being turned. |
| V10-05 | Boilers | AI | Solar water heater on a Cyprus roof against blue sky. |
| V10-06 | Mid CTA | AI | Window being opened and closed. |
| V10-07 | Windows | AI | Hand running along a worn window seal; daylight visible through a gap. |
| V10-08 | Windows | AI | Tape measure across a window opening; new window being fitted. |
| V10-09 | Flooring | AI | Screwdriver handle tapping floor tiles to find hollow ones; a tile lifted to show the base. |
| V10-10 | Flooring | AI | Tile samples held against an existing floor; damp patch on a floor. |
| V10-11 | Flooring | AI | Sanding a wooden floor, fine dust in the light. |
| V10-12 | Checklist | GFX | Checklist graphic building up. |
| V10-13 | Checklist | AI | Written quote on a table with two options highlighted. |
| V10-14 | Owner | FILM | Owner to camera (checklist and end). |
| V10-15 | Boilers | FILM | Owner inspecting a boiler. |
| V10-16 | End | GFX | End screen. |

## Video 11 – Mistakes People Make When Hiring a Contractor
Narration: `audio/Inonda_Video11_narration_Emma.mp3`

| ID | Section | Type | Shot |
|---|---|---|---|
| V11-01 | Hook | AI | Half-finished room with tools left on the floor and bare plaster. |
| V11-02 | Hook / intro / end | FILM | Owner to camera. |
| V11-03 | Intro | FILM | Real montage of past Inonda work. |
| V11-04 | Intro | GFX | Title card listing the six mistakes. |
| V11-05 | Mistake 1 | AI | Three printed quotes on a table, highlighter marking a line item. |
| V11-06 | Mistake 2 | AI | Tape measure across a room; phone photographing a damp patch. |
| V11-07 | Mistake 2 | AI | Hand writing a scope list on a notepad. |
| V11-08 | Mistake 3 | AI | Payment schedule table sketched on paper; banking app transfer on a phone (no real names). |
| V11-09 | Mistake 4 | AI | Before-and-after photos swiped on a tablet; handshake at a front door (hands only). |
| V11-10 | Mistake 5–6 | AI | Calendar with dates circled; materials delivery being unloaded. |
| V11-11 | Mistake 5–6 | AI | Change-request note signed by two hands. |
| V11-12 | Mistake 4 | FILM | Real reviews page scrolling (your own reviews only). |
| V11-13 | Mid CTA / End | GFX | Subscribe animation; end screen. |
| V11-14 | End | GFX | End screen card. |

## Video 12 – How to Read a Renovation Quote
Narration: `audio/Inonda_Video12_narration_Emma.mp3`

| ID | Section | Type | Shot |
|---|---|---|---|
| V12-01 | Hook | AI | A one-line handwritten quote on a clipboard. |
| V12-02 | Hook / owner | FILM | Owner to camera holding an itemised quote (hook, red flags, compare, end). |
| V12-03 | Intro | FILM | Owner pointing at the top of a quote. |
| V12-04 | Basics | GFX | Sample quote sections highlighted; checklist ticking. |
| V12-05 | Materials | AI | Tile samples with price tags; a calculator. |
| V12-06 | Materials | AI | Close-up of the word "allowance" circled in pen on a printed quote. |
| V12-07 | Mid CTA | AI | Waterproofing membrane being rolled on a shower floor. |
| V12-08 | Forgotten parts | AI | Rubble bags cleared out; dust sheets laid on a floor. |
| V12-09 | Forgotten parts | AI | Wall calendar; handwritten payment schedule. |
| V12-10 | Red flags | GFX | Red-flag icons over a quote. |
| V12-11 | Compare | AI | Three quotes and a hand-drawn comparison table, highlighter in hand. |
| V12-12 | Compare | AI | Pen ticking items on a printed quote. |
| V12-13 | Owner | FILM | Owner to camera, compare section. |
| V12-14 | Owner | FILM | Owner to camera, end. |
| V12-15 | End | GFX | End screen. |

## Video 13 – Holiday Home Maintenance While You Are Abroad
Narration: `audio/Inonda_Video13_narration_Emma.mp3`

| ID | Section | Type | Shot |
|---|---|---|---|
| V13-01 | Hook | AI | Closed-up Cyprus villa, shutters down, slow push-in to the front door and a key in the lock. |
| V13-02 | Intro | FILM | Presenter to camera outside a property. |
| V13-03 | Intro | AI | Quick cuts: toolbox, a tap, a roof terrace. |
| V13-04 | What goes wrong | AI | Dry sink trap; damp corner (label "illustration"). |
| V13-05 | What goes wrong | AI | Cracked sealant on a window; blocked air vent (label "illustration"). |
| V13-06 | What goes wrong | AI | Overgrown garden path at an empty villa. |
| V13-07 | Good visit | AI | Hands running a tap, flushing a toilet, opening shutters. |
| V13-08 | Good visit | AI | Phone photographing each room; clipboard with a tick list. |
| V13-09 | Keys | AI | Key safe on a wall; labelled keys with tags. |
| V13-10 | Keys | AI | Phone showing a chat thread with room photos (generic, no names). |
| V13-11 | Before you leave | AI | Hand turning the main water valve off; emptied fridge with door propped open. |
| V13-12 | Before you leave | AI | Shutters half-closed; terrace being cleared of pots and furniture. |
| V13-13 | CTAs / limits | FILM | Presenter to camera (mid, limits, end). |
| V13-14 | Limits | FILM | Blank/generic insurance document. |
| V13-15 | End | GFX | End screen. |

## Video 14 – Cheap Upgrades for Cyprus Landlords
Narration: `audio/Inonda_Video14_narration_Emma.mp3`

| ID | Section | Type | Shot |
|---|---|---|---|
| V14-01 | Hook | AI | Two apartment doors side by side: one dull and scuffed, one clean and bright. |
| V14-02 | Intro | FILM | Presenter to camera in a clean rental (intro, mid, which-first). |
| V14-03 | Intro | AI | Keys handed over; viewing in a bright apartment (hands and backs only). |
| V14-04 | Clean & fixed | AI | Paint roller on a wall; hand re-applying white silicone. |
| V14-05 | Clean & fixed | AI | Replacing a door handle; a dripping tap being repaired. |
| V14-06 | Comfort | AI | Technician's hands servicing an AC unit filter; ceiling fan turning. |
| V14-07 | Comfort | AI | Dim room becomes bright as new lights are switched on; blinds fitted. |
| V14-08 | Kitchen/bath/outdoor | AI | New handles on kitchen cabinets; fresh white grout lines. |
| V14-09 | Kitchen/bath/outdoor | AI | Tidy balcony with a small table and two chairs; mosquito screen being fitted. |
| V14-10 | Photos & safety | AI | Phone photographing a living room in daylight. |
| V14-11 | Photos & safety | AI | Smoke alarm on a ceiling being tested; notebook comparing listings. |
| V14-12 | Which first | GFX | Numbered checklist animation. |
| V14-13 | Which first | FILM | Presenter to camera. |
| V14-14 | Hook/upgrade | AI | Bright, clean rental living room, slow pan. |
| V14-15 | End | GFX | End screen with two cards. |

## Video 15 – What to Inspect Before Buying Property in Cyprus
Narration: `audio/Inonda_Video15_narration_Emma.mp3`

| ID | Section | Type | Shot |
|---|---|---|---|
| V15-01 | Hook | AI | Slow golden-hour reveal of a Cyprus villa exterior. |
| V15-02 | Hook | AI | Close-up of a hand tapping a wall. |
| V15-03 | Intro | FILM | Presenter to camera (intro, mid). |
| V15-04 | Intro | AI | Surveyor's hand with a moisture meter (label "illustration"); generic documents on a desk. |
| V15-05 | Water & damp | AI | Terrace with dried water-pooling marks; damp stain on a ceiling. |
| V15-06 | Water & damp | AI | Torch under a sink checking for leaks; age plate on a hot-water tank. |
| V15-07 | Structure | AI | Ruler held against a wall crack; gutter outlet. |
| V15-08 | Structure | AI | Rusty balcony railing; hand testing a window that sticks. |
| V15-09 | Electrics | AI | Electrical panel opened; hand held up to an AC vent. |
| V15-10 | Electrics | AI | Pool pump room; water meter close-up. |
| V15-11 | Questions | AI | Snagging list on a clipboard; defect marked with blue tape. |
| V15-12 | Budget | AI | Calculator and notes on a kitchen table. |
| V15-13 | Questions | FILM | Presenter with a couple in a kitchen (real people, with permission). |
| V15-14 | Budget | GFX | Four-step checklist animation. |
| V15-15 | CTA | FILM | Presenter to camera. |
| V15-16 | End | GFX | End screen. |

## Video 16 – Home Maintenance Calendar: Every Season
Narration: `audio/Inonda_Video16_narration_Emma.mp3`

| ID | Section | Type | Shot |
|---|---|---|---|
| V16-01 | Hook | AI | Same Cyprus house through the seasons: spring blossom, summer glare, autumn rain clouds, winter rain. |
| V16-02 | Hook | AI | Wall calendar pages turning. |
| V16-03 | Intro | FILM | Presenter to camera at a house (intro, mid). |
| V16-04 | Intro | AI | Flat roof, weathered balcony near the sea, a pool. |
| V16-05 | Spring | AI | Hand pointing at a ceiling stain; blocked roof outlet being cleared. |
| V16-06 | Spring | AI | AC filter cleaned; garden irrigation line dripping in spring. |
| V16-07 | Summer | AI | AC filter rinsed under a tap; water tank float valve. |
| V16-08 | Summer | AI | Cracked window sealant; shutters half-closed in strong sun. |
| V16-09 | Autumn | AI | Gutter cleared by a gloved hand; water test on a terrace. |
| V16-10 | Autumn | AI | Hand running along a window seal; outdoor socket cover closed. |
| V16-11 | Winter | AI | Rain on a window; extractor fan running. |
| V16-12 | Winter | AI | Hand wiping mould; smoke alarm test button pressed. |
| V16-13 | Summary | AI | Phone calendar with four seasonal reminders (generic UI). |
| V16-14 | Summary | GFX | Animated checklist. |
| V16-15 | CTA | FILM | Presenter to camera (end). |
| V16-16 | End | GFX | End screen. |

## Video 17 – Job of the Week (real case study)
Narration: **not voiced yet** – script needs real job details first.

This video documents a real Inonda job from call to handover. It must be filmed; AI footage
would present an invented job as real.

| ID | Section | Type | Shot |
|---|---|---|---|
| V17-01 | Hook | FILM | Real problem, phone ringing, van arriving, finished room. |
| V17-02 | Series intro | FILM | Owner on site; genuine past-work montage. |
| V17-03 | First call | AI | Generic phone ringing on a desk beside a notebook (no names). |
| V17-04 | First call | AI | Hand writing questions in a notebook; booking marked on a calendar. |
| V17-05 | Site visit | FILM | Tools actually used; the real defect; owner explaining. |
| V17-06 | Quote | FILM | Real quote (figures blurred); owner at the table. |
| V17-07 | Work | FILM | Work in stages; end-of-day clean-up. |
| V17-08 | Surprise | FILM | Real unexpected issue; owner and client. |
| V17-09 | Handover | FILM | Finished result; walk-through; sign-off. |
| V17-10 | Work | AI | Dust sheets being laid in a hallway (neutral cutaway). |
| V17-11 | Takeaways | FILM | Owner to camera. |
| V17-12 | End | GFX | Recap graphics, WhatsApp card, end screen. |
| V17-13 | Hook | GFX | Title card. |

## Video 18 – 10 Quick Home Repairs Anyone Can Do
Narration: `audio/Inonda_Video18_narration_Emma.mp3`

| ID | Section | Type | Shot |
|---|---|---|---|
| V18-01 | Hook | AI | Fast montage of DIY repairs: silicone, grout, hinge, tap (hands only). |
| V18-02 | Safety / pro / end | FILM | Owner to camera. |
| V18-03 | Safety | GFX | Red-and-white graphic of the three exclusions. |
| V18-04 | Repairs 1–3 | AI | Cutting out old silicone, taping edges, smoothing a new bead. |
| V18-05 | Repairs 1–3 | AI | Scraping and refilling grout between tiles. |
| V18-06 | Repairs 1–3 | AI | Tightening hinge screws; sanding a sticking door edge. |
| V18-07 | Repairs 4–6 | AI | Isolation valve turned off under a sink. |
| V18-08 | Repairs 4–6 | AI | Tap parts laid out on a towel; screwdriver adjusting a cabinet hinge. |
| V18-09 | Repairs 7–8 | AI | Filler applied to a wall hole, sanded, primed and painted. |
| V18-10 | Repairs 7–8 | AI | Bucket under a sink trap; cleaned trap parts; water test. |
| V18-11 | Repairs 9–10 | AI | Toilet cistern lid off, float being adjusted. |
| V18-12 | Repairs 9–10 | AI | AC filters slid out, rinsed, dried and refitted. |
| V18-13 | When to call a pro | FILM | Genuine damp and crack examples (script: genuine footage only). |
| V18-14 | Repairs | AI | Finished neat silicone bead close-up. |
| V18-15 | When to call a pro | GFX | List appearing line by line; WhatsApp card; end screen. |
| V18-16 | End | FILM | Owner to camera. |

## Video 19 – Behind the Scenes at Inonda (real company)
Narration: `audio/Inonda_Video19_narration_Emma.mp3`

About how Inonda really works, so almost everything must be filmed.

| ID | Section | Type | Shot |
|---|---|---|---|
| V19-01 | Hook | FILM | Office or van, tools loaded, owner arriving on site. |
| V19-02 | Intro | FILM | Owner to camera on site; owner at work. |
| V19-03 | Enquiry | AI | Phone with a blurred message; tape measure; notebook (generic). |
| V19-04 | Enquiry | FILM | Photos being taken of a real site. |
| V19-05 | Quote | FILM | Owner explaining a real quote. |
| V19-06 | Quote | AI | Highlighter marking scope lines on a printed quote. |
| V19-07 | Planning | AI | Simple job schedule written on paper beside a planner. |
| V19-08 | Planning / running | FILM | Materials loaded; protection laid; work in progress; end-of-day sweep. |
| V19-09 | Handover | FILM | Walk-through with a client (permitted); care note handed over. |
| V19-10 | End | FILM | Owner to camera. |
| V19-11 | End | GFX | WhatsApp card, end screen. |

## Video 20 – A Job That Went Wrong (real case study)
Narration: **not voiced yet** – needs the real job details.

An honest case study about a real job. No AI shots: invented "defect" or "repair" footage
would undermine the whole point of the video.

| ID | Section | Type | Shot |
|---|---|---|---|
| V20-01 | Hook | FILM | Real defect close-up; owner to camera on site. |
| V20-02 | Why | FILM | Owner to camera; workspace or van. |
| V20-03 | Original job | FILM | Genuine handover photos/footage. |
| V20-04 | What went wrong | FILM | Defect close-ups; return-visit photos. |
| V20-05 | Cause | FILM | Close-ups of the cause; owner to camera. |
| V20-06 | Cause | GFX | Diagram of what went wrong. |
| V20-07 | Fix | FILM | Repair in progress; test; corrected result. |
| V20-08 | What we changed | FILM | New checklist/test in action. |
| V20-09 | End | FILM | Owner to camera. |
| V20-10 | End | GFX | WhatsApp card, end screen. |
