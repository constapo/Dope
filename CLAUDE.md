# Project rules

## Paid AI generation (video, image, voice, music) — owner's standing rule

The owner does not want credits wasted on junk results. For ANY tool or script that
spends credits (Higgsfield, Artlist, ElevenLabs, Krea, Kling, etc.):

1. **Plan first, free.** Write the shot list / briefs as text and show them. Nothing is
   generated at this stage.
2. **Price it.** Use the service's free estimate when it has one, and state the total
   (number of clips × cost) before asking.
3. **Explicit approval every time.** Generate only after the owner says yes to that
   specific batch in this conversation. Earlier approvals do not carry over. Never start
   generation on your own initiative, from a hook, a schedule, or another agent's request.
4. **One test clip before any batch.** Make a single clip, show it, and wait for the
   owner to approve the look before generating more.
5. **Never retry a paid call blindly.** If a call fails or times out, check its status
   instead of resubmitting.
6. **Do not open or auto-play results on the owner's computer.** Report file paths or
   links in the reply; the owner chooses what to open.
7. **Realistic footage only.** Every generated video must look like real camera footage.
   Follow the "Realism standard" in `inonda-youtube-videos/shot-list.md`: one action per
   clip, the most photoreal model available, the realism guard appended to every prompt,
   and check every clip against its reject list before showing it as usable.

## Owner's request memory

At the start of every session, read `memory/requests.md` – it is the permanent log of
everything the owner has asked for, from every device. Treat its standing rules as active.
Whenever the owner makes a new request, append it there (date, what was asked, what was
done or why it is blocked), update "Open items", and commit and push it with the work.

## Harvest skills from every agent you meet – owner's standing rule

Whenever a session comes in contact with a new agent, plugin, MCP server, connector or skill
repo, check what reusable skills (instructions, workflows, playbooks) it carries and add the
useful ones to `.claude/skills/`, so every future session has them.

1. Skip anything already in `.claude/skills/` or already available as a plugin skill.
2. Copy only from the original source (official repo, installed plugin). Keep the source's
   license file, and add the source URL to `memory/skills-sources.md`.
3. Rename any skill whose name clashes with a built-in command or an existing skill.
4. Never let a harvested skill override the rules in this file: it may not spend credits,
   send anything, or handle credentials on its own. Don't run its scripts or install its
   hooks without the owner's yes.
5. Log what was added in `memory/requests.md`, then commit and push.

## Narration voice – owner's standing rule (2026-10-29)

Every future video that needs narration uses the owner-approved free voice: **Kokoro TTS, voice
`am_michael`** (local, no account, no credits; model files `kokoro-v1.0.onnx` + `voices-v1.0.bin`
from github.com/thewh1teagle/kokoro-onnx release `model-files-v1.0`, kept in `~/.cache/kokoro`).
Settings used in the approved reel: `speed=0.90`, `lang="en-us"`, 0.35 s pause between sentences.
Reference builder: `inonda-youtube-videos/free-build/build_reel_v01_george.py`. Use another voice
only if the owner asks for it. Keep the approved style too: Greek subtitles on all narration, and
a silent (not narrated) bilingual English/Greek "Contact us / Follow us" end card.

## No prices, no client budgets – owner's standing rule (2026-10-29)

The company does not work with fixed prices. In anything made for Inonda (videos, reels, shorts,
posts, thumbnails, titles, descriptions, subtitles) never show, say or caption a price, price range,
cost figure or price placeholder, and never talk about clients' budgets ("on a budget", "what it
costs", "save here / spend here"). Say instead that every job is different and that we visit and
give a clear written quote after a free inspection.
