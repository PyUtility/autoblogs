<div align = "center">

# Auto Blogs - AI-Powered Content Generation Toolkit

[![GitHub Issues](https://img.shields.io/github/issues/PyUtility/autoblogs?style=plastic)](https://github.com/PyUtility/autoblogs/issues)
[![GitHub Forks](https://img.shields.io/github/forks/PyUtility/autoblogs?style=plastic)](https://github.com/PyUtility/autoblogs/network)
[![GitHub Stars](https://img.shields.io/github/stars/PyUtility/autoblogs?style=plastic)](https://github.com/PyUtility/autoblogs/stargazers)
[![LICENSE File](https://img.shields.io/github/license/PyUtility/autoblogs?style=plastic)](https://github.com/PyUtility/autoblogs/blob/master/LICENSE)

</div>

<div align = "justify">

AN AI-assisted content generation tool that can leverage both open-source and/or propritary Large Language Model (LLM) agent to
create high-quality, SEO-optimized contents for various needs. The system integrates a *human-in-the-loop workflow*, ensuring
that AI-generated drafts can be reviewed, edited, and refined before publishing.

## Project Overview

This project aims to simplify and accelerate the process of writing contents (blog, articles, book, research papers, etc.) by
combining AI automation with human editorial control. It provides a flexible framework where multiple LLM providers can be
integrated to create and customize contents using a [streamlit](https://streamlit.io/) dashboard.

The contents can then be published online, like in [GitHub Pages](https://docs.github.com/en/pages), [substack](https://substack.com/),
etc. and thus starting a technical writing business or freelance job becomes very easy.

## Getting Started

The repository uses third party Python SDKs, that provides API interface to interact with *open-source* or any *proprietary* LLM,
like [OpenAI](https://pypi.org/project/openai/) or [Anthropic Claude](https://pypi.org/project/anthropic/) to generate contents.

The package is available in PyPI and can be installed as below:

```shell
pip install autoblogs
```

The package does not have a hard dependency on a third-party LLM SDK, but requires so based on the type of model you want to
use. For example,

```python
import autoblogs

...

client = autoblogs.client.OpenAIClien(...) # pip install openai
client = autoblogs.client.ClaudeClient(...) # pip install anthropic
```

### Environment Variables

For getting started, you will require the name of the model (`LLM_MODEL_NAME`) and an API key (if any, `LLM_MODEL_APIKEY`) to
use the module. You can also integrate to external API endpoints or self-hosted/your own companies API endpoints to configure
the services as below.

```shell
LLM_MODEL_NAME = "awesome-model"
LLM_MODEL_APIKEY = "abc-example.com"
LLM_API_BASE_URL = "https://example.com/api/v1"
```

### Python Script

```python
import autoblogs

model = autoblogs.model.AIModel(
  model = os.environ.get("LLM_MODEL_NAME"), provider = "LLM-PROVIDER"
)
request = autoblogs.model.AIRequest(
  topic = "Linear Regression",
  prompt = "What is Linear Regression? Explain in 50 Words."
)

# use openai client to use openai/any suuported endpoints
client = autoblogs.client.OpenAIClient(
  model = model, apikey = os.environ.get("LLM_MODEL_APIKEY"),
  base_url = os.environ.get("LLM_API_BASE_URL")
)

# or, use claude client; this does not support an base url
client = autoblogs.client.ClaudeClient(
  model = model, apikey = os.environ.get("LLM_MODEL_APIKEY")
)

# get the response using `.generate()` function; unified in clients
response - client.generate(request = request)
print(response.raw_reponse)
>>> Linear Regression is a statistical method that ...
```

## Contribution Guidelines

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome. A detailed
overview on how to contribute can be found in the **contributing guidelines**. If you run into an issue, please file a new
[issue](https://github.com/PyUtility/autoblogs/issues) for discussion. Create a pull request for a new feature or a fix to
an existing issue [here](https://github.com/PyUtility/autoblogs/pulls).

As contributors and maintainers to this project, you are expected to abide by [PyUtility](https://github.com/PyUtility)'s
code of conduct. More information can be found at: **Contributor Code of Conduct**.

</div>
