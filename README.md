terminator-plugin
=================

## About

with this plugin provides a new menu with configurable servers grouped by configurable groups to connect via ssh using custom options like username, port. verbosity and key.
It is possible to open ssh connection in new tab, horizontaly or verticaly splitted teminal session.

Thx a lot to https://github.com/dr1s/terminator-plugins where I got some code.

## Installation

1. Put files in `~/.config/terminator/plugins/`:

        git clone https://
        mkdir -p ~/.config/terminator/plugins
        cp terminator-plugin/ssh-group/ssh-group.py ~/.config/terminator/plugins/
        cp -r terminator-plugin/ssh-group/ssh-group-config ~/.config/terminator/plugins/
	      Add config to ~/.config/terminator/plugins/ssh-group-config in json-format
        
2. Edit `~/.config/terminator/plugins/ssh-group-config/config.json`, for example:

   See: cluster_connect_config/config.json

   Options:	
  
        - user: Username (not provided will use current user)
        - group: Group name for submenu.
        - agent: True or False, if true then ssh agent is enabled and -A Option is added to command
        - port: set ssh port to something else than default
        - identity: specify path to a ssh-key-file
        - verbose: 1, 2 or 3 for -v, -vv or -vvv

4. Restart [Terminator](http://www.tenshu.net/p/terminator.html)

3. Enable Plugin in `Context-Menu -> Preferences -> Plugins -> SSHGroup`

Use
===
Right click on `Terminator window -> SSH Group`
