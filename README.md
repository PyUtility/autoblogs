<div align = "center">

# Auto Blogs - AI-Powered Content Generation Toolkit

[![GitHub Issues](https://img.shields.io/github/issues/PyUtility/autoblogs?style=plastic)](https://github.com/PyUtility/autoblogs/issues)
[![GitHub Forks](https://img.shields.io/github/forks/PyUtility/autoblogs?style=plastic)](https://github.com/PyUtility/autoblogs/network)
[![GitHub Stars](https://img.shields.io/github/stars/PyUtility/autoblogs?style=plastic)](https://github.com/PyUtility/autoblogs/stargazers)
[![LICENSE File](https://img.shields.io/github/license/PyUtility/autoblogs?style=plastic)](https://github.com/PyUtility/autoblogs/blob/master/LICENSE)

</div>

<div align = "justify">

**`AutoBlogs`** is an AI-assisted content generation tool that can leverage both open-source and/or proprietary Large Language
Model (LLM) agents to create high-quality, SEO-optimized content for various needs. The system integrates a *human-in-the-loop workflow*,
ensuring that AI-generated drafts can be reviewed, edited, and refined before publishing.

## Project Overview

This project aims to simplify and accelerate the process of writing contents (blog, articles, book, research papers, etc.) by
combining AI automation with human editorial control. It provides a flexible framework where multiple LLM providers can be
integrated to create and customize contents using a [streamlit](https://streamlit.io/) dashboard.

The contents can then be published online, like in [GitHub Pages](https://docs.github.com/en/pages), [substack](https://substack.com/),
etc. and thus starting a technical writing business or freelance job becomes very easy.

## Getting Started

The repository uses third-party Python SDKs that provide an API interface to interact with *open-source* or any *proprietary* LLM,
like [OpenAI](https://pypi.org/project/openai/) or [Anthropic Claude](https://pypi.org/project/anthropic/) to generate content.

The package is available on PyPI and can be installed as follows:

```shell
pip install autoblogs
```

The package does not have a hard dependency on a third-party LLM SDK, but requires one based on the type of model you want to
use. For example, it either requires the [Anthropic SDK](https://pypi.org/project/anthropic/) for the `CLAUDE` provider or the
[OpenAI SDK](https://pypi.org/project/openai/) for all other types of providers.

### Environment Variables

Copy `.env.example` to `.env` and fill in your values, or supply them as system environment variables. The available
variables are described below.

```shell
# LLM provider name - e.g. "OPENAI", "ANTHROPIC", "LOCAL", "NVIDIA-NIM"
LLM_PROVIDER = "LOCAL"

# Model identifier and API key for the selected provider
LLM_MODEL_NAME = "awesome-model"
LLM_MODEL_APIKEY = "your-api-key-here"

# Optional: override the default API base URL (useful for self-hosted or custom endpoints)
LLM_API_BASE_URL = "https://example.com/api/v1"

# Model generation parameters
MAX_TOKENS = 4096
TEMPERATURE = 0.7

# I/O configuration
CONTENT_OUTPUT_DIR = "output"
AGENT_PROMPT_CONTEXT = "base.txt.jinja"
```

### Command Line Tools

The package provides two distinct tools for different workflows. **`autoblogs-cli`** is a lightweight interactive terminal
tool for quick content generation, while **`autoblogs-ui`** launches a full browser-based dashboard for an end-to-end
editorial workflow — creation, editing, preview, and file management.

#### AutoBlogs-CLI

`autoblogs-cli` runs entirely in the terminal. It reads your configuration from the `.env` file (or system environment),
then walks you through a short interactive session to collect the content requirements before calling the LLM.

```shell
autoblogs-cli
```

Once launched, it prompts for the following inputs in order:

| Prompt | Description | Example |
|--------|-------------|---------|
| **Content Topic** | One-line subject of the post | `Linear Regression for Beginners` |
| **Generation Prompt** | Free-form instructions for the model | `Explain with real-world examples, keep it beginner-friendly` |
| **SEO Keywords** | Comma-separated keywords to embed | `statistics, regression, machine learning, data science` |
| **Output Filename** | Path (relative to `CONTENT_OUTPUT_DIR`) to save the result | `linear-regression.md` |

A sample session looks like:

```
Set the Content Topic (one-line): Linear Regression for Beginners
Explain the Prompt to Generate Content: Explain with real-world examples, keep it beginner-friendly
Set SEO Keywords (comma separated): statistics, regression, machine learning
Input Output Filename: linear-regression.md
```

The generated post is written to `<CONTENT_OUTPUT_DIR>/<Output Filename>` (default: `output/linear-regression.md`).

#### AutoBlogs-UI

`autoblogs-ui` launches a multi-page [Streamlit](https://streamlit.io/) dashboard in your browser. It provides the same
content generation capabilities as the CLI, plus an inline draft editor, live markdown preview, and file download.

```shell
# Launch on the default port (http://localhost:8501)
autoblogs-ui

# Run on a custom port
autoblogs-ui --server.port 8080

# Run in headless / server mode (no browser auto-open)
autoblogs-ui --server.headless true
```

Any native [Streamlit CLI flag](https://docs.streamlit.io/develop/api-reference/cli/run) is accepted and forwarded
directly. Once running, open `http://localhost:8501` (or the configured port) in your browser.

The dashboard is organised into five pages:

| Page | Description |
|------|-------------|
| **About the App** | Project overview, supported providers, and last-run generation metrics |
| **Dashboard** | Browse generated files — lists output directory contents with size and a quick preview |
| **Create Content** | Fill in Topic, Prompt, and SEO Keywords, then click *Generate Content* to call the LLM |
| **Draft Editor** | Edit the generated draft inline, preview rendered Markdown, save to file, or download |
| **Model Settings** | Change provider, model name, API key, base URL, temperature, max tokens, and prompt template without restarting |

## Contribution Guidelines

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome. A detailed
overview of how to contribute can be found in the **contributing guidelines**. If you run into an issue, please file a new
[issue](https://github.com/PyUtility/autoblogs/issues) for discussion. Create a pull request for a new feature or a fix to
an existing issue [here](https://github.com/PyUtility/autoblogs/pulls).

As contributors and maintainers to this project, you are expected to abide by [PyUtility](https://github.com/PyUtility)'s
code of conduct. More information can be found at: **Contributor Code of Conduct**.

</div>
