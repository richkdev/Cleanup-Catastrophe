# /// script
# dependencies = [
#  "pygame-ce",
#  "zengl"
# ]
# ///

# run this command
#   pygbag --PYBUILD 3.12 --ume_block 0 --template noctx.tmpl "tests\zengl_test\main.py"

import asyncio
import pygame
import zengl

pygame.init()
screen = pygame.display.set_mode((640, 480), flags=pygame.OPENGL, vsync=True)

pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_ES)

ctx = zengl.context()

window_size = pygame.display.get_window_size()
screen_texture = ctx.image(window_size, 'rgba8unorm')

vertexShader = """
#version 300 es

precision highp float;

vec2 vertices[3] = vec2[](
    vec2(-1.0, -1.0),
    vec2(3.0, -1.0),
    vec2(-1.0, 3.0)
);

out lowp vec2 vertex;

void main() {
    gl_Position = vec4(vertices[gl_VertexID], 0.0, 1.0);
    vertex = vertices[gl_VertexID];
}
"""

fragmentShader = """
#version 300 es

precision highp float;

uniform sampler2D screen_texture;

in lowp vec2 vertex;

layout (location = 0) out vec4 out_color;

void main() {
    vec2 uv = vertex * 0.5 + 0.5;
    vec4 color2 = texture(screen_texture, uv);
    out_color = color2 * color2.a;
}
"""

pipeline = ctx.pipeline(
    vertex_shader=vertexShader,
    fragment_shader=fragmentShader,
    layout=[
        {
            'name': 'screen_texture',
            'binding': 0,
        },
    ],
    resources=[
        {
            'type': 'sampler',
            'binding': 0,
            'image': screen_texture,
        },
    ],
    framebuffer=None,
    viewport=(0, 0, *window_size),
    topology='triangles',
    vertex_count=3,
)

rectangle = pygame.Surface((100, 200))
rectangle.fill(pygame.Color(255, 255, 255))

clock = pygame.Clock()
FPS = 100

running = True

async def main():
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ctx.new_frame()
        screen.fill(pygame.Color(0, 0, 0))
        screen.blit(rectangle, (10, 10))

        screen_texture.write(pygame.image.tobytes(screen, 'RGBA', flipped=True))
        pipeline.render()
        ctx.end_frame()

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)
    pygame.quit()

asyncio.run(main())
