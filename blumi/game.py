import pygame
import random
from blumi.player import Player, Pipes
from time import sleep
import json

VWLIGHT = '#6091C3'
VWDARK = '#1F2F57'
VWGRAY = '#A8A8A8'
VWWHITE = '#FDFAF9'

class Game:
    """BlumiBird THE GAME, either use main() to execute the game"""
    def __init__(self, bg = "blumi/assets/background.jpg", ground = "blumi/assets/ground.png"):
        """Initialises and sets necessary values"""
        self.screen_width = 720
        self.screen_height = 1280

        self.bg = bg
        self.ground = ground
        self.load_data()
        self.ground_scroll = 0
        self.scroll_speed = 4
        self.bird_gr()

        self.placetop = -400
        self.placebot = 1680
        
        self.chimneybtm_list = []
        self.chimneytop_list = []
        self.chimney_gr()

        pygame.font.init()
        pygame_icon = pygame.image.load('blumi/assets/sprite_0.png')
        pygame.display.set_icon(pygame_icon)
        self.font = pygame.font.SysFont('Comic Sans MS', 40)

        self.score = -1


    def load_data(self):
        self.loadedbg = pygame.image.load(self.bg)
        self.loadedground = pygame.image.load(self.ground)
    
    def bird_gr(self):
        """Creates the bird"""
        self.bird_group = pygame.sprite.Group()
        self.bird = Player(False, 100, int(self.screen_height / 2))
        self.bird_group.add(self.bird)

    def chimney_gr(self):
        """Used to get the chimneys"""
        self.chimney_group = pygame.sprite.Group()
        chimneytop = Pipes(720,self.placetop,1)
        chimneybtm = Pipes(720,self.placebot,-1)
        print(self.placetop)
        print(self.placebot)
        self.get_placement()
        self.chimneytop_list.append(chimneytop)
        self.chimneybtm_list.append(chimneybtm)
        if len(self.chimneytop_list) > 5:
            del self.chimneybtm_list[0]
            del self.chimneytop_list[0]
        self.chimney_group.add(self.chimneybtm_list)
        self.chimney_group.add(self.chimneytop_list)
    
    def get_placement(self):
        """Gets "random" Pipe placements"""
        lotto = random.randint(1, 9)
        print(f"loot = {lotto}")
        if lotto == 1:
            self.placetop = -400
            self.placebot = 1680
        elif lotto == 2:
            self.placetop = -600
            self.placebot = 1480
        
        elif lotto == 3:
            self.placetop = -200
            self.placebot = 1880
        
        elif lotto == 4:
            self.placetop = 0
            self.placebot = 2080
        
        elif lotto == 5:
            self.placetop = -800
            self.placebot = 1280
        
        elif lotto == 6:
            self.placetop = -500
            self.placebot = 1580
        
        elif lotto == 7:
            self.placetop = -100
            self.placebot = 1980
        
        elif lotto == 8:
            self.placetop = -800
            self.placebot = 1280
        elif lotto == 9:
            self.placetop = -700
            self.placebot = 1380
    
    def scoring(self):
        if self.score >= 0:
            self.text_surface = self.font.render(str(self.score), False, (0, 0, 0))
            self.screen.blit(self.text_surface, (self.screen_width/2, 200))
        else:
            self.text_surface = self.font.render('0', False, (0, 0, 0))
            self.screen.blit(self.text_surface, (self.screen_width/2, 200))

    def main_game(self):
        """The Actual game, must be called in the main() function inside the loop"""
        if self.timer >= 120 and self.bird.gameover != True and self.scroll_speed != 0:

            self.chimney_gr()
            self.score += 1
            self.timer = 0

        self.screen.blit(self.loadedbg,(0,0))
        self.screen.blit(self.loadedground, (self.ground_scroll,
        self.screen_height-self.loadedground.get_height()+70))
         
        self.chimney_group.draw(self.screen)
        self.bird_group.draw(self.screen)
        self.scoring()
        
        self.bird_group.update()

        if self.bird.gameover != True:
            
            self.chimney_group.update()

        if pygame.sprite.groupcollide(self.bird_group,self.chimney_group, False, False) or self.bird.rect.center[1] > 1150:
            # print('Game Over')
            self.scroll_speed = 0
            self.bird.gameover = True
        
        if self.bird.gameover == True:
            self.restart_flag = True
        
        self.ground_scroll -= self.scroll_speed

        if abs(self.ground_scroll) > 35:
            self.ground_scroll = 0
        
        self.timer += 1

    def main_menu(self):
        """Makes a main menu, to be called within the main loop"""
        self.screen.blit(self.loadedbg,(0,0))
        self.screen.blit(self.loadedground, (self.ground_scroll,
        self.screen_height-self.loadedground.get_height()+70))

        self.mouse = pygame.mouse.get_pos()
        menutext = self.bigfont.render('BlumiBird', True , VWWHITE)
        self.screen.blit(menutext, (self.screen_width/2-200, self.screen_height/2-300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.screen_width/2-100 <= self.mouse[0] <= self.screen_width/2+100 and self.screen_height/2 <= self.mouse[1] <= self.screen_height/2+40: 
                    self.game_flag = True
                
                if self.screen_width/2-100 <= self.mouse[0] <= self.screen_width/2+100 and self.screen_height/2 +50 <= self.mouse[1] <= self.screen_height/2+90:
                    pygame.quit()
                    self.run = False
        
        if self.screen_width/2-100 <= self.mouse[0] <= self.screen_width/2+100 and self.screen_height/2 <= self.mouse[1] <= self.screen_height/2+40: 
            pygame.draw.rect(self.screen,VWGRAY,[self.screen_width/2-100,self.screen_height/2,200,40])
          
        else: 
            pygame.draw.rect(self.screen,VWDARK,[self.screen_width/2-100,self.screen_height/2,200,40])
        
        if self.screen_width/2-100 <= self.mouse[0] <= self.screen_width/2+100 and self.screen_height/2 +50 <= self.mouse[1] <= self.screen_height/2+90:
            pygame.draw.rect(self.screen,VWGRAY,[self.screen_width/2-100,self.screen_height/2+50,200,40])
        
        else:
            pygame.draw.rect(self.screen,VWDARK,[self.screen_width/2-100,self.screen_height/2+50,200,40])

        self.screen.blit(self.text_start , (self.screen_width/2-35,self.screen_height/2))
        self.screen.blit(self.text_exit , (self.screen_width/2-25, self.screen_height/2+50))

    def restart_btn(self):
        """Creates the Restart button"""
        self.mouse = pygame.mouse.get_pos()
        self.highscore()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.screen_width/2-100 <= self.mouse[0] <= self.screen_width/2+100 and self.screen_height/2 <= self.mouse[1] <= self.screen_height/2+40: 
                    self.restart()
                
                if self.screen_width/2-100 <= self.mouse[0] <= self.screen_width/2+100 and self.screen_height/2 +50 <= self.mouse[1] <= self.screen_height/2+90:
                    pygame.quit()
                    self.run = False

        if self.screen_width/2-100 <= self.mouse[0] <= self.screen_width/2+100 and self.screen_height/2 +50 <= self.mouse[1] <= self.screen_height/2+90:
            pygame.draw.rect(self.screen,VWGRAY,[self.screen_width/2-100,self.screen_height/2+50,200,40])
        
        else:
            pygame.draw.rect(self.screen,VWDARK,[self.screen_width/2-100,self.screen_height/2+50,200,40])
            
        if self.screen_width/2-100 <= self.mouse[0] <= self.screen_width/2+100 and self.screen_height/2 <= self.mouse[1] <= self.screen_height/2+40: 
            pygame.draw.rect(self.screen,VWGRAY,[self.screen_width/2-100,self.screen_height/2,200,40])
          
        else: 
            pygame.draw.rect(self.screen,VWDARK,[self.screen_width/2-100,self.screen_height/2,200,40])

        with open('blumi/highscore.json', 'r') as self.file:
            self.high = self.file.read()

        self.text_highscore = self.smallfont.render('Highscore: ' + self.high , True , VWWHITE)
        self.screen.blit(self.text_highscore, (self.screen_width/2-100, self.screen_height/2+100))

        self.screen.blit(self.text_restart , (self.screen_width/2-50,self.screen_height/2))
        self.screen.blit(self.text_exit , (self.screen_width/2-25, self.screen_height/2+50))

    def restart(self):
        """Supposed to restart the game"""
        print("restart")
        self.load_data()
        self.ground_scroll = 0
        self.scroll_speed = 4
        self.bird_gr()

        self.placetop = -400
        self.placebot = 1680
        
        self.chimneybtm_list = []
        self.chimneytop_list = []
        self.chimney_gr()

        self.chimney_group.draw(self.screen)
        self.bird_group.draw(self.screen)
        self.bird_group.update()

        self.score = -1
        self.timer = 0
        
        self.bird.gameover = False
        self.restart_flag = False

    def highscore(self):
        #read current highscore
        try:
            with open('blumi/highscore.json', 'r') as self.highscore_file:
                self.data = self.highscore_file.read()

            self.current_highscore = json.loads(self.data)
            

        except:
            self.current_highscore = 0

        if self.score >= self.current_highscore:
                with open('blumi/highscore.json', 'w') as self.highscore_file:
                    self.highscore_file.write(str(self.score))
        
    

    def main(self):
        """Main Function"""

        self.init_game()

        while self.run:
            self.game_loop()
        pygame.quit()

    def init_game(self):
        """Used in conjunction with S_mate_Drone, Sets up all the necessary Values for a smooth start"""
        self.game_flag = False
        pygame.init()
        self.screen_width = 720
        self.screen_height = 1280

        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        pygame.display.set_caption('BlumiBird')

        self.smallfont = pygame.font.SysFont('Corbel',35)
        self.bigfont = pygame.font.SysFont('Corbel_Bold', 120)

        self.text_start = self.smallfont.render('Start' , True , VWWHITE)
        self.text_exit = self.smallfont.render('Exit', True, VWWHITE)
        self.text_restart = self.smallfont.render('Restart', True, VWWHITE)
        
        self.timer = 0
        self.restart_flag = False

        pygame.mixer.music.load("blumi/assets/funky town low quality.mp3")
        #https://www.youtube.com/watch?v=poa_QBvtIBA if you want the song ;)
        pygame.mixer.music.play(loops = -1)
        pygame.mixer.music.set_volume(0.05)

        self.run = True
    
    def game_loop(self):
        """must be executed in a loop, displays the actual game"""
        if self.game_flag == False:
            self.main_menu()

        elif self.restart_flag == True:
            self.restart_btn()

        else:
            self.main_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                
        pygame.display.update()
        # self.timer += 1
        pygame.time.Clock().tick(60)

    def close_game(self):
        pygame.display.quit()
        pygame.mixer.quit()


if __name__ == "__main__":
    game = Game()
    game.main()
