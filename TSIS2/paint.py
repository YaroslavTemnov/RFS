import pygame
import math
from datetime import datetime
import sys

def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))
    
    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)
    elif color_mode == 'yellow':
        color = (c2, c2, c1)
    elif color_mode == 'purple':
        color = (c2, c1, c2)
    elif color_mode == 'black':
        color = (0, 0, 0)
    else:
        color = (255, 255, 255)
    
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

def draw_rectangle(screen, start, end, color, width):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(start[0] - end[0])
    h = abs(start[1] - end[1])
    pygame.draw.rect(screen, color, (x, y, w, h), width)

def draw_circle(screen, start, end, color, width):
    center = start
    radius = int(math.hypot(end[0] - start[0], end[1] - start[1]))
    pygame.draw.circle(screen, color, center, radius, width)

def draw_square(screen, start, end, color, width):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    side = max(abs(start[0] - end[0]), abs(start[1] - end[1]))
    pygame.draw.rect(screen, color, (x, y, side, side), width)

def draw_right_triangle(screen, start, end, color, width):
    points = [start, (start[0], end[1]), end]
    pygame.draw.polygon(screen, color, points, width)

def draw_equilateral_triangle(screen, start, end, color, width):
    base = abs(start[0] - end[0])
    height = math.sqrt(3) / 2 * base
    if end[0] > start[0]:
        third_x = (start[0] + end[0]) / 2
    else:
        third_x = (end[0] + start[0]) / 2
    third_y = start[1] - height if start[1] > end[1] else start[1] + height
    points = [start, end, (third_x, third_y)]
    pygame.draw.polygon(screen, color, points, width)

def draw_rhombus(screen, start, end, color, width):
    center_x = (start[0] + end[0]) // 2
    center_y = (start[1] + end[1]) // 2
    dx = abs(start[0] - end[0]) // 2
    dy = abs(start[1] - end[1]) // 2
    points = [
        (center_x, center_y - dy),  
        (center_x + dx, center_y),  
        (center_x, center_y + dy),  
        (center_x - dx, center_y)   
    ]
    pygame.draw.polygon(screen, color, points, width)

def flood_fill(surface, x, y, target_color, replacement_color):
    """Flood fill algorithm using stack (iterative)"""
    if target_color == replacement_color:
        return
    
    surface.lock()
    h = surface.get_height()
    w = surface.get_width()
    
    stack = [(x, y)]
    while stack:
        px, py = stack.pop()
        if px < 0 or px >= w or py < 0 or py >= h:
            continue
        
        if surface.get_at((px, py)) != target_color:
            continue
        
        surface.set_at((px, py), replacement_color)
        
        stack.append((px + 1, py))
        stack.append((px - 1, py))
        stack.append((px, py + 1))
        stack.append((px, py - 1))
    
    surface.unlock()

def draw_line_preview(screen, start, end, color, width):
    """Draw a line for preview"""
    pygame.draw.line(screen, color, start, end, width)

    
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Advanced Paint Tool")
clock = pygame.time.Clock()
    
brush_sizes = {pygame.K_1: 2, pygame.K_2: 5, pygame.K_3: 10}
radius = 5 
    
color_mode = 'blue'
tool = 'pen'
drawing = False
start_pos = (0, 0)
points = []  # Для pen и eraser
    
line_start = None
text_active = False
text_content = ""
text_position = (0, 0)
text_rendered = False 
font = pygame.font.Font(None, 36)
    
colors = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'purple': (255, 0, 255),
    'white': (255, 255, 255),
    'black': (0, 0, 0)
}
    
    
canvas = screen.copy()
    
running = True
while running:
    pressed = pygame.key.get_pressed()
    alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
    ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

    if tool == 'line' and line_start and drawing and not text_active:
        screen.blit(canvas, (0, 0))
        current_color = colors[color_mode]
        draw_line_preview(screen, line_start, pygame.mouse.get_pos(), current_color, radius)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and ctrl_held:
                running = False
            if event.key == pygame.K_F4 and alt_held:
                running = False
                
            if event.key == pygame.K_s and ctrl_held:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"canvas_{timestamp}.png"
                pygame.image.save(screen, filename)
                print(f"Canvas saved as {filename}")
                
            if text_active:
                if event.key == pygame.K_RETURN:
                    if text_content:
                        text_surface = font.render(text_content, True, colors[color_mode])
                        screen.blit(text_surface, text_position)
                        canvas = screen.copy()
                        text_rendered = True
                    text_active = False
                    text_content = ""
                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                    text_content = ""
                    text_rendered = False
                elif event.key == pygame.K_BACKSPACE:
                    text_content = text_content[:-1]
                else:
                    if event.unicode and event.unicode.isprintable() and len(event.unicode) == 1:
                        text_content += event.unicode
                continue  
                
            if event.key == pygame.K_ESCAPE:
                running = False
            
            if event.key in brush_sizes:
                radius = brush_sizes[event.key]
                print(f"Brush size changed to {radius}px")
            
            if event.key == pygame.K_4 and not ctrl_held:
                color_mode = 'red'
            elif event.key == pygame.K_5 and not ctrl_held:
                color_mode = 'green'
            elif event.key == pygame.K_6 and not ctrl_held:
                color_mode = 'blue'
            elif event.key == pygame.K_7:
                color_mode = 'yellow'
            elif event.key == pygame.K_8:
                color_mode = 'purple'
            elif event.key == pygame.K_9:
                color_mode = 'white'
            elif event.key == pygame.K_0:
                color_mode = 'black'
            
            if event.key == pygame.K_p:
                tool = 'pen'
                points = []  
                print("Tool: Pencil")
            elif event.key == pygame.K_l:
                tool = 'line'
                points = []
                print("Tool: Line")
            elif event.key == pygame.K_r:
                tool = 'rectangle'
                points = []
                print("Tool: Rectangle")
            elif event.key == pygame.K_c:
                tool = 'circle'
                points = []
                print("Tool: Circle")
            elif event.key == pygame.K_s and not ctrl_held:
                tool = 'square'
                points = []
                print("Tool: Square")
            elif event.key == pygame.K_t:
                tool = 'right_triangle'
                points = []
                print("Tool: Right Triangle")
            elif event.key == pygame.K_e:
                tool = 'equilateral_triangle'
                points = []
                print("Tool: Equilateral Triangle")
            elif event.key == pygame.K_h:
                tool = 'rhombus'
                points = []
                print("Tool: Rhombus")
            elif event.key == pygame.K_x:
                tool = 'eraser'
                points = []  
                print("Tool: Eraser")
            elif event.key == pygame.K_f:
                tool = 'fill'
                points = []
                print("Tool: Fill")
            elif event.key == pygame.K_g:
                tool = 'text'
                points = []
                print("Tool: Text ")

            if event.key == pygame.K_UP:
                radius = min(50, radius + 2)
                print(f"Brush size: {radius}px")
            elif event.key == pygame.K_DOWN:
                radius = max(1, radius - 2)
                print(f"Brush size: {radius}px")
            
            if event.key == pygame.K_SPACE:
                points = []
                screen.fill((0, 0, 0))
                canvas = screen.copy()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not text_active:
                drawing = True
                start_pos = event.pos
                
                if tool == 'pen':
                    points = [event.pos] 
                elif tool == 'eraser':
                    points = [event.pos]  
                elif tool == 'line':
                    line_start = event.pos
                elif tool == 'fill':
                    try:
                        target_color = screen.get_at(event.pos)
                        replacement_color = colors[color_mode]
                        flood_fill(screen, event.pos[0], event.pos[1], target_color, replacement_color)
                        canvas = screen.copy()
                    except Exception as e:
                        print(f"Flood fill error: {e}")
                elif tool == 'text':
                    text_active = True
                    text_position = event.pos
                    text_content = ""
                    text_rendered = False
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing and not text_active:
                drawing = False
                end_pos = event.pos
                current_color = colors[color_mode] if tool != 'eraser' else (0, 0, 0)
                line_width = radius
                
                if tool == 'rectangle':
                    draw_rectangle(screen, start_pos, end_pos, current_color, line_width)
                elif tool == 'circle':
                    draw_circle(screen, start_pos, end_pos, current_color, line_width)
                elif tool == 'square':
                    draw_square(screen, start_pos, end_pos, current_color, line_width)
                elif tool == 'right_triangle':
                    draw_right_triangle(screen, start_pos, end_pos, current_color, line_width)
                elif tool == 'equilateral_triangle':
                    draw_equilateral_triangle(screen, start_pos, end_pos, current_color, line_width)
                elif tool == 'rhombus':
                    draw_rhombus(screen, start_pos, end_pos, current_color, line_width)
                elif tool == 'line':
                    draw_line_preview(screen, start_pos, end_pos, current_color, line_width)
                
                canvas.blit(screen, (0, 0))
                line_start = None
                points = [] 
        
        if event.type == pygame.MOUSEMOTION:
            if drawing and (tool == 'pen' or tool == 'eraser') and not text_active:
                points.append(event.pos)
                points = points[-256:]  
    
    if not text_active:
        if tool == 'pen' and len(points) > 1:
            screen.blit(canvas, (0, 0))
            i = 0
            while i < len(points) - 1:
                drawLineBetween(screen, i, points[i], points[i + 1], radius, color_mode)
                i += 1
            canvas.blit(screen, (0, 0))
        elif tool == 'eraser' and len(points) > 1:
            screen.blit(canvas, (0, 0))
            i = 0
            while i < len(points) - 1:
                drawLineBetween(screen, i, points[i], points[i + 1], radius, 'black')
                i += 1
            canvas.blit(screen, (0, 0))
    
    if text_active and not text_rendered:
        screen.blit(canvas, (0, 0))
        cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
        text_surface = font.render(text_content + cursor, True, colors[color_mode])
        screen.blit(text_surface, text_position)

    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
