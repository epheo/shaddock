#!/usr/bin/env python
import os

#[('/etc/octopenstack', ['conf/configuration.yml', 'conf/services.yml']),

conf_directories=[]

for dirname, dirnames, filenames in os.walk('dockerfiles'):
    for subdirname in dirnames:
        config_dest_path = ('/etc/octopenstack/%s' % dirname)
        for dirname, dirnames, filenames in os.walk('dockerfiles/%s' % subdirname):
            config_dir=[]
            for filename in filenames:
                config_src_path = ('%s/%s' % (dirname, filename))
                config_dir.append(config_src_path)

        config_file_dir_liste = config_dest_path, config_dir
    conf_directories.append(config_file_dir_liste)

return conf_directories