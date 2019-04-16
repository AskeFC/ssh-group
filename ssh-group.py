#!/usr/bin/env python3
# Terminator plugin by donfuz14
# GPL v2 only

from gi.repository import Gtk, Vte
import random
import terminatorlib.plugin as plugin
from terminatorlib.config import Config
import getpass
import json
import os
import re
import itertools
import gi
gi.require_version('Gtk', '3.0')


pluginpath = os.path.dirname(os.path.realpath(__file__))
configpath = (pluginpath + "/ssh-group-config")

# get information from config.json
for root, dirs, files in os.walk(configpath):
    for file in files:
        if file.endswith(".json"):
            filename = (os.path.join(root, file))
            try:
                with open(filename) as data_file:
                    try:
                        SSHGROUP
                    except NameError:
                        SSHGROUP = json.load(data_file)
                    else:
                        SSHGROUP.update(json.load(data_file))
            except Exception as e:
                print("Error loading "+filename+": "+str(e))


AVAILABLE = ['SSHGroup']
current_user = getpass.getuser()
groupdict = {}


class SSHGroup(plugin.Plugin):
    capabilities = ['terminal_menu']
    config = None

    def __init__(self):
        self.config = Config()
        for server, option in SSHGROUP.items():
            group = self.get_property(server, 'group')
            # server = str.join("", server)
            # print(group, server)
            if group not in groupdict:
                groupdict[group] = [server]
            else:
                groupdict[group].append(str.join("", server))

    def callback(self, menuitems, menu, terminal):
        submenu = {}
        item = Gtk.MenuItem('SSH Group')
        menuitems.append(item)
        submenu = Gtk.Menu()
        item.set_submenu(submenu)

        # create groupdict for submenu
        for group, servers in groupdict.items():
            sub_groups = self.add_submenu(submenu, group)
            servers.sort()
            for server in servers:
                self.add_split_submenu(terminal, sub_groups, server)
            menuitem = Gtk.SeparatorMenuItem()
            submenu.append(menuitem)

    def add_submenu(self, submenu, name):
        menu = Gtk.MenuItem(name)
        submenu.append(menu)
        menu_sub = Gtk.Menu()
        menu.set_submenu(menu_sub)
        return menu_sub

    def add_split_submenu(self, terminal, sub_groups, server):
        # get username for ssh session
        if self.get_property(server, 'user'):
            user = self.get_property(server, 'user')
        else:
            user = current_user

        sub_split = self.add_submenu(sub_groups, server)

        menuitem = Gtk.MenuItem('Horizontal Split')
        menuitem.connect('activate', self.connect_server, terminal, server,
                         user, 'H')
        sub_split.append(menuitem)

        menuitem = Gtk.MenuItem('Vertical Split')
        menuitem.connect('activate', self.connect_server, terminal, server,
                         user, 'V')
        sub_split.append(menuitem)

        menuitem = Gtk.MenuItem('New Tab')
        menuitem.connect('activate', self.connect_server, terminal, server,
                         user, 'T')
        sub_split.append(menuitem)

    def connect_server(self, widget,  terminal, server, user, option):
        focussed_terminal = None
        term_window = terminal.terminator.windows[0]

        visible_terminals_temp = term_window.get_visible_terminals()

        if option == 'H':
            terminal.key_split_horiz()
        elif option == 'V':
            terminal.key_split_vert()
        elif option == 'T':
            term_window.tab_new(term_window.get_focussed_terminal())

        visible_terminals = term_window.get_visible_terminals()
        for visible_terminal in visible_terminals:
            if visible_terminal not in visible_terminals_temp:
                terminal2 = visible_terminal
        self.start_ssh(terminal2, user, server)

    def start_ssh(self, terminal, user, server):
        # Function to generate the ssh command, with specified options
        if server:
            command = "ssh"

        if user != current_user:
            command = command + " -l " + user

        # check if ssh agent should be used, if not disable it
        if self.get_property(server, 'agent'):
            command += " -A"
        else:
            command += " -a"

        # If port is configured, get that port
        port = self.get_property(server, 'port')
        if port:
            command = command + " -p " + port

        # If ssh-key is specified, use that key
        key = self.get_property(server, 'identity')
        if key:
            command = command + " -i " + key

        # get verbosity level
        verbose = self.get_property(server, 'verbose')
        if verbose:
            count = 0
            command = command + " -"
            while count < int(verbose) < 4:
                command += "v"
                count += 1

        command = command + " " + server

        # Check if a command was generated an pass it to the terminal
        if command[len(command) - 1] != '\n':
            command += '\n'
            self.feed_child(terminal, command)

    def feed_child(self, terminal, command):
        try:
            terminal.vte.feed_child(str(command))
        except TypeError:
            terminal.vte.feed_child(command, len(command))

    def get_property(self, server, prop, default=False):
        # Check if property and server exsist return true else return false
        if SSHGROUP.has_key(server) and SSHGROUP[server].has_key(prop):
            return str.join("", SSHGROUP[server][prop])
        else:
            return default
