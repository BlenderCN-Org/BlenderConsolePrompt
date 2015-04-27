# ***** BEGIN GPL LICENSE BLOCK *****
#
# This program is free software; you may redistribute it, and/or
# modify it, under the terms of the GNU General Public License
# as published by the Free Software Foundation - either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, write to:
#
#   the Free Software Foundation Inc.
#   51 Franklin Street, Fifth Floor
#   Boston, MA 02110-1301, USA
#
# or go online at: http://www.gnu.org/licenses/ to view license options.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name": "Console Prompt",
    "author": "Dealga McArdle",
    "version": (0, 1, 3),
    "blender": (2, 7, 4),
    "location": "Console - keystrokes",
    "description": "Adds feature to intercept console input and parse accordingly.",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Console"}

if 'bpy' in globals():
    print(__package__, 'detected reload event! cool.')

    if 'bc_operators' in globals():
        print('doing reloads')
        import imp
        imp.reload(bc_operators)
        imp.reload(bc_panels)
        imp.reload(bc_utils)
        imp.reload(bc_search_utils)
        imp.reload(bc_gist_utils)
        imp.reload(bc_scene_utils)
        imp.reload(bc_update_utils)
        imp.reload(bc_CAD_utils)
        imp.reload(bc_TEXT_utils)

else:
    from BCPrompt import bc_operators
    from BCPrompt import bc_panels
    from BCPrompt import bc_TEXT_utils

import bpy


def add_keymap():
    wm = bpy.context.window_manager

    console = wm.keyconfigs.user.keymaps.get('Console')
    if console:
        keymaps = console.keymap_items
        if not ('console.do_action' in keymaps):
            keymaps.new('console.do_action', 'RET', 'PRESS', ctrl=1)

    TE = wm.keyconfigs.user.keymaps.get('Text')
    if TE:
        keymaps = TE.keymap_items
        if not ('text.do_comment' in keymaps):
            keymaps.new('text.do_comment', 'SLASH', 'PRESS', ctrl=1)


def register():
    bpy.utils.register_module(__name__)
    add_keymap()


def unregister():
    bpy.utils.unregister_module(__name__)
