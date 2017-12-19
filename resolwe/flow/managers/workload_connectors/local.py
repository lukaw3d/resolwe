""".. Ignore pydocstyle D400.

===============
Local Connector
===============

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import subprocess

from resolwe.utils import BraceMessage as __

from .base import BaseConnector

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Connector(BaseConnector):
    """Local connector for job execution."""

    def submit(self, data, dest_dir, argv, verbosity=1):
        """Run process locally.

        For details, see
        :meth:`~resolwe.flow.managers.workload_connectors.base.BaseConnector.submit`.
        """
        logger.debug(__(
            "Connector '{}.{}' running {}.",
            self.__class__.__module__,
            self.__class__.__name__,
            repr(argv)
        ))
        subprocess.Popen(
            argv,
            cwd=dest_dir,
            stdin=subprocess.DEVNULL
        ).wait()