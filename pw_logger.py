import yaml
import sys
import logging
import logging.config

logging.config.dictConfig(yaml.load(open('logging.yaml', 'r')))

if not sys.platform.startswith('win'):
    import coloredlogs
    coloredlogs.DEFAULT_LEVEL_STYLES = {'info': {'color': 'blue'},
                                        'error': {'color': 'red'}, 'debug': {'color': 'green'},
                                        'warning': {'color': 'yellow'}}
    fmt = '%(asctime)s - %(name)s - %(filename)s[%(lineno)d] - %(levelname)s - %(message)s'
    coloredlogs.install(level='DEBUG', fmt=fmt)
    coloredlogs.install(level='DEBUG', logger=logging.getLogger("runtime"), fmt=fmt)
    coloredlogs.install(level='DEBUG', logger=logging.getLogger("tornado.access"), fmt=fmt)
    coloredlogs.install(level='DEBUG', logger=logging.getLogger("tornado.application"), fmt=fmt) 

m_logger = logging.getLogger("runtime")
err_logger = logging.getLogger("tornado.application")
