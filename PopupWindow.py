import pygame
import pygame.font

class PopupWindow:
    def __init__(self, screen, title, message, width=300, height=200):
        self.screen = screen
        self.title = title
        self.message = message
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Arial", 16)
        self.close_button_rect = pygame.Rect(self.width - 30, 10, 20, 20)
        self.running = True

    def draw(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((255, 255, 255))

        self.screen.blit(overlay, (self.screen.get_width() // 2 - self.width // 2,
                                  self.screen.get_height() // 2 - self.height // 2))
        
        title_surface = self.font.render(self.title, True, (0, 0, 0))
        self.screen.blit(title_surface, (self.screen.get_width() // 2 - self.width // 2 + 10,
                                         self.screen.get_height() // 2 - self.height // 2 + 10))
        
        message_surface = self.font.render(self.message, True, (0, 0, 0))
        self.screen.blit(message_surface, (self.screen.get_width() // 2 - self.width // 2 + 10,
                                           self.screen.get_height() // 2 - self.height // 2 + 40))

        pygame.draw.rect(self.screen, (255, 0, 0), self.close_button_rect.move(
            self.screen.get_width() // 2 - self.width // 2,
            self.screen.get_height() // 2 - self.height // 2
        ))
        close_text = self.font.render("X", True, (255, 255, 255))
        self.screen.blit(close_text, (self.close_button_rect.x + 5, self.close_button_rect.y + 3))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.close_button_rect.collidepoint(mouse_x, mouse_y):
                    self.running = False

    def show(self):
        while self.running:
            self.handle_events()
            self.draw()
            pygame.time.wait(10)
