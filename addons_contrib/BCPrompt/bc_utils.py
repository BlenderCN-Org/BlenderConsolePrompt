import bpy

import os
import json
import webbrowser
from urllib.request import (urlopen, urlretrieve)
import sys
import traceback


# def throw_manual():
#     bcp_webbrowser("README.html")


def throw_manual():
    # if i want to do own parsing + stylesheet
    zef = "https://raw.githubusercontent.com/zeffii/"
    ul = zef + "BlenderConsolePrompt/master/README.md"

    path_init = os.getcwd()
    temp_root = os.path.dirname(__file__)
    tmp = os.path.join(temp_root, 'tmp')
    os.chdir(tmp)

    readme_path = os.path.join(tmp, 'README.md')
    urlretrieve(ul, readme_path)

    # generate the markdown json obj first.
    with open(readme_path) as mdfile:
        md_str = repr(''.join(mdfile.readlines()))
        json_str = """var jsonObject = {{"items": {0}}}""".format(md_str)
        with open("bcp_readme.json", 'w') as destjson:
            destjson.writelines(json_str)

    webbrowser.open('README.html')
    os.chdir(path_init)


def bcp_webbrowser(local_path):
    '''sets current dir to tmp, starts the browser, reverts dir.'''
    path_init = os.getcwd()
    temp_root = os.path.dirname(__file__)
    temp_html = os.path.join(temp_root, 'tmp')
    os.chdir(temp_html)
    webbrowser.open(local_path)
    os.chdir(path_init)


def bcp_justbrowse(destination):
    webbrowser.open(destination)


def sv_test():
    try:
        ng = bpy.data.node_groups
    except:
        print('no node SV groups!')
        return

    sv_present = 'sverchok' in globals()
    if not sv_present:
        try:
            import sverchok
            print('Sverchok is now in globals')
        except:
            print('failed to import sverchok')
            return

    return True


def get_sv_times(named_group):

    if not sv_test():
        return

    import sverchok
    ng = bpy.data.node_groups
    upd = bpy.ops.node.sverchok_update_current

    # at this point sverchok should be available.
    # github.com/nortikin/sverchok/issues/500#issuecomment-67337023
    def write_time_graph_json(destination_path):
        m = sverchok.core.update_system.graphs
        atk = {}
        for idx, event in enumerate(m[0]):
            atk[idx] = event

        tk = dict(items=atk)
        tkjson = json.dumps(tk, sort_keys=True, indent=2)
        with open(destination_path, 'w') as time_graph:
            # this augments the first line of the json with a var
            # transforming it into a valid .js file which can be
            # called from the inlet.js
            final_write = "var jsonObject = " + tkjson
            time_graph.writelines(final_write)

    _root = os.path.dirname(__file__)
    fp = os.path.join(_root, 'tmp', 'sverchok_times.json')

    for g in ng:
        if g.bl_idname == 'SverchCustomTreeType':
            if g.name == named_group:
                upd(node_group=named_group)
                print('updating for:', named_group)
                write_time_graph_json(fp)
                bcp_webbrowser('index.html')
                break


def get_sv_times_all():
    if not sv_test():
        return

    import sverchok
    ng = bpy.data.node_groups
    upd = bpy.ops.node.sverchok_update_current
    for g in ng:
        if g.bl_idname == 'SverchCustomTreeType':
            upd(node_group=g.name)
            m = sverchok.core.update_system.graphs
            print(g.name)
            print(m)
            print('::::')

    ''' Augmented full node tree and subtree json'''

    _root = os.path.dirname(__file__)
    fp_full = os.path.join(_root, 'tmp', 'sverchok_times_full.json')

    # full_atk = {}
    # print('number of subgraphs:', len(m))
    # for index, (graph, graph_name) in enumerate(zip(m, mn)):
    #     print('-----', index, graph, graph_name, '<<<<')

    #     atk = {idx: event for idx, event in enumerate(graph)}
    #     gtk = dict(items=atk, name=graph_name)
    #     full_atk[index] = gtk

    # print(full_atk)

    # tkjson_full = json.dumps(full_atk, sort_keys=True, indent=2)
    # with open(dp2, 'w') as time_graph:

    #     # this augments the first line of the json with a var
    #     # transporming it into a valid .js file which can be
    #     # called from the inlet.js
    #     final_write = "var jsonObject = " + tkjson_full
    #     time_graph.writelines(final_write)
    pass


def github_commits(url, num_items):
    found_json = urlopen(url).readall().decode()

    wfile = json.JSONDecoder()
    wjson = wfile.decode(found_json)
    for idx, i in enumerate(wjson):
        commit = i['commit']

        print(commit['committer']['name'])
        for line in commit['message'].split('\n'):
            if not line:
                continue
            print('  ' + line)
        print()
        if idx > num_items:
            break


def do_text_glam():

    def set_props(s):
        # s = context.space_data
        s.show_line_numbers = True
        s.show_word_wrap = True
        s.show_syntax_highlight = True
        s.show_margin = True

    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:

            if not area.type == 'TEXT_EDITOR':
                continue

            for s in area.spaces:
                if s.type == 'TEXT_EDITOR':
                    set_props(s)


def set_keymap():

    # script to map 1, 2, 3 to vertex, edge, face selection for 3dview
    wm = bpy.context.window_manager

    if True:
        deactivate_list = ['ONE', 'TWO', 'THREE']
        view3d_km_items = wm.keyconfigs.default.keymaps['3D View'].keymap_items
        for j in view3d_km_items:
            if j.type in deactivate_list and j.name == 'Layers':
                j.active = False

    if True:
        my_keymap = {
            'ONE': "True, False, False",
            'TWO': "False, True, False",
            'THREE': "False, False, True"
        }

        km = wm.keyconfigs.default.keymaps['Mesh']
        for k, v in my_keymap.items():
            new_shortcut = km.keymap_items.new('wm.context_set_value', k, 'PRESS')
            new_shortcut.properties.data_path = 'tool_settings.mesh_select_mode'
            new_shortcut.properties.value = v

    print('complete')


def vtx_specials(self, m):
    '''
    [1] checks if the addon is enabled by testing a known operator
    [2] if operator is not present, tries to enable the addon.
    [3] If it fails to enable the addon the function returns early.
        [ arguably this should suggest download + install + enable ]
    [4] If the function is found, it calls the specified function.
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


def remove_obj_and_mesh(context):
    scene = context.scene
    objs = bpy.data.objects
    meshes = bpy.data.meshes
    for obj in objs:
        if obj.type == 'MESH':
            scene.objects.unlink(obj)
            objs.remove(obj)
    for mesh in meshes:
        meshes.remove(mesh)


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
