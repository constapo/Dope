# TEMPLATE — VHS tape for a Claude Code (terminal) beat. Copy to projects/<slug>/<beat>.tape and edit.
# Run via scripts/capture-terminal.sh (installs vhs+ttyd once, re-encodes for HyperFrames seeking).
# https://github.com/charmbracelet/vhs — `.tape` is to the terminal what hero-script.js is to the browser.
#
# SANITATION — the terminal's "no-PII on screen" gate (same rule as capture step 2):
#   • Record in a clean throwaway dir: the host path shows in the prompt line AND in tool calls.
#   • `unset CLAUDE_CODE_CHILD_SESSION` — else a nested run shows "transcript saving is off …".
#   • Escape after the turn — dismisses onboarding popups ("Teach auto mode about your environment?").
#     A late popup can still flash at the very tail (Escape doesn't always land first). If a capture catches
#     one, cap that beat's data-duration in the composition to just BEFORE it — deterministic, no re-capture.
#   • The "N MCP servers need authentication" line comes from your GLOBAL config — the launch line below
#     hides it by aliasing `claude` to `claude --strict-mcp-config` (ignores all other MCP config). The alias
#     is defined in the hidden section, so the RECORDED command stays a clean `claude`, not the flag.
#   • A LIVE model turn is NON-DETERMINISTIC (wording + surprise popups vary run to run). For a polished,
#     repeatable cut, script a fixed answer (the HTML-terminal re-enactment seam in composition.html)
#     or record a good take and trim. Live capture = most authentic; re-enactment = most controllable.

Output beat.mp4          # capture-terminal.sh re-encodes this in place (dense keyframes)
Set FontSize 20
Set Width 1600           # match the browser capture (viewport) so beats stitch without letterboxing
Set Height 900
Set Padding 24
# Set Theme "Builtin Dark"   # optional; the default (charm) already renders the Claude Code TUI cleanly

Hide
Type "cd {{DEMO_DIR}} && unset CLAUDE_CODE_CHILD_SESSION && alias claude='claude --strict-mcp-config' && clear"
Enter
Sleep 400ms
Type "claude"
Enter
Sleep 4s
Enter                    # accept the folder-trust prompt if shown (otherwise a harmless empty submit)
Sleep 2s
Show

Sleep 700ms
Type "{{PROMPT}}"        # e.g. Find me an AI weather agent I can call and pay for
Sleep 1s
Enter
Sleep 13s                # long enough for the turn you want on screen (tune per prompt)
Escape                   # dismiss any popup before the beat ends
Sleep 1s
