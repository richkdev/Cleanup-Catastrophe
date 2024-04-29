from scripts.settings import vertexShader, fragmentShader, newPath
from array import array
from struct import pack

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

## normal shader
# program['tex'] = 0
# render_object = ctx.vertex_array(
#     program, [
#       (quad_buffer, '2f 2f', 'vert', 'texcoord')])

## crt shader
render_object = ctx.vertex_array(
    program, [
        (ctx.buffer(pack('8f', *[-1, -1,  1, -1, -1,  1,  1,  1])), '2f', 'vert'),
        (ctx.buffer(pack('8f', *[0, 1,  1, 1, 0, 0,  1, 0])), '2f', 'in_text')
    ],
    ctx.buffer(pack('6I', *[0, 1, 2, 1, 2, 3])))

def surf_to_texture(surf):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = "BGRA"
    tex.write(surf.get_view('1'))
    return tex
