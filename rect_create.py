import pygame

class rect_create:
    def __init__(self, surface):
        self.surface = surface
        
    def draw_rect(self,x,y,w,h,color,border):
        rect = pygame.Rect(x,y,w,h)
        pygame.draw.rect(self.surface, color, rect, border)
        return rect

    def create_generate_button(self):
        DARK_GRAY = (127,127,127)
        BLUE_GREEN = (0, 245, 212)
        self.draw_rect(62,482,150,35,DARK_GRAY,0)
        generate_btn = self.draw_rect(60,480,150,35,BLUE_GREEN,0)
        font = pygame.font.Font('SourceSansPro-Regular.otf', 16)
        font.set_bold(True)
        generate_txt = font.render('GENERATE PUZZLE', True, (0, 0, 128))
        self.surface.blit(generate_txt,
                 (generate_btn.x + ((generate_btn.width - font.size('GENERATE PUZZLE')[0])//2),
                  generate_btn.y + ((generate_btn.height - font.size('GENERATE PUZZLE')[1])//2)))
        return generate_btn
