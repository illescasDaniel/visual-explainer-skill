# visual-explainer

Turns a codebase or system into an interactive visual page: a map of the components, what depends on what, and how data
flows through them. The agent reads the real source, builds one self-contained HTML page (click a component to inspect
it, pick a flow to follow numbered steps, light and dark themes, works on a phone) and publishes it. By default that is
a private Claude Artifact. With `github-page` it creates a static site in `docs/` and enables GitHub Pages with `gh`,
while making sure the folder never ends up in your binary, package or module zip.

It is an [Agent Skill](https://agentskills.io) (a `SKILL.md` plus an HTML template and a small script), so it works in Claude Code, Codex,
Cursor and any other agent that loads skills. The Artifact mode needs an agent with Claude's Artifact tool (Claude Code desktop or claude.ai); `github-page` mode works with any
agent that has `git` and the `gh` CLI.

## How it works

| Step | What happens |
|------|--------------|
| **Analyze** | Reads entry points, wiring, interfaces and main flows; collects files, responsibilities, limits and failure handling. |
| **Build** | Fills `templates/flow-map.html` with the verified components, edges and 2 to 4 flows. |
| **Artifact (default)** | Publishes a private page and hands you the link. No project files change. |
| **`github-page`** | Wraps the page as `docs/index.html`, excludes `docs/` from the project's package (Go, npm, Python and Rust covered), commits, pushes, enables Pages from `/docs`, and checks the site answers with 200. |

It asks before committing, pushing or enabling Pages unless you already said to.

## Usage

```text
/visual-explainer                      # private Artifact of this project's architecture
/visual-explainer github-page          # the same page on GitHub Pages
/visual-explainer the data flow of the sync engine
```

## Install

### Any agent: the `skills` CLI

```bash
npx skills add illescasDaniel/visual-explainer-skill
```

It asks which agents to install for and whether to install into the current project or globally. Non-interactive:
`npx skills add illescasDaniel/visual-explainer-skill -a claude-code -a codex -y`, plus `-g` for global.

### By hand

Copy the `skills/visual-explainer` folder into your agent's skills directory.

| | Project (shared with your team) | All your projects |
|---|---|---|
| Claude Code | `.claude/skills/visual-explainer/` | `~/.claude/skills/visual-explainer/` |
| Codex | `.agents/skills/visual-explainer/` | `~/.agents/skills/visual-explainer/` |
| Cursor | `.cursor/skills/visual-explainer/` | `~/.cursor/skills/visual-explainer/` |

## Contributing

Issues and pull requests are welcome. The skill is deliberately short: if a change makes `SKILL.md` longer, it should
earn it.

## License

MIT, see [LICENSE](LICENSE).
