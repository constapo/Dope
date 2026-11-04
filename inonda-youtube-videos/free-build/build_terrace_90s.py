#!/usr/bin/env python3
"""90 s short "Leaking terrace / flat roof: the waterproofing repair" (from script v04).

Same house rules as the tile reel: real-looking stills only, handheld phone at chest height, no faces,
free sources only (AI Horde), no prices or budgets, Inonda LTD logo top-left, Kokoro am_michael voice,
Greek subtitles, silent bilingual end card.

Usage:
  python3 build_terrace_90s.py prompts            # prints "name<TAB>prompt" lines for horde.sh
  python3 build_terrace_90s.py STILLS_DIR OUT_DIR # builds the video from one image per scene name
"""
import sys

from build_tiles_photo import main

COMMON = ("only gloved hands and forearms visible if any, nobody's face, smartphone photo from chest height, "
          "level horizon, real house in Cyprus, bright Mediterranean daylight, photorealistic, 26mm lens")
NEGATIVE = ("person, face, head, man, woman, people, legs, feet, shoes, silhouette, cartoon, illustration, "
            "drawing, painting, 3d render, cgi, top-down view, overhead view, aerial view, drone view, view from "
            "ceiling, fisheye, text, watermark, logo, blurry, deformed hands, extra fingers")

# (still, spoken English, Greek subtitle, on-screen label, zoom from, zoom to, slide x, slide y, picture prompt)
SCENES = [
    ("dampwall", "Damp patches under your terrace?", "Υγρασία κάτω από τη βεράντα σας;", "BEFORE · ΠΡΙΝ", 1.00, 1.10, 0.0, 0.0,
     "interior white wall corner just below the ceiling with brown damp stains, bubbling and peeling paint, black mould spots, eye level view of the wall"),
    ("drip", "Every rain, the same leak comes back.", "Σε κάθε βροχή, η ίδια διαρροή επιστρέφει.", "BEFORE · ΠΡΙΝ", 1.04, 1.04, -0.5, 0.0,
     "a plastic bucket on a tiled living room floor catching dripping water, wet floor around it, damp stain on the wall behind"),
    ("terrace_old", "The problem starts up on the terrace.", "Το πρόβλημα ξεκινά πάνω στη βεράντα.", "BEFORE · ΠΡΙΝ", 1.00, 1.08, 0.3, 0.0,
     "old flat roof terrace of a Cypriot house with worn cracked terracotta tiles, weeds growing in the joints, stained low parapet walls, blue sky"),
    ("cracks", "Cracked tiles and failed joints let the water in.", "Σπασμένα πλακάκια και φθαρμένοι αρμοί αφήνουν το νερό να μπει.", "BEFORE · ΠΡΙΝ", 1.06, 1.00, 0.0, 0.2,
     "close view of cracked old terracotta terrace tiles, crumbling grout joints, dirt and moss in the cracks, looking down at the terrace floor"),
    ("drain", "Blocked drains make it worse.", "Τα φραγμένα σιφόνια το κάνουν χειρότερο.", "BEFORE · ΠΡΙΝ", 1.00, 1.08, 0.0, 0.0,
     "a blocked terrace floor drain full of dry leaves and dirt, a puddle of stagnant water around it on old terrace tiles"),
    ("inspect", "First, we find exactly where the water gets in.", "Πρώτα βρίσκουμε ακριβώς από πού μπαίνει το νερό.", "", 1.04, 1.04, 0.5, 0.0,
     "gloved hand pressing a digital moisture meter against an old terrace tile, the meter display visible, old terrace floor"),
    ("removal", "Then the old tiles come off, down to the slab.", "Μετά τα παλιά πλακάκια βγαίνουν, μέχρι την πλάκα.", "", 1.00, 1.08, 0.0, 0.2,
     "gloved hands with a chisel and hammer lifting old terracotta terrace tiles, broken tile pieces and dust, bare concrete showing underneath"),
    ("slab", "The concrete is cleaned and repaired.", "Το μπετόν καθαρίζεται και επισκευάζεται.", "", 1.05, 1.00, -0.4, 0.0,
     "bare grey concrete flat roof slab swept clean, a few cracks freshly filled with repair mortar, a broom leaning on the low parapet wall"),
    ("primer", "A primer goes on, so the membrane bonds.", "Περνάμε αστάρι για να κολλήσει η μεμβράνη.", "", 1.00, 1.07, 0.4, 0.0,
     "gloved hand rolling clear primer with a paint roller on a bare grey concrete roof slab, wet primed area shining, a bucket of primer"),
    ("tape", "Corners and joints get reinforcing tape.", "Γωνίες και αρμοί παίρνουν ενισχυτική ταινία.", "", 1.06, 1.00, 0.0, 0.2,
     "gloved hand brushing liquid waterproofing over white reinforcing fabric tape along the corner where the roof slab meets the parapet wall"),
    ("coat1", "Then the first coat of waterproofing membrane.", "Μετά η πρώτη στρώση στεγανωτικής μεμβράνης.", "", 1.00, 1.08, 0.5, 0.0,
     "gloved hand rolling grey liquid waterproofing membrane over the concrete flat roof with a long roller, half the terrace coated, bucket of membrane"),
    ("coat2", "A second coat, up the walls as well.", "Δεύτερη στρώση, και πάνω στους τοίχους.", "", 1.04, 1.04, -0.6, 0.0,
     "flat roof terrace fully coated with a smooth light grey waterproofing membrane continuing up the low parapet walls, fresh glossy finish, blue sky"),
    ("newdrain", "Every drain is sealed into the membrane.", "Κάθε σιφόνι σφραγίζεται μέσα στη μεμβράνη.", "", 1.00, 1.08, 0.0, 0.0,
     "a new clean stainless steel terrace drain sealed into a light grey waterproofing membrane with a reinforced collar around it"),
    ("watertest", "We flood test it, to prove it holds.", "Κάνουμε δοκιμή με νερό για να αποδείξουμε ότι αντέχει.", "", 1.03, 1.03, 0.6, 0.0,
     "flat roof terrace with shallow clear water pooled on top of a light grey waterproofing membrane for a flood test, reflections of the blue sky"),
    ("terrace_new", "Then the terrace is finished, ready to use.", "Μετά η βεράντα ολοκληρώνεται, έτοιμη για χρήση.", "AFTER · ΜΕΤΑ", 1.00, 1.08, 0.4, 0.0,
     "finished flat roof terrace of a Cypriot house with new light beige anti-slip outdoor tiles, clean white parapet walls, potted plants, sea view, sunny"),
    ("drywall", "Inside, the walls stay dry.", "Μέσα, οι τοίχοι μένουν στεγνοί.", "AFTER · ΜΕΤΑ", 1.05, 1.00, 0.0, 0.0,
     "freshly painted clean white interior wall corner below the ceiling, no stains, bright living room, eye level view of the wall"),
    ("rain", "Rain comes, and runs straight to the drain.", "Έρχεται η βροχή και τρέχει κατευθείαν στο σιφόνι.", "AFTER · ΜΕΤΑ", 1.00, 1.07, -0.3, 0.2,
     "rain falling on a finished terrace with light beige anti-slip tiles, rainwater flowing along the slight slope into a clean drain, wet reflective surface"),
    ("terrace_new2", "A dry home, season after season.", "Ένα στεγνό σπίτι, κάθε εποχή.", "AFTER · ΜΕΤΑ", 1.03, 1.12, 0.5, 0.3,
     "finished terrace with light beige anti-slip tiles at golden hour, table and two chairs, plants, sea view in the distance, nobody on the terrace"),
]
LINES = [s[:8] for s in SCENES]

if __name__ == "__main__":
    if sys.argv[1:] == ["prompts"]:
        for s in SCENES:
            print(f"{s[0]}\t{s[8]}, {COMMON}")
    else:
        main(sys.argv[1], sys.argv[2], LINES, "Inonda_Terrace_Waterproofing_90s_PREVIEW.mp4")
