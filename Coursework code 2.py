#-----------------IMPORTS-----------------#
import pygame,time,random,operator,time,math
#-----------------VARIABLES-----------------#
done = False
screen_width = 960
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pressed = pygame.key.get_pressed()
green = (91, 188, 26)
yellow = (250, 240, 48)
white = (255,255,255)
orange = (255, 114, 0)
gold = (255, 250, 0)
grey = (152, 161, 173)
light_grey = (200, 200, 200)
red = (255, 0, 0)
dark_blue = (61,133,198)
blue = 111,168,220
light_blue = (160,217,255)
black = (0,0,0)
buttons = []
textboxes = []
edges = []
nodes = []
maze_width = 0
maze_height = 0
path = []
added_nodes = []
confirmed_edges = []
search_edges = []
searched_nodes = []
clicked_nodes = []
reached_nodes = []
count = 0
click = False
hidesolution = False
generate = 'none'
maze_walls = pygame.sprite.Group()
#-----------------CLASSES-----------------#
class button():
    #initialises itself and sets all the arguments that it is given to parameters
    def __init__ (self,screen, colour, x, y, width,height, label,outline_colour,font_size,font_colour):
        self.screen = screen
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.outline_colour = outline_colour
        self.font_size = font_size
        self.original_colour = colour
        self.font_colour = font_colour
    def draw(self):
        #this method draws the button and the label on it
        pygame.draw.rect(self.screen, self.outline_colour,(self.x,self.y, self.width, self.height))
        pygame.draw.rect(self.screen, self.colour,(self.x+1,self.y+1, self.width-2, self.height-2))
        font = pygame.font.SysFont('agency fb',self.font_size,True,False)
        text = font.render(self.label, True, self.font_colour)
        text_rect = text.get_rect(center=(self.x+self.width/2,self.y+self.height/2))
        screen.blit(text, text_rect)
    def clicked(self):
        #gets all the global variables that are needed in this method
        global edges,nodes,textboxes,buttons,mst_edges,maze_width,maze_height,path,paths,neighbours,nodes,generate,search_edges,added_nodes,confirmed_edges,maze_walls,searched_nodes,toggle1,toggle2,clicked_nodes,path,hidesolution,reached_nodes
        #gets the x,y co-ords of the mouse
        pos = pygame.mouse.get_pos()
        mx = pos[0]
        my = pos[1]
        #this statement checks if the mouse is in the area of the button
        if my<self.y+self.height and my>self.y and mx< self.x+self.width and mx>self.x and b.colour != grey:
            self.colour = int(self.colour[0]*0.8),int(self.colour[1]*0.8),int(self.colour[2]*0.8)
            #these statements make a change to the width/height displays based on the button clicked
            if self.label == '+' and self == buttons[1] and int(textboxes[0].word)<100:
                textboxes[0].word = str(int(textboxes[0].word) + 5)
            elif self.label == '+' and self == buttons[3] and int(textboxes[1].word)<100:
                textboxes[1].word = str(int(textboxes[1].word) + 5)
            elif self.label == '-' and self == buttons[0] and int(textboxes[0].word)>5:
                textboxes[0].word = str(int(textboxes[0].word) - 5)
            elif self.label == '-' and self == buttons[2] and int(textboxes[1].word)>5:
                textboxes[1].word = str(int(textboxes[1].word) - 5)
            #if generate maze is selected it resets all the variables, builds up a new grid of edges and nodes and starts the maze generation off
            elif self.label == 'GENERATE MAZE':
                if toggle1.selected != '':
                    added_nodes,confirmed_edges,maze_walls,edges,search_edges,nodes,path,searched_nodes,clicked_nodes = reset()
                    nodes = new_nodes(int(textboxes[0].word),int(textboxes[1].word))
                    search_edges,edges = edge_filler(nodes)
                    added_nodes,confirmed_edges,search_edges = kruskal_main(added_nodes,confirmed_edges,search_edges)
                    maze_width,maze_height = int(textboxes[0].word),int(textboxes[1].word)
                    generate = 'maze'
                #if all in one is selected if generates the whole thing at once, if not it will run one iteration of the algorithm each time it goes through the game loop
                if toggle1.selected == 'ALL IN ONE':
                    while len(added_nodes) < len(nodes):
                        added_nodes,confirmed_edges,search_edges,maze_walls = kruskals_loop(search_edges, nodes,added_nodes,confirmed_edges,maze_walls)
                            
            elif self.label == 'SOLVE MAZE':
                if toggle2.selected != '':
                    paths,neighbours = dijkstras_main(confirmed_edges,nodes,nodes[0],nodes[-1])
                    if toggle2.selected == 'ALL IN ONE':
                        while paths[nodes[-1].name][0] == float('inf'):
                            paths,searched_nodes = dijkstras_loop(confirmed_edges,nodes,nodes[0],nodes[-1],paths,neighbours,searched_nodes,generate)
                        path,reached_nodes = dijkstras_list(paths,nodes[0],nodes[-1],nodes)
                    else:
                        generate = 'solution'
            elif self.label == 'LOAD MAZE':
                #resets all variables and then calls the load maze function which updates the returned variables to make a maze
                added_nodes,confirmed_edges,maze_walls,edges,search_edges,nodes,path,searched_nodes,clicked_nodes = reset()
                maze_walls,maze_width,maze_height,path,searched_nodes,nodes,reached_nodes = load_maze("maze1.txt",maze_walls,path,searched_nodes,reached_nodes)
            elif self.label == 'SAVE MAZE':
                #runs the save maze proceedure which just stores the data about the currnet maze into a file to be loaded
                save_maze(maze_walls,maze_width,maze_height,path,searched_nodes,reached_nodes)
            elif self.label == 'HIDE PATH':
                if hidesolution == False:
                    hidesolution = True
                else:
                    hidesolution = False
            #returns true if that button was clicked which stops the program to stop looking through the buttons list
            return True
        
#toggle is a subclass of button         
class toggle(button):
    #initialises itself through the button class and defines the variables it needs with the arguments give on top of the 
    def __init__ (self,screen, colour, x, y, width,height, label,label2,outline_colour,font_size,font_colour):
        button.__init__(self,screen, colour, x, y, width,height,label,outline_colour,font_size,font_colour)
        self.original_colour = colour
        self.label1 = label
        self.label2 = label2
        self.outline_colour1 = outline_colour
        self.outline_colour2 = outline_colour
        self.font_size = font_size
        #selected will be the value that stores the selction of the toggle
        self.selected = ''
    def draw(self):
        #draws in much the same way as the button class but draws two seperate shapes
        pygame.draw.rect(self.screen, self.outline_colour1,(self.x,self.y, self.width*2/5, self.height))
        pygame.draw.rect(self.screen, self.colour1,(self.x+1,self.y+1, (self.width*2/5)-2, self.height-2))
        pygame.draw.rect(self.screen, self.outline_colour2,((self.x+self.width*3/5),self.y, self.width*2/5, self.height))
        pygame.draw.rect(self.screen, self.colour2,((self.x+self.width*3/5)+1,self.y+1, (self.width*2/5)-2, self.height-2))
        font = pygame.font.SysFont('comic sans',self.font_size,True,False)
        text = font.render(self.label1, True, white)
        text_rect = text.get_rect(center=(self.x+self.width*1/5,self.y+self.height/2))
        screen.blit(text, text_rect)
        text2 = font.render(self.label2, True, white)
        text_rect2 = text2.get_rect(center=(self.x+self.width*4/5,self.y+self.height/2))
        screen.blit(text2, text_rect2)
    def clicked(self):
        #changes the value of selected and the colours of each toggle if they have been clicked
        pos = pygame.mouse.get_pos()
        mx = pos[0]
        my = pos[1]
        if my<self.y+self.height and my>self.y and mx< self.x+(self.width*2/5 ) and mx>self.x:
            self.colour2 = grey
            self.colour1 = self.original_colour
            self.selected = self.label1
        elif my<self.y+self.height and my>self.y and mx< self.x+self.width and mx>self.x+(self.width*3/5):
            self.colour2 = self.original_colour
            self.colour1 = grey
            self.selected = self.label2
            
class textbox():
    def __init__ (self,screen, x, y, word,fontsize,colour):
        self.screen = screen
        self.x = x
        self.y = y
        self.word = word
        self.fontsize = fontsize
        self.colour = colour
    def draw(self):
        font = pygame.font.SysFont('agency fb',self.fontsize,True,False)
        text = font.render(self.word, True, self.colour)
        text_rect = text.get_rect(center=(self.x,self.y))
        screen.blit(text, text_rect)
 
class edge(pygame.sprite.Sprite):
    #class counter is a variable used to assign each new object a unique name by incrementing by 1 for each new object
    def __init__ (self,start,end):
        class_counter = 0
        pygame.sprite.Sprite.__init__(self)
        self.length = 1
        class_counter += 1
        self.name = class_counter
        self.in_maze = True
        self.start = start
        self.end = end
        #the start_pos and end_pos variables act as coordinatines for the edge ends
    def draw(self,x_len,y_len,colour,wall):
        if wall == True:
            pygame.draw.line(screen,colour,((255+((self.start[0]+0.5)*(screen_width-255)/x_len)),(((self.start[1]-0.5)*(screen_height)/y_len))),((255+((self.end[0]-0.5)*(screen_width-255)/x_len)),((self.end[1]+0.5)*(screen_height)/y_len)),1)
        elif wall == False:
            pygame.draw.line(screen,colour,((255+((self.start[0])*(screen_width-255)/x_len)),(((self.start[1])*(screen_height)/y_len))),((255+((self.end[0])*(screen_width-255)/x_len)),(((self.end[1])*(screen_height)/y_len))),1)
 
class node(pygame.sprite.Sprite):
    def __init__ (self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #the x an y attributes act as coordinates for the nodes
        self.x = x
        self.y = y
        self.name= (self.x,self.y)
    def draw(self,x_len,y_len,colour):
        pygame.draw.rect(screen,colour,((255+((self.x-0.5)*(screen_width-255)/x_len),((self.y-0.5)*(screen_height)/y_len),(((screen_width-255)/x_len))+1,(screen_height/y_len)+1)))
    def clicked(self,clicked_nodes,x_len,y_len):
        #this class allows each node to act like a button that changes colour when clicked
        pos = pygame.mouse.get_pos()
        mx = pos[0]
        my = pos[1]
        #uses the dimensions of the node along with its co ords to check for clicks within it
        if my<((self.y-0.5)*(screen_height)/y_len)+(screen_height/y_len)+1 and my>((self.y-0.5)*(screen_height)/y_len) and mx< 255+((self.x-0.5)*(screen_width-255)/x_len)+(((screen_width-255)/x_len))+1 and mx>255+((self.x-0.5)*(screen_width-255)/x_len):
                if self not in clicked_nodes:
                    clicked_nodes.append(self)
        return clicked_nodes
#-----------------FUNCTIONS-----------------#
def new_nodes(node_x,node_y):
    nodes = []
    for x in range(0,node_x):
        for y in range(0,node_y):
            nodes.append(node(x+0.5,y+0.5))
    return nodes
 
def edge_filler(nodes):
    edges = []
    for n in nodes:
        for n2 in nodes:
            if n.x+1 == n2.x and n.y==n2.y:
                edges.append(edge((n.x,n.y),(n2.x,n2.y)))
            elif n.x == n2.x and n.y==n2.y+1:
                edges.append(edge((n.x,n.y),(n2.x,n2.y)))
    return edges,edges
 
def reset():
    #this function resets all the variables which avoids any incorrect things to get drawn
    nodes = []
    added_nodes =[]
    confirmed_edges = []
    maze_walls = pygame.sprite.Group()
    edges = []
    search_edges = []
    path = []
    searched_nodes = []
    clicked_nodes = []
    return added_nodes,confirmed_edges,maze_walls,edges,search_edges,nodes,path,searched_nodes,clicked_nodes
 
def kruskal_shortest_edges(edges,shortest_length):
    #makes a list of the joint shortest edges
    shortest_edges = []
    for edge in edges:
        if edge.length == shortest_length:
            shortest_edges.append(edge)
    return shortest_edges
 
def kruskal_main(added_nodes,confirmed_edges,search_edges):
    #random starting edge is selected from a list of the shortest edges in the graph
    start_edge = search_edges[random.randint(0,len(search_edges)-1)]
    search_edges.remove(start_edge)
    #add the start edge to the solution
    confirmed_edges.append(start_edge)
    added_nodes.append(start_edge.start)
    added_nodes.append(start_edge.end)
    #this loop will not break untill all nodes are included in the solution
    return added_nodes,confirmed_edges,search_edges
 
def kruskals_loop(search_edges, nodes,added_nodes,confirmed_edges,maze_walls):
    #creates a list of the shortest edges and chooses one at random
    random_shortest_edge = search_edges[random.randint(0,len(search_edges)-1)]
    while random_shortest_edge.end not in added_nodes and random_shortest_edge.start not in added_nodes:
        random_shortest_edge = search_edges[random.randint(0,len(search_edges)-1)]
    if random_shortest_edge.end in added_nodes or random_shortest_edge.start in added_nodes:
        cycle = False
        #checks if the random edge joins to any nodes not currently in the solution
        if random_shortest_edge.end in added_nodes and random_shortest_edge.start in added_nodes:
            cycle = True
        #if there is no cycle the new nose gets added to added_nodes and the edge gets removed
        if cycle == False:
            confirmed_edges.append(random_shortest_edge)
            if random_shortest_edge.start not in added_nodes:
                added_nodes.append(random_shortest_edge.start)
            if random_shortest_edge.end not in added_nodes:
                added_nodes.append(random_shortest_edge.end)
        else:
            maze_walls.add(random_shortest_edge)
        #removes the edge after this as it is either alreadly in the current solution or not suitable
        search_edges.remove(random_shortest_edge)
    return (added_nodes,confirmed_edges,search_edges,maze_walls)
 
def paths_dijkstra (nodes,start_node):
    paths = {}
    for node in nodes:
        #for each node createsa dictionary item that stores distance and the node before it
        paths[node.name] = [float('inf'),'',False]
        if node.name == start_node.name:
            paths[node.name] = [0,'A',False]
    return paths
 
def neighbours_dijkstra (nodes,edges):
    neighbours = {}
    for node in nodes:
        temp = []
        #loops thorough each edge and node and builds a list of nodes and their connected edges
        for edge in edges:
            if edge.start == node.name:
                temp.append(edge.end)
            elif edge.end == node.name:
                temp.append(edge.start)
        neighbours[node.name] = temp
    return neighbours
 
def dijkstras_loop(edges,nodes,start_node,end_node,paths,neighbours,searched_nodes,generate):
    lowest_path = float('inf')
    #the search node variable holds the node that is next to be searched by the algorithm
    searched_node = ()
    #this checks through the current paths to find the next search node based on the current shortest path
    for path in paths:
        if paths[path][0] < lowest_path and paths[path][2] == False:
            lowest_path = paths[path][0]
            searched_node = path
    #when there is no current shortest path the start node is used as this is the first iteration of the algorithm
    connections = neighbours[searched_node]
    for connection in connections:
        for edge in edges:
            #this will update the min path weight of a node if the newly discovered path is shorter
            if edge.start == connection and edge.end == searched_node or edge.end == connection and edge.start == searched_node:
                if edge.length + paths[searched_node][0] < paths[connection][0]:
                    #adds on the length of the path to the search node to the length of the connecting edge to get the new path distance for that node
                    paths[connection][0] = edge.length + paths[searched_node][0]
                    paths[connection][1] =  searched_node
    #when a node gets searched this boolean value is flipped to true
    paths[searched_node][2] = True
    searched_nodes.append(searched_node)
 
 
    return paths,searched_nodes
 
def dijkstras_list(paths,start_node,end_node,nodes):
    #creates a list of the nodes along the path by using the shortest path to the end node node in reverse
    final_path = [end_node]
    #loop continues until the start node is reached
    while final_path[-1] != start_node:
        #adds in the node that leads to the node we just added into the list
        for node in nodes:
            if node.name == paths[final_path[-1].name][1]:
                final_path.append(node)
 
            if paths[node.name][0] <float('inf') and paths[node.name][2] == False:
                reached_nodes.append(node)
 
    #flips the output value so that it goes from start to end
    return final_path[::-1],reached_nodes
 
def dijkstras_main(edges,nodes,start_node,end_node):
    #this function calls all the individual dijskatras funtions itself so you dont have to call them all yourself
    search_nodes = []
    paths = paths_dijkstra (nodes,start_node)
    neighbours = neighbours_dijkstra (nodes,edges)
    return paths,neighbours
 
def load_maze(filename,maze_walls,path,searched_nodes,reached_nodes):
    #opens the file and stores all the data in the lines variable
    f = open(filename,"r")
    lines = f.readlines()
    f.close()
    #line one holds the dimensions of the saved maze
    line1 = lines[0]
    lines = lines[1:]
    for line in lines:
        #checks each line to see where each line need to be saved
        line = line.replace('\'','')
        #stores lines with special letters at the end into their corresponding lists
        if line[-2] == 'p' or line[-2] == 's' or line[-2]== 'n' or line[-2] == 'r':
            x,y = line.split(',')
            y = y.replace('p','')
            y = y.replace('s','')
            y = y.replace('n','')
            y = y.replace('r','')
            #a new node is made with the stored co ords and stored into the temp file
            temp = node(float(x),float(y))            
            if line[-2] == 'p':
                path.append(temp)
            if line[-2] == 'r':
                reached_nodes.append(temp)
            if line[-2] == 'p' or line[-2] == 's' or line[-2] == 'r':              
                searched_nodes.append((float(x),float(y)))
            nodes.append(temp)
        else:
            #every line without a letter corresponds to a maze wall, these are all added to the maze wall lists after being re made into edges
            line = line.split(',')
            maze_walls.add(edge((float(line[0]),float(line[1])),(float(line[2]),float(line[3]))))
    #extrats the maze dimensions from text form
    temp = line1.split('x')
    maze_width,maze_height = int(temp[0]),int(temp[1])

    return maze_walls,maze_width,maze_height,path,searched_nodes,nodes,reached_nodes
 
def save_maze(maze_walls,maze_x,maze_y,path,searched_nodes,reached_nodes):
    #opens text file
    open('maze1.txt', 'w').close()
    writefile=open("maze1.txt","a")
    writefile.write(str(maze_y) + "x"+str(maze_y)+'\n')
    #for every node a new line is added to store its co ordinates this will allow the node system and path to be re built
    for n in nodes:
        if n in path:
            writefile.write(str(n.name)[1:-1]+'p'+'\n')
        elif n in reached_nodes:
            writefile.write(str(n.name)[1:-1]+'r'+'\n')            
        elif n.name in searched_nodes:
            writefile.write(str(n.name)[1:-1]+'s'+'\n')
        else:
            writefile.write(str(n.name)[1:-1]+'n'+'\n')
    #every edge stored in the maze walls list that forms the walls of the maze is added in to the end of the file
    for wall in maze_walls:
        writefile.write(str(wall.start)[1:-1] + "," + str(wall.end)[1:-1]+'\n')
    writefile.close()
#----------------------------------#
buttons.append(button(screen,blue,20,180,35,35,'-',white,40,white))
buttons.append(button(screen,blue,195,180,35,35,'+',white,40,white))
textboxes.append(textbox(screen,123,200,'20',35,white))
buttons.append(button(screen,blue,20,265,35,35,'-',white,40,white))
buttons.append(button(screen,blue,195,265,35,35,'+',white,40,white))
textboxes.append(textbox(screen,123,285,'20',35,white))
textboxes.append(textbox(screen,123,60,generate,24,black))
textboxes.append(textbox(screen,123,160,'WIDTH',25,white))
textboxes.append(textbox(screen,123,245,'HEIGHT',25,white))
buttons.append(button(screen,blue,25,335,200,50,'GENERATE MAZE',white,25,white))
buttons.append(button(screen,blue,25,465,200,50,'SOLVE MAZE',white,25,white))
buttons.append(button(screen,blue,15,625,60,50,'SAVE MAZE',white,13,white))
buttons.append(button(screen,blue,95,625,60,50,'LOAD MAZE',white,13,white))
buttons.append(button(screen,blue,175,625,60,50,'HIDE PATH',white,13,white))
toggle1 = toggle(screen,blue,25,405,200,35,'STEP BY STEP','ALL IN ONE',white,14,white)
toggle1.colour1 = grey
toggle1.colour2 = grey
toggle2 = toggle(screen,blue,25,535,200,35,'STEP BY STEP','ALL IN ONE',white,14,white)
toggle2.colour1 = grey
toggle2.colour2 = grey
pygame.init()
screen.fill(white)
#-----------------GAME LOOP-----------------#
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                        done = True
        #-----------------EVENT MANAGEMENT-----------------#
        if event.type == pygame.MOUSEBUTTONUP:
            for b in buttons:
                b.colour = b.original_colour
            click = False
        #checks if the mouse is clicked down on the pygame window 
        if event.type == pygame.MOUSEBUTTONDOWN:
            #if the maze has not started to be solved then all the nodes are able to be highlighted to form the predicted path
            if generate == 'none' and (len(nodes)>0 and len(path)==0):
                click = True
            elif generate == 'none' and hidesolution==True:
                click = True
            toggle1.clicked()
            toggle2.clicked()
 
            for b in buttons:
                if b.clicked() == True:
                    break
 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                clicked_nodes = clicked_nodes[:-1]
 
 
    #-----------------GAME LOGIC-----------------#
    count+=1
    if click == True:
        for n in nodes:
            clicked_nodes = n.clicked(clicked_nodes,maze_width,maze_height)
 
 
    #-----------------DRAWING TO SCREEN-----------------#
    pygame.draw.rect(screen,light_blue,(0,0,250,screen_height))
    pygame.draw.rect(screen,white,(250,0,screen_width,screen_height))
    pygame.draw.rect(screen,white,(2,2,246,116))
 
    if generate == 'maze':
        textboxes[2].word = count%4*' '+'creating maze'+count%4*'.'
        if len(added_nodes)<len(nodes):
            pygame.draw.rect(screen,white,(250,0,screen_width,screen_height))
            added_nodes,confirmed_edges,search_edges,maze_walls = kruskals_loop(search_edges, nodes,added_nodes,confirmed_edges,maze_walls)
            for e in confirmed_edges:
                e.draw(maze_width,maze_height,black,False)
        elif len(added_nodes) == len(nodes):
            generate = 'none'
            maze_walls.add(search_edges)
 
    elif generate == 'solution':
        textboxes[2].word = (1+count%4)*' '+'solving maze'+count%4*'.'
        if paths[nodes[-1].name][0] == float('inf'):
            paths,searched_nodes = dijkstras_loop(confirmed_edges,nodes,nodes[0],nodes[-1],paths,neighbours,searched_nodes,generate)
        else:
            generate = 'none'
            path,reached_nodes = dijkstras_list(paths,nodes[0],nodes[-1],nodes)
            
        if hidesolution == False: 
            for n in nodes:
                if n.name in searched_nodes:
                    n.draw(maze_width,maze_height,grey)
                elif paths[n.name][0] <float('inf') and paths[n.name][2] == False:
                    n.draw(maze_width,maze_height,light_grey)
     
            for e in maze_walls:
                e.draw(maze_width,maze_height,black,True)
            for c in clicked_nodes:
                c.draw(maze_width,maze_height,dark_blue)           

 
    elif generate == 'none':
        textboxes[2].word = 'idle'
        if hidesolution == False:
            for n in nodes:
                if n.name in searched_nodes:
                    n.draw(maze_width,maze_height,grey)
                if n in reached_nodes:
                    n.draw(maze_width,maze_height,light_grey)

            #changes the colour argument for each node in ppath depending on its position in the path list.
            #this gives a gradient effect
            for p in path:
                colour = int((path.index(p)/len(path))*255)
                p.draw(maze_width,maze_height,(colour,0,255-colour))
            #correct num stored the number of node that have been highlighted and selected in the computers path
            correct_num = 0
            for c in clicked_nodes:
                if c in path:
                    correct_num +=1
                    c.draw(maze_width,maze_height,green)
                else:
                    c.draw(maze_width,maze_height,dark_blue)
            #adds the percentage of nodes in the path that were highlighted to the console
            if len(clicked_nodes)>0 and len(path) >0 :
                textboxes[2].word = str(round((correct_num/len(path))*100))+'% of correct path found'
        else:
            for c in clicked_nodes:
                c.draw(maze_width,maze_height,dark_blue)
        for e in maze_walls:
            e.draw(maze_width,maze_height,black,True)
        
    for b in buttons:
        if (b.label == 'SOLVE MAZE' and (len(maze_walls) == 0 or len(path)> 0 or generate == 'maze' or toggle2.selected == '')) or (b.label == 'GENERATE MAZE' and toggle1.selected == '') or (b.label == 'SAVE MAZE' and path == []):
            b.colour = grey
        b.draw()
 
 
 
    for t in textboxes:
        t.draw()
    toggle1.draw()
    toggle2.draw()
    #----------------------------------#
    pygame.display.flip()
    clock.tick()
pygame.quit()
