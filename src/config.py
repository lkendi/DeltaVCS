#!/usr/bin/env python3
"""Configuration module - contains global variables"""
import os

DELTA_DIR = ".delta"
OBJECTS_DIR = os.path.join(DELTA_DIR, "objects")
REFS_DIR = os.path.join(DELTA_DIR, "refs")
HEADS_DIR = os.path.join(REFS_DIR, "heads")
HEAD_FILE = os.path.join(DELTA_DIR, "HEAD")
INDEX_FILE = os.path.join(DELTA_DIR, "index")
BRANCH_DIR = os.path.join(REFS_DIR, "heads")
