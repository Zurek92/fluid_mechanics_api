import sys

try:
    from config.config_dev import *

    print('Found and set developer configuration.')
except ImportError:
    try:
        from config.config_prod import *

        print('Found and set production configuration.')
    except ImportError:
        print('Missing configuration file!')
        sys.exit()
