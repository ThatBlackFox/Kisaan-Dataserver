import pandas as pd
import os
import pathlib
files = []
for file in pathlib.Path('data/').iterdir():
    files.append(file.joinpath(file))

print(files)