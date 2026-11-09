---
name: visual-explainer
description: Analyze a codebase or system and turn it into an interactive visual page (components, dependencies, data flows). Publishes a private Artifact by default; with "github-page" builds a static site in docs/ and enables GitHub Pages. Use when asked to "map the architecture", "show how the data flows", "make an interactive diagram or explainer", or "put it on a GitHub page".
---

# Visual explainer

Read the real source, then show the system as one self-contained, interactive HTML page. Every fact on the page must be
verified in the code; the page is only as good as the analysis behind it.

**Modes.** Default: publish an Artifact (private link). With `github-page` (in the user's words or as the argument): a
static site in the repo's `docs/` folder served by GitHub Pages. Same page either way.

## 1. Analyze

- Read entry points, wiring/composition code, interfaces and the main flows. Use `git ls-files`, not a blind `find`.
- Note for each component: files, job, what it calls, what calls it, the limits and rules worth knowing (timeouts, caps,
  ordering, failure handling). Note external systems and where data lands on disk.
- Pick 2 to 4 flows a reader would ask about (a request, a background job, an install). Each step names one edge.
- Do not modify the project in Artifact mode. Work files go in the scratchpad.

## 2. Build the page

Copy `templates/flow-map.html` and replace only the sample data (`LAYERS`, `COLS`, `NODES`, `EDGES`, `FLOWS`), the
`<title>`, the lede and the one-line rule. It gives a column map, flow tabs with numbered steps, click-to-inspect
components, light and dark themes, and phone width (the map scrolls inside its own box).

- Columns left to right follow the dependency direction. Nodes need at least 56 units between `y` values.
- Edges point from caller to callee; use the double-headed flag only for call-plus-event pairs.
- Name the page after the project, 2 to 4 words (for example "Acme Architecture Map"), no subtitle after a colon.
- If the subject is not a system (a timeline, a comparison), build a different page and keep the same standards.
- Check the script: extract it and run `node --check`. Serve the file on localhost and click one flow tab if a browser
  tool is available.

## 3a. Artifact mode (default)

1. Load the `artifact-design` skill (or run the Artifact tool's `quickstart`) before publishing.
2. Publish the HTML from the scratchpad with the Artifact tool: `icon` (one generic word, e.g. `diagram`) and a one
   sentence `description`.
3. Give the user the link and say it is private until they share it. Offer `github-page` if they want it public.

## 3b. `github-page` mode

Ask before each step that leaves the machine (commit, push, enabling Pages) unless the user already said to do it.

1. **Preflight**: `git status --short`, `git worktree list`, `gh auth status`, `gh repo view --json visibility,defaultBranchRef`.
   Look at `docs/`. If it holds other content or the repo already has Pages, say so and ask. If the repo is private,
   Pages may still be public on some plans: ask.
2. **Write the site**: `python3 <skill>/scripts/make-standalone.py page.html docs/index.html --description "..."`, plus an
   empty `docs/.nojekyll`.
3. **Keep it out of the product.** Find how the project ships (embed directives, package manifests, Dockerfiles, CI
   globs) and make sure `docs/` is not part of it. Verify, do not assume:

   | Stack | Where `docs/` could leak | Fix |
   |---|---|---|
   | Go | module zip (`go install`, proxy) includes every file | `docs/go.mod` stub (`module <module>/docs`); embed only lists named dirs |
   | npm | `files` absent means everything ships | add `files` or `.npmignore` entry |
   | Python | sdist includes tracked files | `MANIFEST.in` `prune docs` or build config exclude |
   | Rust | `cargo package` | `exclude = ["docs"]` in `Cargo.toml` |

   Go check: `golang.org/x/mod/zip` `CheckDir` on the tree shows no `docs/` files. Also confirm tests and CI still list
   the same packages.
4. **Commit** only the files you added, on the branch the user names (default branch only if they say so).
5. **Push**, then **enable Pages** (use the default branch name):
   ```bash
   gh api -X POST repos/OWNER/REPO/pages -f 'source[branch]=main' -f 'source[path]=/docs' --jq .html_url
   ```
   If it already exists, use `-X PUT` instead. Wait about 45 s, then confirm
   `gh api repos/OWNER/REPO/pages/builds/latest --jq .status` is `built` and `curl -s -o /dev/null -w '%{http_code}'` on
   the URL returns 200.
6. Report the URL. Offer a README link and the repo's About "website" field; do not add them unasked.

## Rules

- Never state anything about the code you did not verify. Mark nothing as fact from memory.
- No secrets, internal hostnames, tokens or private data on the page, especially for `github-page`.
- Artifact mode changes no project files. `github-page` changes only `docs/` (plus the exclusion file for the stack).
- Never push, enable Pages, create a repo or make anything public without the user's go-ahead.
- Never overwrite an existing `docs/` or Pages configuration without asking.
