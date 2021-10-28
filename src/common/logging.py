"""Logging helper functions"""
from logging import getLogger
from flask import current_app as app, request


def setup_request_logger(ctx=None):
    """Wrapper for getLogger"""
    request.log = getLogger(
        ctx.config['NAME'] if ctx is not None else app.config['NAME'])
