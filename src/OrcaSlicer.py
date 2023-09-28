from SlicerInterface import SlicerInterface

import os
import logging

class OrcaSlicer(SlicerInterface):

  def __init__(self, profile):
    super().__init__(profile)
    self.slicer = "OrcaSlicer"
    self.base_path = "resources/profiles/" + self.profile["brand"]["name"]
    self.config = None

  def generate(self):
    logging.info("### generating OrcaSlicer config\n")
    logging.info(self.config)
    path = f"output/{self.slicer}"
    os.mkdir(path)
    path = f"{path}/{self.profile['brand']['name']}"
    os.mkdir(path)
    for folder in ["filament", "machine", "process"]:
      os.mkdir(f"{path}/{folder}")

    # with open(f"{path}/{self.profile['brand']['name']}.ini", "w") as configfile:
    #   pass
