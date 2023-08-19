#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023 The ibanez_ts9 developers. All rights reserved.
# Project site: https://github.com/matthewrankin/ibanez_ts9
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
from invoke import run, task
from unipath import Path

TESTPYPI = "https://testpypi.python.org/pypi"
ROOT_DIR = Path(__file__).ancestor(1)


@task
def lint(ctx):
    """Run flake8 to lint code"""
    run("python3 -m flake8")
    run("python3 -m mypy create_plot.py")


@task
def freeze(ctx):
    # pylint: disable=W0613
    """Freeze the pip requirements using pip-chill"""
    run(f"pip-chill > {Path(ROOT_DIR, 'requirements.txt')}")


@task(lint)
def test(ctx):
    """Lint, unit test, and check setup.py"""
    run("nose2")


@task
def min(ctx):
    """Create the plot using example data from a FRTONMIN"""
    run("python create_plot.py inputs/FRTONMIN.DAT outputs/frtonmin.pdf")


@task
def mid(ctx):
    """Create the plot using example data from a FRTONMID"""
    run("python create_plot.py inputs/FRTONMID.DAT outputs/frtonmid.pdf")


@task
def max(ctx):
    """Create the plot using example data from a FRTONMAX"""
    run("python create_plot.py inputs/FRTONMAX.DAT outputs/frtonmax.pdf")
