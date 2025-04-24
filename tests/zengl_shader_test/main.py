# /// script
# dependencies = [
#  "pygame-ce",
#  "zengl"
# ]
# ///

# run this command
#   pygbag --PYBUILD 3.12 --git --ume_block 0 --template noctx.tmpl "tests/zengl_shader_test/main.py"

# thanks to @szabolcsdombi for the help!
# discussion: https://discord.com/channels/550302843777712148/1333440038293209171


import asyncio
import pygame
import zengl
import struct

pygame.init()

screen_size = (300, 300)

screen = pygame.display.set_mode(screen_size, flags=pygame.OPENGL, vsync=True)

ctx = zengl.context()

pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_ES)

vertexShader = """
#version 300 es

layout (location = 0) in vec2 vert;
layout (location = 1) in vec2 in_text;
out vec2 vertex;

void main() {
    gl_Position = vec4(vert, 0.0, 1.0);
    vertex = in_text;
}
"""

fragmentShader = """
#version 300 es

precision mediump float;
uniform sampler2D MainTexture;

in vec2 vertex;
out vec4 color;

void main() {
    float flatness = 2.7; // 2.7 = crt, 10.0 = flatscreen
    float distance = 1.05; // 1.0-1.5, distance from screen

    vec2 center = vec2(0.5, 0.5);
    vec2 off_center = vertex - center;

    off_center *= vec2(distance) + 0.8 * pow(abs(off_center.yx), vec2(flatness));

    vec2 v_text2 = center+off_center;

    if (v_text2.x > 1.0 || v_text2.x < 0.0 || v_text2.y > 1.0 || v_text2.y < 0.0){
        color = vec4(0.0, 0.0, 0.0, 1.0);
    } else {
        color = vec4(texture(MainTexture, v_text2).rgb, 1.0);
        float fv = fract(v_text2.y * float(textureSize(MainTexture,0).y));
        fv = min(1.0, 0.8+0.5*min(fv, 1.0-fv));
        color.rgb *= fv;
    }
}
"""

screen_texture = ctx.image(screen_size, 'rgba8unorm')

vertexBuffer = ctx.buffer(data=struct.pack('8f', *[-1, -1, 1, -1, -1, 1, 1, 1]), index=False)
instanceBuffer = ctx.buffer(data=struct.pack('8f', *[0, 1, 1, 1, 0, 0, 1, 0]), index=False)
indexBuffer = ctx.buffer(data=struct.pack('6I', *[0, 1, 2, 1, 2, 3]), index=True)

pipeline = ctx.pipeline(
    vertex_shader=vertexShader,
    fragment_shader=fragmentShader,
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
    viewport=(0, 0, *screen_size),
    topology='triangles',
    vertex_buffers=(
        *zengl.bind(vertexBuffer, '2f', 0),
        *zengl.bind(instanceBuffer, '2f', 1),
    ),
    index_buffer=indexBuffer,
    vertex_count=indexBuffer.size//4,
)

rectangle = pygame.Surface((100, 200))
rectangle.fill(pygame.Color(255, 255, 255))

clock = pygame.Clock()
FPS = 60

print(screen_size, screen_texture.size)

async def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 255, 0))
        screen.blit(rectangle, (10, 10))

        ctx.new_frame()
        screen_texture.clear()

        screen_texture.write(data=pygame.image.tobytes(screen, 'RGBA', flipped=False), size=screen_size)
        pipeline.render()

        clock.tick(FPS)

        pygame.display.flip()
        ctx.end_frame()

        await asyncio.sleep(0)
    pygame.quit()

asyncio.run(main())
