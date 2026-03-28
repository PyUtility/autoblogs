<h1 align = "center">CHANGELOG</h1>

<div align = "justify">

All notable changes to this project will be documented in this file. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [PEP0440](https://peps.python.org/pep-0440/)
styling guide. For full details, see the [commit logs](https://github.com/PyUtility/autoholidays/commits).

## `PEP0440` Styling Guide

<details>
<summary>Click to open <code>PEP0440</code> Styilng Guide</summary>

Packaging for `PyPI` follows the standard PEP0440 styling guide and is implemented by the **`packaging.version.Version`** class.
The other popular versioning scheme is [`semver`](https://semver.org/), but each build has different parts/mapping. The
following table gives a mapping between these two versioning schemes:

<div align = "center">

| `PyPI` Version | `semver` Version |
| :---: | :---: |
| `epoch` | n/a |
| `major` | `major` |
| `minor` | `minor` |
| `micro` | `patch` |
| `pre` | `prerelease` |
| `dev` | `build` |
| `post` | n/a |

</div>

One can use the **`packaging`** version to convert between PyPI to semver and vice-versa. For more information, check this
[link](https://python-semver.readthedocs.io/en/latest/advanced/convert-pypi-to-semver.html) for more information.

</details>

## Release Note(s)

The release notes are documented, the list of changes to each different release are documented. The `major.minor` patch are indicated
under `h3` tags, while the `micro` and "version identifiers" are listed under `h4` and subsequent headlines.

<details>
<summary>Click to open <code>Legend Guidelines</code> for the Project CHANGELOG.md File</summary>

  * 🎉 - **Major Feature** : something big that was not available before.
  * ✨ - **Feature Enhancement** : a miscellaneous minor improvement of an existing feature.
  * 🛠️ - **Patch/Fix** : something that previously didn’t work as documented – or according to reasonable expectations – should now work.
  * ⚙️ - **Code Efficiency** : an existing feature now may not require as much computation or memory.
  * 💣 - **Code Refactoring** : a breakable change often associated with `major` version bump.

</details>

### AutoBlogs v1.0.0 (`Train Yard`) | 2026-03-29

Initial developmental build of **AutoBlogs** — an AI-assisted, human-in-the-loop content generation toolkit that supports
both a command-line interface and a Streamlit web UI.

#### Core Library

- `autoblogs.model.dataflows` — frozen dataclasses `AIModel`, `AIRequest`, and `AIResponse` for typed, immutable data flow
  across the generation pipeline. `AIResponse` exposes computed properties `total_tokens` and `word_count`.
- `autoblogs.config.constants` — `AIProvider` enum (`CLAUDE`, `OPENAI`, `NVIDIA-NIM`, `LOCAL`) and `DraftState` lifecycle enum
  (`PENDING`, `GENERATING`, `DRAFT`, `REVIEWING`, `APPROVED`, `PUBLISHED`, `FAILED`, `RETRACTED`, `DELETED`).
- `autoblogs.config.default` — module-level defaults available globally.
- `autoblogs.error.error` — `AIClientError` for surfacing provider/SDK failures.

#### Client Layer

- `autoblogs.client.anthropic` — `claudeGenerate` function for Claude (Anthropic SDK) using system-prompt + user-message pattern.
- `autoblogs.client.openai` — `generateOpenAI` function compatible with OpenAI, NVIDIA-NIM, and local inference servers.
- `autoblogs.manager.client.ClientManager` — provider-agnostic client factory with lazy, selective SDK imports; raises
  `AIClientError` when the required SDK (`anthropic` / `openai`) is not installed.

#### Content & Prompt Layer

- `autoblogs.manager.content.ContentManager` — Jinja2-based prompt renderer with `FileSystemLoader`; supports topic, SEO
  keywords, word-count bounds, sub-section count, and a Claude-specific rendering path.
- Prompt templates shipped with the package under `autoblogs/prompts/`:
  - `base.txt.jinja` — base template inherited by all content templates.
  - `python.txt.jinja` — specialized template for Python-topic blog posts.
- File-write support: `ContentManager.writefile()` persists generated Markdown content to a configurable output directory.

#### CLI Tool (`autoblogs-cli`)

- Interactive terminal workflow: displays ASCII-art banner, collects topic, generation prompt, SEO keywords, and output
  filename from the user.
- Full `.env` / environment-variable configuration (`LLM_PROVIDER`, `LLM_MODEL_NAME`, `LLM_MODEL_APIKEY`, `LLM_API_BASE_URL`,
  `MAX_TOKENS`, `TEMPERATURE`, `CONTENT_OUTPUT_DIR`, `AGENT_PROMPT_CONTEXT`).
- Registered as `autoblogs-cli` entry-point in `pyproject.toml`.

#### Streamlit Web UI (`autoblogs-ui`)

- Multi-page navigation wired via `st.navigation` with five pages:
  - **About** — project overview.
  - **Dashboard** — content dashboard.
  - **Create Content** — form-driven generation (topic, prompt, SEO keywords); displays word count, token usage, and latency
    metrics on success.
  - **Draft Editor** — tabbed Edit / Preview interface with a 600-line editable text area and live Markdown preview; separate
    Save to File and Download tabs for persisting or exporting drafts as `.md` files.
  - **Model Settings** — configure provider, model, and API credentials.
- Sidebar heading and info button (links to PyUtility GitHub).
- Custom CSS stylesheet loaded at startup via `st.markdown`.
- Footer rendered without inline JS (workaround for `st.markdown` innerHTML restriction).
- Registered as `autoblogs-ui` entry-point in `pyproject.toml`.

#### CI / Automation

- Streamlit Community Cloud CI validation workflow (`.github/workflows/streamlit.yml`).
- PyPI publish workflow (`.github/workflows/publish.yml`).
- Dependabot configured to keep GitHub Actions versions up to date.
