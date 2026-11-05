// TEMPLATE — playwright-cli run-code hero script. Copy to projects/<slug>/capture.js and edit the beats.
// Run via scripts/capture.sh (sets PLAYWRIGHT_MCP_SANDBOX, uses the local binary, converts to MP4).
// Rules that make captures clean and re-runnable:
//   • all-forward navigation (no goBack) so page.screencast survives same-tab route changes
//   • eased scrollTo (below) instead of jumps
//   • real locators: exact a[href="…"] or getByRole; ALWAYS add a fallback so one missing element can't abort
//   • deliberate pauses after each state change; note the cumulative time of each beat → that drives chapter sync
async page => {
  const scrollTo = (y, dur) =>
    page.evaluate(({ y, dur }) => new Promise((res) => {
      const start = window.scrollY, delta = y - start, t0 = performance.now();
      const step = (now) => {
        const p = Math.min(1, (now - t0) / dur);
        const e = p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2; // easeInOutQuad
        window.scrollTo(0, start + delta * e);
        if (p < 1) requestAnimationFrame(step); else res();
      };
      requestAnimationFrame(step);
    }), { y, dur });

  await page.screencast.start({ path: 'capture.webm', size: { width: 1600, height: 900 } });

  // ── Beat 1 — {{BEAT_1_LABEL}} (t≈0) ────────────────────────────────
  await page.waitForTimeout(2600);          // hold on the landing state
  await scrollTo(660, 1900);                // reveal more content
  await page.waitForTimeout(1400);
  await scrollTo(0, 1100);
  await page.waitForTimeout(700);

  // ── Beat 2 — {{BEAT_2_LABEL}} (t≈7.5s) ─────────────────────────────
  await page.getByRole('link', { name: /{{BEAT_2_LOCATOR}}/ }).first().click();
  await page.waitForURL(/{{BEAT_2_URL_MATCH}}/, { timeout: 15000 });
  await page.waitForTimeout(1900);
  await scrollTo(720, 2600);
  await page.waitForTimeout(1300);

  // ── Beat 3 — {{BEAT_3_LABEL}} (t≈13.8s) ────────────────────────────
  const target = page.locator('{{BEAT_3_SELECTOR}}').first();     // e.g. a[href="/catalog/ai-agent-oracle"]
  if (await target.count()) await target.click();
  else await page.locator('{{BEAT_3_FALLBACK}}').first().click(); // e.g. article a[href^="/catalog/"]
  await page.waitForURL(/{{BEAT_3_URL_MATCH}}/, { timeout: 15000 });
  await page.waitForTimeout(2200);
  await scrollTo(1150, 3200);               // scroll through the detail
  await page.waitForTimeout(1300);

  await page.screencast.stop();
}
