"""
Contains the default values for all parameters for both the 2D and the 3D implementation
"""
# GENERAL
DEFAULT_SPEED = 1
DEFAULT_RADIUS = 2
DEFAULT_NOISE = 0.3
DEFAULT_NUM_PARTICLES = 100

# cell-based implementation
DEFAULT_NUM_CELLS = 100

# neighbours behaviour
DEFAULT_K_NEIGHBOURS = -1 # all neighbours. set to 0 to completely ignore neighbours

DEFAULT_K_MODE1 = 2
DEFAULT_K_MODE2 = 5

# display options
DEFAULT_SHOW_PARAMETERS = False
DEFAULT_SHOW_EXAMPLE_PARTICLE = True

# 2D
DEFAULT_DOMAIN_SIZE_2D = (100, 100)

# 3D
DEFAULT_DOMAIN_SIZE_3D = (100, 100, 100)
