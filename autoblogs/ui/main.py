# -*- encoding: utf-8 -*-

"""
Launcher for Streamlit Dashboard for AutoBlogs Module

The launcher dashboard uses :mod:`streamlit` to create, review and
finally publish the contents easily. The :func:`launch` exposes script
``autoblogs-ui`` that calls the function internally. Any command line
arguments like ``server.port`` etc. are accepted.
"""

import sys
import pathlib

from streamlit.web import cli as stcli

def launch() -> None:
    """
    Launch a Functional Streamlit UI Dashboard for Content Management

    Using the :class:`streamlit.web.cli` the function exposes the
    UI using an executable script ``autoblogs-ui`` which is shipped
    with the module. The function runs the application, and accepts
    any command line arguments as below:

    .. code-block:: shell

        autoblogs-ui # run using default configuration
        autoblogs-ui --server.port 8080 # run from port 8080
        autoblogs-ui --server.headless true # run in serverless mode

    Any native :mod:`streamlit` flags can be used directly, check
    https://docs.streamlit.io/develop/api-reference/cli/run details.
    """

    app = pathlib.Path(__file__).parent / "app.py"
    sys.argv = ["streamlit", "run", str(app)] + sys.argv[1:]
    sys.exit(stcli.main())

if __name__ == "__main__":
    launch()
