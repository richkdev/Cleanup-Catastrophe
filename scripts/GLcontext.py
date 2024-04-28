from scripts.settings import vertexShader, fragmentShader, newPath
from array import array

import moderngl
ctx = moderngl.create_context()

print("ModernGL context found")

quad_buffer = ctx.buffer(data=array('f', [
    -1.0, 1.0, 0.0, 0.0,  # topleft
    1.0, 1.0, 1.0, 0.0,   # topright
    -1.0, -1.0, 0.0, 1.0, # bottomleft
    1.0, -1.0, 1.0, 1.0,  # bottomright
]))

program = ctx.program(vertex_shader=open(newPath(vertexShader)).read(),
                      fragment_shader=open(newPath(fragmentShader)).read())
render_object = ctx.vertex_array(
    program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])


def surf_to_texture(surf):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = "BGRA"
    tex.write(surf.get_view('1'))
    return tex
