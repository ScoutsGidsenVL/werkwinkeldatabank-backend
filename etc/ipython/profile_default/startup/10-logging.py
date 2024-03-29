# flake8: noqa: E402 (module level import not at top of file)
# pylint: disable=unused-import
# pylint: disable=wrong-import-position
# pylint: disable=invalid-name
"""IPython startup-file, outside of PYTHONPATH.

Files in this startup-folder will be run in lexicographical order,
so you can control the execution order of files with a prefix, e.g.::

    00-foo.py
    10-baz.py
    20-bar.py

return-statements are not allowed.

"""
print(f"\nExecuting {__file__}")

import logging
import os  # noqa
import sys  # noqa

# import libranet_logging

# # import demo_flask.cfg as cfg

# # setup the logging according to etc/logging.yml
# libranet_logging.initialize()

# log = logging.getLogger("ipython-startup")  # name = "__main__"

# # import pdb;pdb.set_trace()
# log.debug("debug-message")
# log.info("info-message")
# log.warning("warning-message")
# log.error("error-message")
# log.critical("critical-message")
