from SlicerInterface import SlicerInterface

import os
import shutil
import logging
import configparser

class SuperSlicer(SlicerInterface):

  def __init__(self, profile):
    super().__init__(profile)
    self.slicer = "SuperSlicer"
    self.base_path = "resources/profiles/" + self.profile["brand"]["name"]
    self.config = None

  def generate(self):
    logging.info("### generating SuperSlicer config\n")

    self.config = configparser.ConfigParser()
    brand = self.profile["brand"]["name"]

    path = f"output/{self.slicer}"
    shutil.rmtree(path)
    os.mkdir(path)

    version = self.profile["version"]
    idx = f"""\
1.0.1-slic3r slic3r-profile adaptation from prusa
min_slic3r_version = 2.4.0-beta0
{version} {brand} configuration
    """
    idx_path = f"{path}/{brand}.idx" 
    with open(idx_path, "w") as idxfile:
      idxfile.write(idx)

    self._vendor()
    self._printer_models()
    self._filaments()
    self._printer()
    self._print()

    # import sys
    # self.config.write(sys.stdout)

    ini_path = f"{path}/{brand}.ini"
    with open(ini_path, "w") as configfile:
      self.config.write(configfile)
    

  def _print(self):
    processes = self.unify_section("processes")
    # tools = self.unify_section("tools")

    for process in processes.keys():
      props = processes[process]["props"]

      for layer_height in props["layer_heights"]:
        key = f"print:{layer_height}mm {processes[process]['name']}"
        self.config.add_section(key)

        self.config.set(key, "layer_height", layer_height)
        self.config.set(key, "first_layer_height", layer_height)

        slicer_props = [
          "print.perimeters",
          "print.enforce_full_fill_volume",
          "print.top_solid_layers",
          "print.top_solid_min_thickness",
          "print.bottom_solid_layers",
          "print.bottom_solid_min_thickness",
          "print.min_width_top_surface",
          "print.ensure_vertical_shell_thickness",
          "print.thin_perimeters",
          "print.thin_perimeters_all",
          "print.thin_walls_min_width",
          "print.s_overhangs",
          "print.overhangs_width_speed",
          "print.seam_position",
          "print.seam_angle_cost",
          "print.seam_travel_cost",

          "print.resolution",
          "print.model_precision",
          "print.xy_size_compensation",
          "print.first_layer_size_compensation",
          "print.hole_size_compensation",

          "print.fill_density",
          "print.fill_pattern",
          "print.infill_anchor_max",
          "print.infill_anchor",
          "print.solid_infill_below_area",

          "print.skirt_distance",
          "print.min_skirt_length",

          "print.support_material_threshold",
          "print.support_material_contact_distance_type",
          "print.support_material_contact_distance",
          "print.support_material_bottom_contact_distance",
          "print.support_material_with_sheath",
          "print.support_material_spacing",
          "print.support_material_interface_spacing",

          "print.perimeter_speed",
          "print.external_perimeter_speed",
          "print.solid_infill_speed",
          "print.infill_speed",
          "print.top_solid_infill_speed",
          "print.support_material_speed",
          "print.support_material_interface_speed",
          "print.bridge_speed",
          "print.gap_fill_speed",
          "print.thin_walls_speed",
          "print.ironing_speed",
          "print.travel_speed",
          "print.first_layer_min_speed",
          "print.first_layer_infill_speed",
          "print.small_perimeter_speed",
          "print.small_perimeter_max_length",
          "print.default_acceleration",
          "print.perimeter_acceleration",
          "print.external_perimeter_acceleration",
          "print.solid_infill_acceleration",
          "print.infill_acceleration",
          "print.top_solid_infill_acceleration",
          "print.bridge_acceleration",
          "print.travel_acceleration",
          "print.first_layer_acceleration",

          "print.extrusion_spacing",
          "print.first_layer_extrusion_width",
          "print.perimeter_extrusion_spacing",
          "print.external_perimeter_extrusion_width",
          "print.infill_extrusion_spacing",
          "print.solid_infill_extrusion_spacing",
          "print.top_infill_extrusion_width",
          "print.support_material_extrusion_width",
          "print.skirt_extrusion_width",
          "print.solid_infill_overlap",
          "print.bridge_flow_ratio",

          "print.wipe_tower",
          "print.wipe_tower_x",
          "print.wipe_tower_y",
          "print.wipe_tower_brim_width",
          "print.single_extruder_multi_material_priming",

          "print.extruder_clearance_radius",
          "print.output_filename_format",
        ]
        for slicer_path in slicer_props:
          self.config.set(key, slicer_path.split(".")[1], self.get_config(props, slicer_path))

  def _printer(self):
    models = self.unify_section("machines")
    tools = self.unify_section("tools")
    brand = self.profile["brand"]["name"]

    for model in models.keys():
      for tool in tools.keys():
        key = f"printer:{brand} {models[model]['name']} {tools[tool]['name']}"
        self.config.add_section(key)
        model_props = models[model]["props"]
        tool_props = tools[tool]["props"]

        small_x = self.get_config(model_props, "printer.thumbnails_small_x")
        small_y = self.get_config(model_props, "printer.thumbnails_small_y")
        big_x = self.get_config(model_props, "printer.thumbnails_big_x")
        big_y = self.get_config(model_props, "printer.thumbnails_big_y")
        thumbnails = f"{small_x}x{small_y},{big_x}x{big_y}"
        self.config.set(key, "thumbnails", thumbnails)

        slicer_props = [
          "printer.gcode_flavor",
          "printer.z_step",
          "printer.thumbnails_small_x",
          "printer.thumbnails_small_y",
          "printer.thumbnails_big_x",
          "printer.thumbnails_big_y",
          "printer.use_relative_e_distances",
          "printer.gcode_filename_illegal_char",
          "printer.time_estimation_compensation",
          "printer.machine_max_feedrate_z",
          "printer.machine_max_feedrate_e",
          "printer.machine_max_acceleration_x",
          "printer.machine_max_acceleration_y",
          "printer.machine_max_acceleration_e",
          "printer.machine_max_acceleration_extruding",
          "printer.machine_max_acceleration_retracting",
          "printer.machine_max_acceleration_travel",
          "printer.machine_max_jerk_x",
          "printer.machine_max_jerk_y",
          "printer.machine_max_jerk_z",
        ]
        for slicer_path in slicer_props:
          self.config.set(key, slicer_path.split(".")[1], self.get_config(model_props, slicer_path))

        slicer_props = [
          "printer.start_gcode",
          "printer.end_gcode",
          "printer.before_layer_gcode",
          "printer.after_layer_gcode",
          "printer.color_change_gcode",
          "printer.pause_print_gcode",
        ]
        for slicer_path in slicer_props:
          gcode = ascii(self.get_config(model_props, slicer_path))
          self.config.set(key, slicer_path.split(".")[1], gcode)

        slicer_props = [
          "tool.retract_lift",
          "tool.retract_lift_below",
          "tool.retract_speed",
          "tool.deretract_speed",
          "tool.retract_before_travel",
          "tool.wipe",
          "tool.filament_retract_layer_change",
        ]
        for slicer_path in slicer_props:
          self.config.set(key, slicer_path.split(".")[1], self.get_config(tool_props, slicer_path))

  def set_list(self, key, slicer_path, props):
    value = self.get_config(props, slicer_path)
    if value is None:
      logging.debug(f"### {slicer_path} not found")
      return
    self.config.set(key, slicer_path.split(".")[1], value)

  def _filaments(self):
    filaments = self.unify_section("materials")
    for filament in filaments.keys():
      key = "filament:" + filaments[filament]["name"]
      self.config.add_section(key)
      props = filaments[filament]["props"]

      slicer_props = [
        "filament.filament_type",
        "filament.filament_vendor",
        "filament.filament_cost",
        "filament.filament_density",
        "filament.first_layer_temperature",
        "filament.first_layer_bed_temperature",
        "filament.temperature",
        "filament.bed_temperature",
        "filament.max_volumetric_speed",
        "filament.min_fan_speed",
        "filament.max_fan_speed",
        "filament.fan_below_layer_time",
        "filament.slowdown_below_layer_time",
        "filament.min_print_speed",
      ]
      for slicer_path in slicer_props:
        # self.config.set(key, slicer_path.split(".")[1], self.get_config(props, slicer_path))
        self.set_list(key, slicer_path, props)

  def _vendor(self):
    self.config.add_section("vendor")
    self.config.set("vendor", "config_version", self.profile["version"])
    self.config.set("vendor", "name", self.profile["brand"]["name"])

  def _printer_models(self):
    models = self.unify_section("machines")
    for model in models.keys():
      props = models[model]["props"]
      brand = self.profile["brand"]["name"]

      # section
      key = f"printer_model:{brand} {models[model]['name']}"
      self.config.add_section(key)

      # name
      model = models[model]["name"]
      self.config.set(key, "name", f'{brand} {model}')
      self.config.set(key, "family", brand)
      self.config.set(key, "printer_model", model)

      # volume
      size_x   = self.get_config(props, "printer_model.size_x")
      size_y   = self.get_config(props, "printer_model.size_y")
      origin_x = self.get_config(props, "printer_model.origin_x")
      origin_y = self.get_config(props, "printer_model.origin_y")
      bed_shape = f"{origin_x}x{origin_y},{size_x}x{origin_y},{size_x}x{size_y},{origin_x}x{size_y}"
      self.config.set(key, "bed_shape", bed_shape)
      self.config.set(key, "max_print_height", self.get_config(props, "printer_model.size_z"))

      # other props
      slicer_props = [
        "printer_model.technology",
        "printer_model.thumbnail",
        "printer_model.bed_model",
        "printer_model.bed_texture"
      ]
      for slicer_path in slicer_props:
        self.config.set(key, slicer_path.split(".")[1], self.get_config(props, slicer_path))

      # fix paths
      paths = [
        "thumbnail",
        "bed_model",
        "bed_texture"
      ]
      for path in paths:
        self.config.set(key, path, f"{self.base_path}/{self.config.get(key, path)}")

      output_path = f"output/{self.slicer}/{brand}/machine/{model}"
      os.makedirs(output_path, exist_ok=True)

      profile_path = f"profiles/{brand}/"

      cover = profile_path + self.get_config(props, "printer_model.thumbnail")
      shutil.copy(cover, output_path)

      bed = profile_path + self.get_config(props, "printer_model.bed_model")
      shutil.copy(bed, output_path)

      bed_texture = profile_path + self.get_config(props, "printer_model.bed_texture")
      shutil.copy(bed_texture, output_path)
  
