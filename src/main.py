import logging

import yaml

from SuperSlicer import SuperSlicer

logging.basicConfig(level=logging.DEBUG)

with open("../profiles/Cosmyx/profile.yml", "r") as file:
  profile = yaml.load(file, Loader=yaml.FullLoader)

slicers = [
  SuperSlicer(profile),
]

for slicer in slicers:
  slicer.generate()

