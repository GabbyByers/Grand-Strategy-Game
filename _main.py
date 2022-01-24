import os, pygame.gfxdraw, pygame, math, random, time, statistics
from matplotlib.image import imread
from _preload import metadata
pygame.init()
DisplayX, DisplayY = 1440,900
win = pygame.display.set_mode((DisplayX, DisplayY))
pygame.display.set_caption("template")
White = (255,255,255)
Black = (0,0,0)
Blue = (0,0,255)
Ocean_Blue = (20,20,110)
Green = (30,170,30)
Darker_Green = (35,140,35)
Red = (255,0,0)
Gray = (150,150,150)
Purple = (255,0,255)
Yellow = (255,255,0)
Brown = (139,69,19)
font = pygame.font.SysFont('courier', 20, True)
pi = 3.141592653589793
scale = 4
global_x = 0
global_y = 0

def user_controls():
    global global_x,global_y
    if MouseScroll:
        global_x += Mouse_RelX
        global_y += Mouse_RelY

def draw_fps():
    ms = statistics.mean(milliseconds)
    ms_text  = font.render(str(round(ms,2))+" ms", 1, White)
    win.blit(ms_text, (2,0))
    if ms != 0:
        fps = font.render(str(round(1000/ms))+" FPS", 1, White)
        win.blit(fps, (2,20))

def province_mouseover():
    i = (MouseX-global_x)//scale
    j = (MouseY-global_y)//scale
    many_mice = []
    for province in provinces:
        if (province.boundry.i <= i < province.boundry.i+province.boundry.di) and (province.boundry.j <= j < province.boundry.j+province.boundry.dj):
            many_mice.append(province)
    for province in many_mice:
        for strip in province.strips:
            if (strip.i <= i <= strip.i+strip.length-1) and (strip.j == j):
                return province
    return 0

class province_object:
    def __init__(self):
        self.tiles = []
        self.strips = []
        self.border_tiles = []
        self.outline_tiles = []
        self.outline_strips_horizontal = []
        self.outline_strips_vertical = []
        self.neighbours = []
        self.debug_colour = 0
        self.debug_colour_dark = 0
        self.boundry = 0
        self.surface = 0
        self.centre = 0
    def draw_province(self,colour):
        for strip in self.strips:
            strip.draw_strip(colour)
    def draw_outline(self,colour):
        for strip in self.outline_strips_horizontal:
            strip.draw_strip_horizontal(colour)
        for strip in self.outline_strips_vertical:
            strip.draw_strip_vertical(colour)
    def generate_surface(self,colour,colour2):
        self.surface = pygame.Surface((self.boundry.di*scale,self.boundry.dj*scale), pygame.SRCALPHA)
        for strip in self.strips:
            pygame.draw.rect(self.surface, colour, ((strip.i-self.boundry.i)*scale,(strip.j-self.boundry.j)*scale,strip.length*scale,scale))
        for strip in self.outline_strips_horizontal:
            pygame.draw.rect(self.surface, colour2, ((strip.i-self.boundry.i)*scale,(strip.j-self.boundry.j)*scale,strip.length*scale,scale))
        for strip in self.outline_strips_vertical:
            pygame.draw.rect(self.surface, colour2, ((strip.i-self.boundry.i)*scale,(strip.j-self.boundry.j)*scale,scale,strip.length*scale))
    def draw_surface(self):
        win.blit(self.surface, (global_x+self.boundry.i*scale,global_y+self.boundry.j*scale))

class boundry_object:
    def __init__(self,i,j,di,dj):
        self.i = i
        self.j = j
        self.di = di
        self.dj = dj
    def draw_boundry(self,colour):
        pygame.draw.rect(win, colour, (global_x+self.i*scale,global_y+self.j*scale,self.di*scale,self.dj*scale),1)

class tile_object:
    def __init__(self,i,j):
        self.i = i
        self.j = j
    def draw_tile(self,colour):
        pygame.draw.rect(win, colour, (global_x+self.i*scale,global_y+self.j*scale,scale,scale))

class strip_object:
    def __init__(self,i,j,length):
        self.i = i
        self.j = j
        self.length = length
    def draw_strip(self,colour):
        pygame.draw.rect(win, colour, (global_x+self.i*scale,global_y+self.j*scale,self.length*scale,scale))
    def draw_strip_horizontal(self,colour):
        pygame.draw.rect(win, colour, (global_x+self.i*scale,global_y+self.j*scale,self.length*scale,scale))
    def draw_strip_vertical(self,colour):
        pygame.draw.rect(win, colour, (global_x+self.i*scale,global_y+self.j*scale,scale,self.length*scale))

LOAD_FROM_METADATA = True
picture = imread("mastermap.png")

if LOAD_FROM_METADATA:
    provinces = []
    for block in metadata:
        province = province_object()
        for strip_data in block[0]:
            strip = strip_object(strip_data[0],strip_data[1],strip_data[2])
            province.strips.append(strip)
        for strip_data in block[1]:
            strip = strip_object(strip_data[0],strip_data[1],strip_data[2])
            province.outline_strips_vertical.append(strip)
        for strip_data in block[2]:
            strip = strip_object(strip_data[0],strip_data[1],strip_data[2])
            province.outline_strips_horizontal.append(strip)
        provinces.append(province)
    for block in metadata:
        province = provinces[metadata.index(block)]
        for neighbour_index in block[3]:
            province.neighbours.append(provinces[neighbour_index])
        province.boundry = boundry_object(block[4][0],block[4][1],block[4][2],block[4][3])
        if len(block[5]) == 1:
            province.centre = 0
        else:
            province.centre = tile_object(block[5][0],block[5][1])
            
def output_metadata():
    print("metadata = [")
    for province in provinces:
        #block start
        print("[")

        #block[0]
        print("[")
        for strip in province.strips:
            print("("+str(strip.i)+","+str(strip.j)+","+str(strip.length)+"),")
        print("],")

        #block[1]
        print("[")
        for strip in province.outline_strips_vertical:
            print("("+str(strip.i)+","+str(strip.j)+","+str(strip.length)+"),")
        print("],")

        #block[2]
        print("[")
        for strip in province.outline_strips_horizontal:
            print("("+str(strip.i)+","+str(strip.j)+","+str(strip.length)+"),")
        print("],")

        #block[3]
        print("[")
        for neighbour in province.neighbours:
            print(str(provinces.index(neighbour))+",")
        print("],")

        #block[4]
        print("[")
        print(str(province.boundry.i)+","+str(province.boundry.j)+","+str(province.boundry.di)+","+str(province.boundry.dj))
        print("],")

        #block[5]
        print("[")
        if province.centre != 0:
            print(str(province.centre.i)+","+str(province.centre.j))
        else: print(0)
        print("],")

        #block end
        print("],")
    print("]")
    
if not LOAD_FROM_METADATA:
    #Count Colours
    def debug_print(text):
        t = font.render(text, 1, White)
        win.fill(Black)
        win.blit(t, (300,300))
        pygame.display.update()
    def rgb_from_depth(depth):
        return (int(255*depth[0]),
                int(255*depth[1]),
                int(255*depth[2]))
    colours = []
    for j in range(len(picture)):
        for i in range(len(picture[0])):
            colour = rgb_from_depth(picture[j][i])
            if colour != (255,255,255) and not colour in colours:
                colours.append(colour)
                debug_print("Discovering Colours: "+str(len(colours)))
    #Generate Provinces
    provinces = []
    explored_colours = []
    for j in range(len(picture)):
        for i in range(len(picture[0])):
            colour = rgb_from_depth(picture[j][i])
            if colour != (255,255,255) and not colour in explored_colours:
                debug_print("Generating Provinces: "+str(len(explored_colours))+"/"+str(len(colours)))
                explored_colours.append(colour)
                province = province_object()
                for j in range(len(picture)):
                    for event in pygame.event.get():
                        pass
                    for i in range(len(picture[0])):
                        colour_sample = rgb_from_depth(picture[j][i])
                        if colour == colour_sample:
                            province.tiles.append(tile_object(i,j))
                province.debug_colour = colour
                province.debug_colour_dark = (int(0.8*colour[0]),int(0.8*colour[1]),int(0.8*colour[2]))
                provinces.append(province)
    #Discover Border Tiles
    for province in provinces:
        debug_print("Border Tiles: "+str(provinces.index(province))+"/"+str(len(colours)))
        for event in pygame.event.get():
            pass
        for tile in province.tiles:
            province.border_tiles.append(tile_object(tile.i+1,tile.j))
            province.border_tiles.append(tile_object(tile.i-1,tile.j))
            province.border_tiles.append(tile_object(tile.i,tile.j+1))
            province.border_tiles.append(tile_object(tile.i,tile.j-1))
        #Remove Border Tiles Inside Province
        pruned_border_tiles = []
        for border_tile in province.border_tiles:
            legal = True
            for tile in province.tiles:
                if border_tile.i == tile.i and border_tile.j == tile.j:
                    legal = False
                    break
            if legal: pruned_border_tiles.append(border_tile)
        province.border_tiles = pruned_border_tiles
        #Remove Duplicate Border Tiles
        pruned_border_tiles = []
        for border_tile in province.border_tiles:
            legal = True
            for tile in pruned_border_tiles:
                if tile.i == border_tile.i and tile.j == border_tile.j:
                    legal = False
                    break
            if legal: pruned_border_tiles.append(border_tile)
        province.border_tiles = pruned_border_tiles
    #Discover Outline Tiles
    for province in provinces:
        debug_print("Outline Tiles: "+str(provinces.index(province))+"/"+str(len(colours)))
        for event in pygame.event.get():
            pass
        for border_tile in province.border_tiles:
            province.outline_tiles.append(tile_object(border_tile.i+1,border_tile.j))
            province.outline_tiles.append(tile_object(border_tile.i-1,border_tile.j))
            province.outline_tiles.append(tile_object(border_tile.i,border_tile.j+1))
            province.outline_tiles.append(tile_object(border_tile.i,border_tile.j-1))
        pruned_outline_tiles = []
        for outline_tile in province.outline_tiles:
            legal = False
            for tile in province.tiles:
                if tile.i == outline_tile.i and tile.j == outline_tile.j:
                    legal = True
                    break
            if legal: pruned_outline_tiles.append(outline_tile)
        province.outline_tiles = pruned_outline_tiles
        pruned_outline_tiles = []
        for outline_tile in province.outline_tiles:
            legal = True
            for tile in pruned_outline_tiles:
                if tile.i == outline_tile.i and tile.j == outline_tile.j:
                    legal = False
                    break
            if legal: pruned_outline_tiles.append(outline_tile)
        province.outline_tiles = pruned_outline_tiles
    #Discover Neighbours
    for province in provinces:
        debug_print("Discovering Neighbours: "+str(provinces.index(province))+"/"+str(len(colours)))
        for border_tile in province.border_tiles:
            for event in pygame.event.get():
                pass
            for neighbour_candidate in provinces:
                legal = False
                if province != neighbour_candidate:
                    for outline_tile in neighbour_candidate.outline_tiles:
                        if outline_tile.i == border_tile.i and outline_tile.j == border_tile.j:
                            legal = True
                    if legal and not neighbour_candidate in province.neighbours:
                        province.neighbours.append(neighbour_candidate)
    #Crude Boundry Box
    for province in provinces:
        debug_print("Crude Boundry Box: "+str(provinces.index(province))+"/"+str(len(colours)))
        for event in pygame.event.get():
            pass
        min_i = province.outline_tiles[0].i
        min_j = province.outline_tiles[0].j
        for outline_tile in province.outline_tiles:
            if outline_tile.i < min_i:
                min_i = outline_tile.i
            if outline_tile.j < min_j:
                min_j = outline_tile.j
        max_i = province.border_tiles[0].i
        max_j = province.border_tiles[0].j
        for border_tile in province.border_tiles:
            if border_tile.i > max_i:
                max_i = border_tile.i
            if border_tile.j > max_j:
                max_j = border_tile.j
        province.boundry = boundry_object(min_i,min_j,max_i-min_i,max_j-min_j)
    #Generate Strips
    for province in provinces:
        debug_print("Generate Strips: "+str(provinces.index(province))+"/"+str(len(colours)))
        for event in pygame.event.get():
            pass
        prev_tile = province.tiles[0]
        this_strip = strip_object(prev_tile.i,prev_tile.j,1)
        for tile in province.tiles:
            if province.tiles.index(tile) != 0:
                if prev_tile.i + 1 == tile.i and prev_tile.j == tile.j:
                    this_strip.length += 1
                else:
                    province.strips.append(this_strip)
                    this_strip = strip_object(tile.i,tile.j,1)
                prev_tile = tile
        province.strips.append(this_strip)
    #Generate Outline Strips
        #Sort
    for province in provinces:
        debug_print("Sorting Outline Strips: "+str(provinces.index(province))+"/"+str(len(colours)))
        for event in pygame.event.get():
            pass
        sorted_outline_tiles = []
        while len(province.outline_tiles) != 0:
            smallest_outline_tile = province.outline_tiles[0]
            for outline_tile in province.outline_tiles:
                if outline_tile.j < smallest_outline_tile.j:
                    smallest_outline_tile = outline_tile
                elif outline_tile.j == smallest_outline_tile.j:
                    if outline_tile.i < smallest_outline_tile.i:
                        smallest_outline_tile = outline_tile
            province.outline_tiles.remove(smallest_outline_tile)
            sorted_outline_tiles.append(smallest_outline_tile)
        province.outline_tiles = sorted_outline_tiles
        #Generate Horizontal Strips
    for province in provinces:
        debug_print("Generating Horizontal Outline Strips: "+str(provinces.index(province))+"/"+str(len(colours)))
        for event in pygame.event.get():
            pass
        prev_outline_tile = province.outline_tiles[0]
        this_strip = strip_object(prev_outline_tile.i,prev_outline_tile.j,1)
        for outline_tile in province.outline_tiles:
            if province.outline_tiles.index(outline_tile) != 0:
                if prev_outline_tile.i + 1 == outline_tile.i and prev_outline_tile.j == outline_tile.j:
                    this_strip.length += 1
                else:
                    province.outline_strips_horizontal.append(this_strip)
                    this_strip = strip_object(outline_tile.i,outline_tile.j,1)
                prev_outline_tile = outline_tile
        province.outline_strips_horizontal.append(this_strip)
        #Remove Single Length Strips
    for province in provinces:
        debug_print("Generating Vertical Outline Strips: "+str(provinces.index(province))+"/"+str(len(colours)))
        for event in pygame.event.get():
            pass
        pruned_strips = []
        single_length_strips = []
        for strip in province.outline_strips_horizontal:
            if strip.length != 1:
                pruned_strips.append(strip)
            else:
                single_length_strips.append(strip)
        province.outline_strips_horizontal = pruned_strips
        remainder_tiles = []
        #Convert Strip to Tiles
        for strip in single_length_strips:
            remainder_tiles.append(tile_object(strip.i,strip.j))
        sorted_remainder_tiles = []
        #Sort
        while len(remainder_tiles) != 0:
            smallest_tile = remainder_tiles[0]
            for tile in remainder_tiles:
                if tile.i < smallest_tile.i:
                    smallest_tile = tile
                elif tile.i == smallest_tile.i:
                    if tile.j < smallest_tile.j:
                        smallest_tile = tile
            remainder_tiles.remove(smallest_tile)
            sorted_remainder_tiles.append(smallest_tile)
        #Generate Vertical Strips
        prev_outline_tile = sorted_remainder_tiles[0]
        this_strip = strip_object(prev_outline_tile.i,prev_outline_tile.j,1)
        for outline_tile in sorted_remainder_tiles:
            if sorted_remainder_tiles.index(outline_tile) != 0:
                if prev_outline_tile.j + 1 == outline_tile.j and prev_outline_tile.i == outline_tile.i:
                    this_strip.length += 1
                else:
                    province.outline_strips_vertical.append(this_strip)
                    this_strip = strip_object(outline_tile.i,outline_tile.j,1)
                prev_outline_tile = outline_tile
        province.outline_strips_vertical.append(this_strip)

def populate_surfaces():
    for province in provinces:
        province.generate_surface(Green,Darker_Green)
populate_surfaces()
toggle = False

run = True
Clock = pygame.time.Clock()
milliseconds = []
map_height = len(picture)
map_width = len(picture[0])
while run == True:
    milliseconds.append(Clock.tick())
    if len(milliseconds) > 100:
        milliseconds.pop(0)
    win.fill(Black)
    MouseX, MouseY = pygame.mouse.get_pos()
    MouseLeft, MouseScroll, MouseRight = pygame.mouse.get_pressed()
    Mouse_RelX, Mouse_RelY = pygame.mouse.get_rel()
    keys = pygame.key.get_pressed()

    user_controls()

    #Draw Scene
    pygame.draw.rect(win, Ocean_Blue, (global_x-20*scale,global_y,map_width*scale+20*scale,map_height*scale))
    for province in provinces:
        if toggle:
            province.draw_province(Green)
            province.draw_outline(Darker_Green)
        else:
            province.draw_surface()
    mouse_province = province_mouseover()
    if mouse_province != 0:
        mouse_province.draw_outline(White)
    draw_fps()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 and scale < 8:
                global_x -= int((MouseX-global_x)*(1/scale))
                global_y -= int((MouseY-global_y)*(1/scale))
                scale += 1
                populate_surfaces()
            if event.button == 5 and scale > 2:
                global_x += int((MouseX-global_x)*(1/scale))
                global_y += int((MouseY-global_y)*(1/scale))
                scale -= 1
                populate_surfaces()
            if event.button == 1:
                if mouse_province != 0:
                    mouse_province.centre = tile_object((MouseX-global_x)//scale,(MouseY-global_y)//scale)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                output_metadata()
            if event.key == pygame.K_q:
                toggle = not toggle

    pygame.display.update()
pygame.quit()

#TEXT = font.render("Hello World!", 1, White)
#win.blit(TEXT, (X, Y))















