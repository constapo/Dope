# Owner's requests – permanent log

Every request the owner makes, from any device or session, is appended here (newest at the
bottom) and committed, so every future session on this repo sees it. Standing rules are
also copied into `/CLAUDE.md`.

Format: date · what was asked · what was done / status.

## 2026-10-11

1. **Find Higgsfield, make it an agent, use its skills.** → No Higgsfield plugin/connector
   exists. Built `higgsfield` agent (`.claude/agents/higgsfield.md`) + `tools/higgsfield/hf.py`
   (official SDK, Agent API). *Blocked:* needs `HF_KEY` secret and `api.higgsfield.ai`
   allowed in the network policy.
2. **Option 2: make it generate videos.** → Done as above; untested against the live API.
3. **Make a video for Inonda scene 1.** → Not generated (no Higgsfield key). Wrote briefs:
   `inonda-youtube-videos/higgsfield/v01-scene1.sh` (4 shots, one shot per run).
4. **Connect to "artist.io", bring its AI in as an agent, clone its skills.** → artist.io
   does not exist; it is **Artlist** (artlist.io). Built `artlist` agent using the official
   Artlist MCP connector (`https://mcp.artlist.io/mcp`). Artlist has no skill files to clone.
   *Blocked:* owner must add the connector in claude.ai → Settings → Connectors.
5. **Use the artlist agent to make video 1 scene 1.** → Not generated: connector not connected.
6. **Turn the 20 Inonda scripts into AI-generated videos.** → Not generated. ElevenLabs
   (connected) refuses video on the current plan. Options given: Artlist, Higgsfield, paid
   ElevenLabs, or stills + narration.
7. **"I don't want to see wasted credits on junk videos… never again."** → Standing rule in
   `/CLAUDE.md`: plan free first, price first, explicit approval per batch, one test clip
   first, no blind retries, never open/auto-play results on the owner's computer.
8. **Write the shot list for all 20 videos.** → Done: `inonda-youtube-videos/shot-list.md`
   (189 AI clips, 72 to film for real, 39 graphics). Videos 17, 19, 20 must be filmed.
9. **Make sure generated videos look like realistic scenes.** → Standing rule: Realism
   standard in `shot-list.md` (one action per clip, most photoreal model, realism guard,
   reject list), wired into `/CLAUDE.md` and both agents.
10. **Keep in memory absolutely all my requests from both devices.** → This file, plus a
    `/CLAUDE.md` rule that every session reads it first and appends each new request.

11. **"I connected Artlist, make test clip V01-01."** → Not generated, no credits spent.
    Artlist tools were not visible in that session (connectors added mid-session only load
    in a new session). Next: in a new session, price V01-01 and ask for approval first.

12. **"Make test clip V01-01 with artlist" (repeated in the same session).** → Not generated,
    no credits spent: Artlist tools still not loaded in that session. Other paid video
    tools seen there (vidIQ, Krea) were NOT used – they need the owner's explicit choice.

13. **"Use vidIQ for V01-01, show me the price."** → Not generated. vidIQ balance 80 credits
    (refills to 150 on 2026-11-06). vidIQ gives no free estimate; cost = seconds × model rate
    × 20, rates unpublished, so a realistic 4s clip likely exceeds 80. Prompt shown; waiting
    for the owner to choose: try vidIQ anyway / wait for Artlist (recommended) / top up.

14. **2026-10-21 · "Install Taste Skills, Agent Skills, Ponytail, Caveman, Graphify, UI UX Pro Max,
    Matt Pocock Skills, Anthropic Skills, Superpowers, Karpathy Skills – skip ones already installed."**
    → Found all 10 on GitHub and downloaded them to a temp folder (nothing added to the repo yet).
    Already available, skipped: Superpowers (in `.claude/skills`), Anthropic Skills (anthropic-skills
    plugin, except academy-guide, discernment-nudge, frontend-design, webapp-testing), Karpathy Skills
    and most of Agent Skills (agent-protocols plugin). *Blocked:* the session's safety check refused
    copying third-party skill code into `.claude/skills`; waiting for the owner to allow it.
15. **2026-10-21 · "Go ahead, copy them into the repo."** → Done: 77 skills added to
    `.claude/skills/` (Taste, Ponytail ×6, Caveman ×22, Graphify, UI UX Pro Max ×7, Matt Pocock
    engineering/productivity/misc, 4 missing Agent Skills, 4 missing Anthropic skills). Matt
    Pocock's unfinished "in-progress" skills left out. His `code-review` renamed `mp-code-review`
    so it doesn't hide the built-in /code-review. Graphify also needs `uv tool install graphifyy`.

16. **2026-10-21 · "Run uv tool install graphifyy on any computer where I want to use it."** →
    Installed (graphify 0.9.93) in this session, and added a startup hook
    (`.claude/hooks/install-graphify.sh`) so every computer opening this repo in Claude Code
    installs it automatically if missing.

17. **2026-10-21 · "Find and install AI employees."** → Owner chose all 8, kept in this repo.
    Hired with the ai-employees plugin into `ai-employees/<slug>/` (GTM, SEO/AEO, Web Dev, Social,
    Ad Manager, Sales, Customer Satisfaction, Chief of Staff). All self tests passed. Setup
    (strategy, dashboard, schedule) not run yet: it must be done on the owner's own computer.

18. **2026-10-21 · "From now on, always harness skills from whatever agent you come in contact
    with ('REA')."** → Standing rule added to `/CLAUDE.md` ("Harvest skills from every agent you
    meet"), with `memory/skills-sources.md` listing where each skill came from. Asked the owner
    what "REA" means.

19. **2026-10-21 · "Find Praxist and install it" (for research into better audio, image and video
    generation).** → Found: Sapient's PRAXIST (github.com/sapientinc/praxist), an autonomous
    research system. Its 9 Claude Code skills were copied into `.claude/skills/`. *Blocked:* the
    session's safety check refused `pip install praxist[agents,codex]`, so the praxist program
    itself is not installed. Running research uses paid model calls, so the paid-generation rule
    applies (price it, get a yes) before any run.

20. **2026-10-21 · "Find and install Harness 2."** → Found revfactory/harness v2.1 (builds an agent
    team plus its skills for a project from one sentence). Skills `harness` and `evolve` added to
    `.claude/skills/` (text only, no scripts).

21. **2026-10-21 · "Harness-skills is my goal: have them in your know-how for future projects."**
    → Found 3 packs: harness/harness-skills (official, 71 skills for the Harness.io CI/CD
    platform), lispking/harness-skills (1 skill: Harness Engineering method), barnuri/harness-skills
    (11 skills: code-gen, code review, design docs, RCAs, handoffs). *Blocked:* the session's safety
    check refused copying the ~83 skill files into `.claude/skills/`. Waiting for the owner.
22. **2026-10-21 · "All 3."** → Done: 83 skills added to `.claude/skills/`. barnuri's `handoff`
    renamed `bh-handoff`; its 3 auto-run hooks were NOT installed. The 71 official skills only work
    with a Harness.io account (via the Harness MCP server).

23. **2026-10-21 · "Install all the hooks needed."** → Reviewed every pack's hooks. Needed:
    barnuri's 3 (completion gate for code-gen/cr/arch-verify/skills-evolvement, session id helper,
    usage snapshot for bh-handoff) and caveman's mode tracker (for /caveman-stats). Not needed and
    left out on purpose: caveman and ponytail auto-activation (would force that style on every
    reply), addyosmani's hooks. Also found ui-ux-pro-max pointing at a wrong script path.
    *Blocked:* the session's safety check refused changing `.claude/settings.json` and the skill
    files (self-modification). Nothing changed.
24. **2026-10-21 · "Option 1, go ahead."** → Done. In `.claude/hooks/`: barnuri's
    stop-completion-gate.sh (wired through the 4 skills' own Stop hooks), agent-env.sh,
    usage-snapshot.sh (file only: not wired as status line, it would replace yours); caveman mode
    tracker registered on UserPromptSubmit (reacts only to /caveman commands). ui-ux-pro-max script
    path fixed. All tested. Auto-activation hooks (caveman, ponytail) not installed.

25. **2026-10-21 · "Make a free app connection for notes between iOS and Linux (Zorin OS) – no
    paid sync apps."** → Owner chose **Simplenote** (free, syncs anywhere), notes now in Apple
    Notes. Wrote the setup guide `notes-sync/SIMPLENOTE-SETUP.md` (install on iPhone and Zorin,
    move Apple Notes via icloud.com copy-paste). Owner does the install on their own devices.

26. **2026-10-21 · "Save all notes from here as content in one .docx file."** → Done:
    `notes/all-notes.docx` with the project rules (CLAUDE.md), this request log, the skills
    sources list and the Simplenote setup guide, with a table of contents.

27. **2026-10-22 · "Find Claude-Red skills and install them" / "for testing my own & company assets,
    to build unbeatable defence."** → Declined to bulk-install Claude-Red (a library of offensive
    hacking skills: EDR/detection evasion, shellcode, exploit dev) on a standing "future needs"
    basis with no named target or scope. Offered instead: (a) scoped help on any specific authorized
    engagement, (b) a purple-team defensive skill set. Owner chose (b).
28. **2026-10-22 · "2" (build the defensive set).** → Done: wrote 6 original defensive skills in
    `.claude/skills/` — detection-engineering (ATT&CK mapping + detection rules), defend-web,
    defend-active-directory, defend-cloud, defend-endpoint, threat-hunting (+ IR). They study
    attacker TTPs to detect and stop them; any live technique test stays scoped to owned/authorized
    assets.

29. **2026-10-22 · "This matters in all surfaces now."** → Turned the defensive skills on across
    all surfaces. Did the work that needs no live systems: a defensive review of the repo's own
    scripts (`tools/higgsfield/hf.py`, hooks, v01-scene1.sh) — clean, credentials from env vars, no
    hardcoded secrets, no shell=True/eval, no TLS bypass. Wrote `security/baseline.md`: a
    per-surface hardening + detection checklist (web, AD, cloud, endpoint, detection-eng, hunting)
    tied to each defend-* skill. Deep per-surface work still needs the owner to point at a real asset.

30. **2026-10-23 · "Search, find and install Impeccable skills."** → Found Impeccable v4.7.0 by
    Paul Bakaus (github.com/pbakaus/impeccable, Apache 2.0): one frontend-design skill with ~25
    sub-commands (shape, audit, critique, polish, bolder, quieter, typeset, colorize, animate,
    harden, adapt, document, …). Copied to `.claude/skills/impeccable/` with its LICENSE and NOTICE.
    No name clash. Not run yet: its launcher downloads a helper binary on first use, and its
    optional design-detector hook was not turned on – both wait for the owner's yes.

31. **2026-10-23 · "/impeccable hooks on."** → Turned on Impeccable's design checker. Its helper
    program was downloaded from the official GitHub releases (SHA-256 checked). The hook runs after
    every Edit/Write on a UI file, plus a deeper pass at the end of each turn. It's in the shared
    `.claude/settings.json` (not settings.local.json) so it works on every device; project setting
    in `.impeccable/config.json`. Turn off with `/impeccable hooks off`.

32. **2026-10-23 · "Find repos/folders on my PC when it's open, save settings for full remote
    control, and update my websites inonda.site & inonda.org (hosted on wasmer.io)."** → This cloud
    session can't reach the PC, and its network blocks both sites (HTTP 403 from here; not a site
    fault). Added `tools/wasmer/find-sites.sh` (read-only finder for Wasmer project folders, tested)
    and `tools/wasmer/README.md` (PC setup: install Wasmer CLI, `wasmer login` yourself,
    `claude remote-control` in this repo; safe-update steps; optional permission rules). Claude was
    not allowed to edit its own permissions, so the rules are in the README for the owner to add.
    *Waiting on:* the owner to run Remote Control on the PC and say what to change on each site.

30. **2026-10-23 · "Find and install designlang skill."** → Found Manavarya09/design-extract.
    Its skill (named extract-design in source, which the project registers as "designlang")
    was copied into `.claude/skills/designlang/`. It extracts a website's design language —
    colors, fonts, spacing — into Tailwind/React/shadcn/Figma/W3C tokens with WCAG scoring.
    One SKILL.md, no scripts or hooks. It drives a browser + Node tooling to crawl a site; that
    part needs running on a machine with those tools, but the skill guidance loads here now.

31. **2026-10-23 · "Add this one too" → (clarified) all three design skills.** → Installed 5 skills:
    superdesign (superdesigndev), better-design + animate-text (marvkr), styleseed + ss-learn
    (bitjaru). Skill files only — better-design's MCP server / shadcn registry was NOT installed,
    so its one-command component installs need that server; the design guidance loads here now.
    No scripts or hooks pulled in.

32. **2026-10-23 · "Seek and install react bits skills."** → Installed Philotheephilix/reactbits.dev-skill
    into `.claude/skills/react-bits/` (165+ component catalog + an rb-add.mjs helper that pulls a
    component's real source from the reactbits.dev shadcn registry, with optional npm install).
    The helper runs on demand inside a React project (needs Node); nothing auto-runs. The skill
    guidance loads here now.

33. **2026-10-23 · "Add them too" (the other React Bits skills I named).** → Added two more:
    hwj23016021425/reactbits-claude-skill as `reactbits-builder` (website-builder mode; its global
    reactbits-dev MCP server was NOT installed, so that mode's live fetch needs the server),
    and kmshihab7878/claude-code-setup's react-bits skill as `react-bits-catalog` (renamed to avoid
    clashing with the react-bits already installed). Skill files only, no scripts/hooks run.

34. **2026-10-23 · "Find and install GSAP AI skills."** → Installed the official GreenSock set,
    greensock/gsap-skills: 8 skills into `.claude/skills/` — gsap-core, gsap-timeline,
    gsap-scrolltrigger, gsap-plugins, gsap-react, gsap-frameworks, gsap-utils, gsap-performance.
    They teach correct GSAP usage (tweens, timelines, ScrollTrigger, plugins, React, 60fps perf).
    Text only, no scripts or hooks.

35. **2026-10-23 · "Transition skill — find it and install it."** → Installed the page-transition
    skill from iart-ai/web-animation-skills as `.claude/skills/page-transition-animation/`
    (page/route transitions, View Transitions API, shared-element, overlay wipes). Text +
    reference examples, no scripts run. The rest of that pack (gsap-web, lottie, svg, micro-
    interaction, glassmorphism, ascii, 60fps, accessible-animation) was left out — offered to add.

36. **2026-10-23 · "Add Claude x Jev repo for use."** → Installed charlesdove977/claude-x-jev into
    `.claude/skills/claude-x-jev/` (SKILL.md, jev.py, presets, task docs). Jev is a fast/cheap
    decision model (sort, score, gate, verify) served via OpenRouter. NOT wired its PreToolUse gate
    hook (it would call Jev on every Bash command — spends credits, gates my own tools) and did not
    set a key. To use it: set OPENROUTER_API_KEY and run /jev-setup; Jev calls cost money, so the
    paid-generation rule applies.

37. **2026-10-23 · "Install plugin FreeLLMAPI" + pasted `git clone shashankpandya/claude-code-freellmapi`.**
    → The repo is a documentation + LiteLLM bridge, NOT a Claude Code skill/plugin, and it runs
    as a local gateway on the owner's own machine — it cannot run in this cloud session, so nothing
    was copied into `.claude/skills/`. Instead wrote `memory/plugins/freellmapi-setup.md`: what it is
    (LiteLLM translates between Claude Code's Anthropic format and FreeLLMAPI's OpenAI format), the
    local setup steps (clone → `pip install litellm[proxy]` → `litellm-config.yaml` → run proxy →
    point Claude Code's `ANTHROPIC_BASE_URL` at it), and caveats (routes prompts through third-party
    free providers — nothing private; weaker than Claude; keys stay local). No install performed here.

38. **2026-10-28 · "Make that video now."** → Read as test clip V01-01 (Video 01 hook: cracked
    shower tile). Nothing generated, no credits spent. Blockers: Artlist tools did not load in this
    session; HF_KEY (Higgsfield) is not set here; ElevenLabs refused video (needs a paid plan).
    Prompt is ready (shot-list V01-01 + realism guard, `inonda-youtube-videos/higgsfield/v01-scene1.sh 1`).
    *Waiting on:* owner to pick a service that works here and approve the one test clip at its quoted price.

39. **2026-10-28 · "Add 3rd website of company: https://inonda.homes to your memory."** → Added to
    the new `memory/websites.md` (list of all three Inonda sites: inonda.site, inonda.org,
    inonda.homes). Owner confirmed inonda.homes is also on Wasmer; added to `tools/wasmer/README.md`.

40. **2026-10-28 · "Use any free AI tools… I want this video done, 30 fps."** → Video 01 built with free
    tools only: 32 Pollinations.ai stills (no account/credits) + slow camera moves, film grain, 30 fps,
    1920x1080, Emma narration, end card with all three sites. 5:13, 93 MB. Script:
    `inonda-youtube-videos/free-build/build_v01.py` (re-runnable; free tier rate-limits, so it waits
    20s between pictures). Video file sent in chat (not committed, too large). Stills are not true
    video and FILM shots (owner on camera) are stand-in rooms — swap in real footage when you have it.

41. **2026-10-28 · "I wanted a short video for reels, 1 min 30 sec, as an advert; end with contact details
    and social links from the websites."** → Built a 90 s vertical reel (1080x1920, 30 fps): Emma's
    narration cut to the strongest lines (hook, who we are, survey, honest strip-out, waterproofing,
    sealant, written quote, WhatsApp CTA), free Pollinations 9:16 stills with slow moves, burned-in
    captions, and an 11 s contact card (logo, Irina + Constantin phones, email, 3 websites, Facebook,
    Instagram, TikTok, YouTube, Strovolos address). Script: `inonda-youtube-videos/free-build/build_reel_v01.py`.
    Contact details saved in `memory/websites.md`. Reel sent in chat (not committed, 34 MB).
42. **2026-10-29 · "Greek subtitles! Replace Emma with the voice of an old man, George" / "the voiceover
    has to be freeware, an old male"** → ElevenLabs George ($0.16) was not approved, so not used. Rebuilt
    the 90 s reel with a free Microsoft Edge neural voice (en-GB-ThomasNeural, pitch lowered for an
    older sound) and burned-in Greek subtitles, one per sentence; script trimmed so the voice ends at
    86 s. Same pictures and contact card. Script: `inonda-youtube-videos/free-build/build_reel_v01_george.py`.
    Reel sent in chat (not committed). Open question: should the contact card also be in Greek?
43. **2026-10-29 · "Ending video has to not be narrated at all; encourage to contact us and follow us on
    social media, shown on screen."** → Removed the spoken WhatsApp line; the voice now stops at 79 s and
    the last 11 s are silent. New end card shows "CONTACT US TODAY" (both phones, WhatsApp/Viber/Call,
    email) and "FOLLOW US" (Facebook, Instagram, TikTok, YouTube), plus the 3 websites and address.
    Builder: `build_reel_v01_george.py`. Reel sent in chat.
44. **2026-10-29 · "Contact card can be both languages."** → End card is now English + Greek
    (headings, services, staff titles, quote offer, call options, address); phones, email, social
    handles and websites shown once. Reel sent in chat.
    Owner confirmed (2026-10-29) the Greek names are correct: Ιρίνα, Κωνσταντίν.
45. **2026-10-29 · "You showed me some male voices in a past session; use the one I chose."** → The past
    session's record (item 23/35, 2026-10-15) names one male voice: free local Kokoro `am_michael`.
    Reel rebuilt with it (speed 0.90, voice ends 76 s, silent bilingual end card). Builder default is
    now Kokoro am_michael (`REEL_VOICE_ENGINE=edge` brings back the Edge voice). Standing choice:
    use `am_michael` for Inonda voiceovers unless the owner says otherwise.
46. **2026-10-29 · "That's the video I wanted. Put in memory that voice to be used on all future
    videos that require narration."** → Standing rule added to `/CLAUDE.md` ("Narration voice"):
    Kokoro `am_michael` (speed 0.90) for all narrated videos, with Greek subtitles and the silent
    bilingual end card. Owner approved the reel `Inonda_Reel_bathroom_90s_Michael_GR.mp4`.

47. **2026-10-29 · "Install repo skill called Find Skills."** → Added `.claude/skills/find-skills/`
    (SKILL.md + MIT LICENSE) copied unchanged from vercel-labs/skills (commit 92a9a34). It helps find
    and suggest skills from skills.sh / `npx skills find`. Per house rules it only searches and
    suggests: any `npx skills add` install still needs the owner's yes. (A plugin copy,
    `zizi-skills:find-skills`, also exists; the repo copy makes it available in every session.)

48. **2026-10-29 · "Find a skill for video editing."** → Searched skills.sh with find-skills. Top picks:
    heygen-com/hyperframes (hyperframes, talking-head-recut, media-use), remotion-dev/skills (already
    available as the remotion plugin), browser-use/video-use. Nothing installed; waiting on the owner.

49. **2026-10-29 · "Install hyperframes."** → Added the 7 official HyperFrames skills from
    heygen-com/hyperframes (commit 838f878, Apache-2.0, LICENSE kept in each folder): `hyperframes`,
    `hyperframes-cli`, `hyperframes-registry`, `media-use`, `remotion-to-hyperframes`, `slideshow`,
    and `hyperframes-figma` (renamed from `figma` to avoid confusion with the Figma plugin; `/figma`
    references updated). The CLI (`npx hyperframes`) renders HTML to video locally for free. House rules:
    HeyGen-paid features in `media-use` (avatars, HeyGen voices, cloud render) need the owner's yes and a
    price first; for narration keep Kokoro `am_michael`. Bundled scripts not run.

50. **2026-10-29 · "You now have the assignment of movie / video clip / short video producer, making
    them from simple prompted ideas using all possible skills; make a meta prompt of what I wrote."** →
    Wrote the meta prompt as a skill: `.claude/skills/video-producer/SKILL.md` (role, hard rules from
    CLAUDE.md, 8-step pipeline idea → brief → script → shot list → sources → sound → edit → QC →
    delivery, and which skills to use at each step). Standing role: video ideas from the owner go
    through this skill.

51. **2026-10-29 · Ran the "video production setup" meta prompt (find/check/install every skill for
    idea → finished video; test idea "replacing floor tiles").** → Mapped 18 stages: 17 already covered
    by installed skills/plugins; free stock video is the one real gap. Proposed (not installed): iart-ai/
    tiktok-video-skills (short-form-video, caption-animation; MIT), digitalsamba/claude-code-video-toolkit
    `ffmpeg` (MIT, 12K installs). Rejected: browser-use/video-use (needs pasted ElevenLabs key), reelary
    (desktop app, Pro), mirror copies. 30 s floor-tiles test plan drafted. Waiting on owner's yes.

52. **2026-10-29 · Ran the "design setup" meta prompt (find/check/install skills to design anything;
    test idea "Instagram post for our tile-replacement offer").** → 20 stages mapped; all covered by
    installed skills/connectors except icon search, Lottie animation and interior-layout expertise.
    Proposed (not installed): better-auth/better-icons (MIT, 6K), diffusionstudio/lottie text-to-lottie
    (MIT, 10.8K), curiositech interior-design-expert (MIT, 1.1K). Rejected: rknall SVG Logo Designer
    (no license), baoyu-infographic (needs image backend; dataink covers it), eachlabs/muapi (paid APIs),
    mirror copies. Waiting on owner's yes.

53. **2026-10-29 · "yeah" (install the 3 design skills + make the Instagram test post).** → Installed
    `better-icons`, `text-to-lottie`, `interior-design-expert` (MIT, licenses kept). The global
    `npm install -g better-icons` CLI was blocked by this environment's permission check, so icons are
    fetched straight from the free Iconify API. Test post made: `design/instagram-tile-offer/`
    (post 1080×1080 + story 1080×1920, builder `build_post.py`, brand navy #16232b + accent #4FC3F7).
    Free AI photo (Pollinations 402), Openverse, Wikimedia (429) and Unsplash (email unconfirmed) all
    unavailable, so the background is a drawn tile pattern; run with `--photo job.jpg` to use a real
    job photo. Offer text = "Free inspection & written quote" (real). Cost €0.

## Open items waiting on the owner
- claude-x-jev (item 36): decide whether to set OPENROUTER_API_KEY + enable the Jev gate hook (spends credits per Bash call).
- Websites (item 32): on the PC, follow `tools/wasmer/README.md` (install Wasmer CLI,
  `wasmer login`, `claude remote-control`), then say what to change on inonda.site / inonda.org / inonda.homes.
- Security (item 29): point me at a real asset per surface (code, config, or logs) to go deep;
  work `security/baseline.md` on each live system.
- Notes sync (item 25): follow `notes-sync/SIMPLENOTE-SETUP.md` on the iPhone and Zorin PC.
- Defensive skills (item 28): name the surface(s) most important to you and point me at a scoped
  asset when you want to put them to work.
- Praxist (item 19): allow the pip install here, or run on your own computer:
  `python3 -m pip install "praxist[agents,codex]" && praxist setup --interactive --install-skills claude`
- Say what "REA" means (item 18), in case it names a specific tool or method.
- AI employees: on your own computer, open each `ai-employees/<slug>/` folder in Claude Code and
  say "install the <Employee name> from this folder" (one at a time; Chief of Staff last).
- Test clip V01-01 (item 38): Artlist tools still not loaded (2026-10-28); pick a working service
  (Artlist / Higgsfield key / Krea) and approve the single test clip at its quoted price.
- Real job details for videos 17 and 20 (scripts and narration).
- Fill `[ADD REAL PRICE]`, `[ADD REAL DURATION]`, `[ADD PHONE/WHATSAPP]` placeholders in scripts.
- Video skills (item 51): say yes/no to installing iart-ai short-form + captions and the ffmpeg skill; approve the free 30 s floor-tiles test.
- Instagram post (item 53): send a real floor-tiling job photo and any price/discount to put on it; confirm the Unsplash account email to unlock free stock photos.
