# ================================================== #
#                   CONFIG LOADER                    #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 09/20/2022                                #
# Last Edited: 09/20/2022                            #
# ================================================== #
#                                                    #
# ================================================== #

import yaml

class ConfigLoader(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConfigLoader, cls).__new__(cls)
        return cls.instance
    def __init__(self):
        with open("src\cancer_crush\config\config.yaml", "r") as config_file:
            self.data = yaml.load(config_file, Loader=yaml.FullLoader)

# ================================================== #
#                        EOF                         #
# ================================================== #
