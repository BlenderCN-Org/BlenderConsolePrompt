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

import bpy

from console_python import add_scrollback


'''
console.do_action can be added to:
  UserPreferences/input/Console/
using the ' + new ', i find ctrl+Enter a convenient key combo.
Possible blender bug when adding keycombos for console specifically.

https://github.com/zeffii/BlenderConsolePrompt/issues/1

FFA3AC
'''


def vtx_specials(self, m):
    ''' this first checks if the addon is enabled by testing
    view3d.ops for the presence of autvtx operator, if it's not
    present it tries to enable it. If it fails to enable the addon
    the function returns early. If the function is found, it calls
    the specific tinyCAD function.
    '''
    addon_enabled = hasattr(bpy.ops.view3d, 'autovtx')
    if not addon_enabled:
        try:
            bpy.ops.wm.addon_enable(module="mesh_tinyCAD")
        except:
            print('tinyCAD addon not found.')
            return

    if m == 'vtx':
        bpy.ops.view3d.autovtx()
    elif m == 'xl':
        bpy.ops.mesh.intersectall()


class ConsoleDoAction(bpy.types.Operator):
    bl_label = "ConsoleDoAction"
    bl_idname = "console.do_action"

    def execute(self, context):
        m = bpy.context.space_data.history[-1].body
        m = m.strip()
        if m == "cen":
            '''cursor to center'''
            context.scene.cursor_location = (0.0, 0.0, 0.0)

        elif m.endswith('!'):
            '''copy current line to clipboard'''
            m = m[:-1]
            context.window_manager.clipboard = m
            add_scrollback('added to clipboard', 'OUTPUT')

        elif m in {'vtx', 'xl'}:
            vtx_specials(self, m)

        elif m == 'ico':
            try:
                bpy.ops.wm.addon_enable(module="development_icon_get")
            except:
                self.report({'INFO'}, "ico addon not present!")

        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
