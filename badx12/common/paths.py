# -*- coding: utf-8 -*-
import sys
from pathlib import Path

import winpath

OUTPUT_DIR = Path.home() / "Documents" / "badX12"

if sys.platform == "win32":
    OUTPUT_DIR = Path(winpath.get_my_documents()) / "badX12"
