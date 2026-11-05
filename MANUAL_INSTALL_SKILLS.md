# Skills that need a manual install

These directory entries have no `/plugin install` command (they use git clone, a setup script, npx/uv, or a manual copy), so `.claude/settings.json` can't enable them. Run these yourself after reading each repo: they are unreviewed third-party code.

| # | Name | Install steps | Link |
|---|---|---|---|
| 1 | **gstack** | `git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack`<br>`cd ~/.claude/skills/gstack`<br>`./setup --prefix` | https://github.com/garrytan/gstack |
| 2 | **paperclip** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/paperclipai/paperclip |
| 3 | **Scrapling** | `pip install "scrapling[ai]"`<br>`claude mcp add scrapling -- "$(which scrapling-mcp)"` | https://github.com/D4Vinci/Scrapling |
| 4 | **archify** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/tt-a1i/archify |
| 5 | **rtk** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/rtk-ai/rtk |
| 6 | **awesome-claude-skills** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/ComposioHQ/awesome-claude-skills |
| 7 | **oh-my-openagent** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/code-yeongyu/oh-my-openagent |
| 8 | **claude-code-best-practice** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/shanraisshan/claude-code-best-practice |
| 9 | **scientific-agent-skills** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/K-Dense-AI/scientific-agent-skills |
| 10 | **cherry-studio** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/CherryHQ/cherry-studio |
| 11 | **t3code** | `npx t3@latest` | https://github.com/pingdotgg/t3code |
| 12 | **awesome-copilot** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/github/awesome-copilot |
| 13 | **book-to-skill** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/virgiliojr94/book-to-skill |
| 14 | **Claude-Code-Game-Studios** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/Donchitos/Claude-Code-Game-Studios |
| 15 | **cognee** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/topoteretes/cognee |
| 16 | **invisible_dots** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/feder-cr/invisible_dots |
| 17 | **cli** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/googleworkspace/cli |
| 18 | **nanoclaw** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/nanocoai/nanoclaw |
| 19 | **distilly** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/titanwings/distilly |
| 20 | **nocobase** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/nocobase/nocobase |
| 21 | **SkillSpector** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/NVIDIA/SkillSpector |
| 22 | **notebooklm-py** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/teng-lin/notebooklm-py |
| 23 | **SkillOpt** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/microsoft/SkillOpt |
| 24 | **kubesphere** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/kubesphere/kubesphere |
| 25 | **eigent** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/eigent-ai/eigent |
| 26 | **prompt-master** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/nidhinjs/prompt-master |
| 27 | **Skill_Seekers** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/yusufkaraaslan/Skill_Seekers |
| 28 | **memU** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/NevaMind-AI/memU |
| 29 | **OpenCreator** | ✅ Installed 2026-11-05 into `.claude/skills/` (video priority). | Copy the skill folder into `.claude/skills/` per the README | https://github.com/krillinai/OpenCreator |
| 30 | **agent-desktop** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/vercel-labs/agent-desktop |
| 31 | **hive** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/aden-hive/hive |
| 32 | **drawio-skill** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/Agents365-ai/drawio-skill |
| 33 | **Claude-Red** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/SnailSploit/Claude-Red |
| 34 | **openrig** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/mvschwarz/openrig |
| 35 | **awesome-agentic-ai-zh** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/WenyuChiou/awesome-agentic-ai-zh |
| 36 | **google-maps-scraper** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/gosom/google-maps-scraper |
| 37 | **skills** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/browser-act/skills |
| 38 | **modlens** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/liustack/modlens |
| 39 | **claude-code-guide** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/zebbern/claude-code-guide |
| 40 | **appllama-skills** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/Appllama/appllama-skills |
| 41 | **Continuous-Claude-v3** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/parcadei/Continuous-Claude-v3 |
| 42 | **pinme** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/glitternetwork/pinme |
| 43 | **drama-skills** | ✅ Installed 2026-11-05 into `.claude/skills/` (video priority). | Copy the skill folder into `.claude/skills/` per the README | https://github.com/zenstory-ai/drama-skills |
| 44 | **ctf-skills** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/ljagiello/ctf-skills |
| 45 | **Claude-Code-Everything-You-Need-to-Know** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/wesammustafa/Claude-Code-Everything-You-Need-to-Know |
| 46 | **pstack** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/backnotprop/pstack |
| 47 | **agent-rules-books** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/ciembor/agent-rules-books |
| 48 | **delegate-skills** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/amElnagdy/delegate-skills |
| 49 | **Deep-Research-skills** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/Weizhena/Deep-Research-skills |
| 50 | **claude-code-my-workflow** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/pedrohcgs/claude-code-my-workflow |
| 51 | **awesome-claude-plugins** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/quemsah/awesome-claude-plugins |
| 52 | **gpt-image2-ppt-skills** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/JuneYaooo/gpt-image2-ppt-skills |
| 53 | **eCommerce-Skills** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/nexscope-ai/eCommerce-Skills |
| 54 | **sno-station** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/sno-ai/sno-station |
| 55 | **Skills-Manager** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/jiweiyeah/Skills-Manager |
| 56 | **claude-council** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/hex/claude-council |
| 57 | **ai-maestro** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/23blocks-OS/ai-maestro |
| 58 | **claude-smart** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/ReflexioAI/claude-smart |
| 59 | **claude-code-java** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/decebals/claude-code-java |
| 60 | **nWave** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/nWave-ai/nWave |
| 61 | **abide** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/coldteadotai/abide |
| 62 | **ok-skills** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/mxyhi/ok-skills |
| 63 | **llm-council-skill** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/gcpdev/llm-council-skill |
| 64 | **ai-marketing-claude-code-skills** | Copy the skill folder into `.claude/skills/` per the README | https://github.com/BrianRWagner/ai-marketing-claude-code-skills |
| 65 | **skill-video-studio** | ✅ Installed 2026-11-05 into `.claude/skills/` (video priority). | Copy the skill folder into `.claude/skills/` per the README | https://github.com/aaitor/skill-video-studio |
| 66 | **marketing-skills** | Marketplace name clashes with another repo, add it under its own name: `/plugin marketplace add irinabuht12-oss/marketing-skills`<br>`/plugin install marketing-skills@ryze` | https://github.com/irinabuht12-oss/marketing-skills |
| 67 | **pm-skills** | Marketplace name clashes with another repo, add it under its own name: `/plugin marketplace add phuryn/pm-skills`<br>`/plugin install pm-product-discovery@pm-skills` | https://github.com/phuryn/pm-skills |
