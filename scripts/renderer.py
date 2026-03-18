import zengl
import struct
from scripts import globals

ctx = zengl.context()

screen_texture = ctx.image(size=globals.SCREEN_SIZE, format='rgba8unorm')


match not globals.retroMode:
    case True:
        pipeline = ctx.pipeline(
            vertex_shader=open(globals.vertShader_path).read(),
            fragment_shader=open(globals.fragShader_path).read(),
            layout=[
                {
                    'name': 'MainTexture',
                    'binding': 0,
                },
            ],
            resources=[
                {
                    'type': 'sampler',
                    'binding': 0,
                    'image': screen_texture,
                    'wrap_x': 'clamp_to_edge',
                    'wrap_y': 'clamp_to_edge',
                    'min_filter': 'linear',
                    'mag_filter': 'linear',
                }
            ],
            framebuffer=None,
            viewport=(0, 0, *globals.SCREEN_SIZE),
            topology='triangles',
            vertex_count=3,
        )
    case False:
        vbo = ctx.buffer(data=struct.pack('8f', *[-1, -1, 1, -1, -1, 1, 1, 1]), index=False)
        uvmap = ctx.buffer(data=struct.pack('8f', *[0, 1, 1, 1, 0, 0, 1, 0]), index=False)
        ibo = ctx.buffer(data=struct.pack('6I', *[0, 1, 2, 1, 2, 3]), index=True)

        pipeline = ctx.pipeline(
            vertex_shader=open(globals.vertShader_path, 'r').read(),
            fragment_shader=open(globals.fragShader_path, 'r').read(),
            layout=[
                {
                    'name': 'MainTexture',
                    'binding': 0,
                },
            ],
            resources=[
                {
                    'type': 'sampler',
                    'binding': 0,
                    'image': screen_texture,
                    'wrap_x': 'clamp_to_edge',
                    'wrap_y': 'clamp_to_edge',
                    'min_filter': 'nearest',
                    'mag_filter': 'nearest',
                }
            ],
            framebuffer=None,
            viewport=(0, 0, *globals.SCREEN_SIZE),
            topology='triangles',
            vertex_buffers=(
                *zengl.bind(vbo, '2f', 0),
                *zengl.bind(uvmap, '2f', 1),
            ),
            index_buffer=ibo,
            vertex_count=ibo.size//4,
        )
