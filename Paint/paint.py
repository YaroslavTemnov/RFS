import pygame
import math

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
    else:
        color = (0, 0, 0)
    
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

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Advanced Paint Tool")
    clock = pygame.time.Clock()
    

    radius = 10  
    color_mode = 'blue'  
    tool = 'pen'  
    drawing = False  
    start_pos = (0, 0)  
    points = []
    

    colors = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'purple': (255, 0, 255),
        'white': (255, 255, 255)
    }
    
    font = pygame.font.Font(None, 24)
    
    running = True
    while running:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    running = False
                if event.key == pygame.K_F4 and alt_held:
                    running = False
                if event.key == pygame.K_ESCAPE:
                    running = False
                

                if event.key == pygame.K_1:
                    color_mode = 'red'
                elif event.key == pygame.K_2:
                    color_mode = 'green'
                elif event.key == pygame.K_3:
                    color_mode = 'blue'
                elif event.key == pygame.K_4:
                    color_mode = 'yellow'
                elif event.key == pygame.K_5:
                    color_mode = 'purple'
                elif event.key == pygame.K_6:
                    color_mode = 'white'
                

                elif event.key == pygame.K_p:  
                    tool = 'pen'
                elif event.key == pygame.K_r:  
                    tool = 'rectangle'
                elif event.key == pygame.K_c:
                    tool = 'circle'
                elif event.key == pygame.K_s:  
                    tool = 'square'
                elif event.key == pygame.K_t:  
                    tool = 'right_triangle'
                elif event.key == pygame.K_e: 
                    tool = 'equilateral_triangle'
                elif event.key == pygame.K_h:  
                    tool = 'rhombus'
                elif event.key == pygame.K_x: 
                    tool = 'eraser'
                

                elif event.key == pygame.K_UP:
                    radius = min(50, radius + 2)
                elif event.key == pygame.K_DOWN:
                    radius = max(1, radius - 2)
                
                elif event.key == pygame.K_SPACE:
                    points = []
                    screen.fill((0, 0, 0))
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    drawing = True
                    start_pos = event.pos
                    if tool == 'pen' or tool == 'eraser':
                        points.append(event.pos)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:  
                    drawing = False
                    end_pos = event.pos
                    current_color = colors[color_mode] if tool != 'eraser' else (0, 0, 0)
                    line_width = radius if tool == 'eraser' else max(1, radius // 2)
                    
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
            
            if event.type == pygame.MOUSEMOTION:
                if drawing and (tool == 'pen' or tool == 'eraser'):
                    points.append(event.pos)
                    points = points[-256:]  
        
        if tool == 'pen':
            i = 0
            while i < len(points) - 1:
                drawLineBetween(screen, i, points[i], points[i + 1], radius, color_mode)
                i += 1
        elif tool == 'eraser':
            i = 0
            while i < len(points) - 1:
                drawLineBetween(screen, i, points[i], points[i + 1], radius, 'black')
                i += 1
        

        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()


main()