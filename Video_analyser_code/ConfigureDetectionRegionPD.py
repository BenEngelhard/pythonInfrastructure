# This is a shell calling the infrastructure class ConfigureDetectionRegions
# The only application specific code is the list of application specific regions

from infrastructure.Video_analyser_code.ConfigureDetectionRegions import ConfigureDetectionRegions

instance = ConfigureDetectionRegions(['m1_c', 'm1_cen', 'm1_d', 'm2_c', 'm2_cen', 'm2_d'])
instance.configure()

