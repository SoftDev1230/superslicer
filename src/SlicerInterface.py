import logging
import json

import yaml


class SlicerInterface:

  def __init__(self, profile):
    self.profile = profile
    self.keys = yaml.load(open("./slicers.yml", "r"), Loader=yaml.FullLoader)
    self.slicer = None

  def generate(self):
    raise NotImplementedError("generate() method is not implemented yet")

  def unify_section(self, section):
    output = {}

    def merge_dicts(dict1, dict2):
      result = {**dict1}
      for key, value in dict2.items():
        if isinstance(value, dict) and key in dict1 and isinstance(dict1[key], dict):
          result[key] = merge_dicts(dict1[key], value)
        else:
          result[key] = value
      return result

    def add_props_recursive(node, inherited_props):
      current_props = merge_dicts(inherited_props, node.get('props', {}))
      if not node.get('virtual', False):
        node_data = {
            'name': node.get('name', ''),
            'props': current_props
        }
        output[node['name']] = node_data
      for child in node.get('children', {}).values():
        add_props_recursive(child, current_props)

    for node in self.profile[section].values():
      add_props_recursive(node, {})

    # logging.debug(f"unified {section} section: {json.dumps(output, indent=2)}")
    return output

  def get_config(self, profile_section, key):
    # logging.debug(f"getting config for {key}")
    if self.slicer is None:
      raise Exception("slicer is not defined")

    slicer_path = key.split(".")
    keys = self.keys[self.slicer]
    while len(slicer_path) > 1:
      keys = keys[slicer_path.pop(0)]

    profile_path = keys[slicer_path.pop(0)].split(".")
    # logging.debug(profile_path)
    while len(profile_path) > 0:
      if profile_path[0] not in profile_section:
        logging.debug(f"{key}: key '{profile_path[0]}' not found in profile section {json.dumps(profile_section, indent=2)}")
        return None
      profile_section = profile_section[profile_path.pop(0)]

    # logging.debug(f"config for {key} is {profile_section}")
    return str(profile_section)
