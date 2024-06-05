from struct import pack
from array import array
from scripts.settings import *


import moderngl

from array import array


try:
    ctx = moderngl.create_context(require=300)
    program = ctx.program(
        vertex_shader=open(vertexShader).read(),
        fragment_shader=open(fragmentShader).read()
    )
except Exception as e:
    print(e)

if ("normal.glsl" in vertexShader) and ("normal.glsl" in fragmentShader):
    render_object = ctx.vertex_array(
        program, [(ctx.buffer(data=array('f', [
            -1.0,  1.0, 0.0, 0.0,  # topleft
            1.0,  1.0, 1.0, 0.0,   # topright
            -1.0, -1.0, 0.0, 1.0,  # bottomleft
            1.0, -1.0, 1.0, 1.0,   # bottomright
        ])), '2f 2f', 'vert', 'texcoord')]
    )

elif ("crt.glsl" in vertexShader) and ("crt.glsl" in fragmentShader):
    render_object = ctx.vertex_array(
        program, [(ctx.buffer(pack('8f', *[-1, -1,  1, -1, -1,  1,  1,  1])), '2f', 'vert'),
                  (ctx.buffer(pack('8f', *[0, 1,  1, 1, 0, 0,  1, 0])), '2f', 'in_text')],
        ctx.buffer(pack('6I', *[0, 1, 2, 1, 2, 3]))
    )

else:
    raise NotImplementedError


def surf_to_texture(surf: pygame.surface.Surface):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (0x2600, 0x2600)  # aka (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = "BGRA"
    tex.write(surf.get_view('1'))
    return tex
