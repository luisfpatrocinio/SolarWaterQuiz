import pygame
import sys

# --- CONFIGURAÇÕES INICIAIS ---
pygame.init()
pygame.font.init()

# Informações da tela (Full HD)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Cores (Alto contraste e vibrantes)
COLOR_BG = (30, 30, 50)       # Fundo escuro azulado
COLOR_TEXT = (255, 255, 255)  # Texto branco
COLOR_BTN_4ANO = (255, 150, 50) # Laranja vibrante
COLOR_BTN_5ANO = (50, 150, 255) # Azul vibrante
COLOR_BTN_HOVER = (200, 200, 200)

# Inicia a tela em modo Fullscreen (remova pygame.FULLSCREEN para modo janela, se precisar testar menor)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Quiz Maker - Educacional")
clock = pygame.time.Clock()

# Fontes (Grandes para Datashow)
try:
    font_title = pygame.font.SysFont("arial", 120, bold=True)
    font_button = pygame.font.SysFont("arial", 60, bold=True)
except:
    font_title = pygame.font.Font(None, 120)
    font_button = pygame.font.Font(None, 60)

# --- DADOS DAS PERGUNTAS ---
QUIZ_DATA = {
    "4ano": [
        {
            "pergunta": "Placa solar funciona em dias nublados e com chuva.",
            "opcoes": ["Mito", "Verdade"],
            "resposta": "Verdade",
            "curiosidade": "Gera menos energia, mas a luz que atravessa a nuvem ainda gera eletricidade!"
        },
        {
            "pergunta": "As placas solares duram para sempre.",
            "opcoes": ["Mito", "Verdade"],
            "resposta": "Mito",
            "curiosidade": "Elas duram de 25 a 30 anos, depois precisam ser recicladas."
        },
        {
            "pergunta": "Dá para usar energia solar à noite.",
            "opcoes": ["Mito", "Verdade"],
            "resposta": "Verdade",
            "curiosidade": "Sim! Mas só se você tiver guardado a energia durante o dia em baterias gigantes."
        }
    ],
    "5ano": [
        {
            "pergunta": "Quantos litros de água são gastos para fazer UMA calça jeans?",
            "opcoes": ["100 Litros", "1.000 Litros", "10.000 Litros"],
            "resposta": "10.000 Litros",
            "curiosidade": "A plantação do algodão e as fábricas de tecido consomem muita água!"
        },
        {
            "pergunta": "Quantos litros de água para fazer UM Hambúrguer de carne?",
            "opcoes": ["500 Litros", "2.400 Litros", "10.000 Litros"],
            "resposta": "2.400 Litros",
            "curiosidade": "O boi bebe muita água e come muita grama que precisou ser irrigada."
        },
        {
            "pergunta": "Quantos litros de água para fabricar UM Smartphone?",
            "opcoes": ["10 Litros", "500 Litros", "12.000 Litros"],
            "resposta": "12.000 Litros",
            "curiosidade": "A mineração dos metais preciosos do celular exige rios inteiros de água."
        }
    ]
}

# --- MÁQUINA DE ESTADOS (STATE MACHINE) ---
STATE_MENU = "MENU"
STATE_QUESTION = "QUESTION"
STATE_FEEDBACK = "FEEDBACK"
STATE_END = "END"

# Variáveis de Controle
current_state = STATE_MENU
current_quiz = None
current_question_index = 0
score = 0
is_correct = False

# --- FUNÇÕES DE DESENHO ---
def draw_text_wrapped(text, font, color, y_pos, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        if font.size(' '.join(current_line))[0] > max_width:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    
    y_offset = y_pos
    for line in lines:
        draw_text_center(line, font, color, y_offset)
        y_offset += font.size(line)[1] + 10
    return y_offset

def draw_text_center(text, font, color, y_pos):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
    screen.blit(text_surface, text_rect)

def draw_button(rect, color, text, font, text_color):
    pygame.draw.rect(screen, color, rect, border_radius=20)
    # Adicionando um leve brilho/borda
    pygame.draw.rect(screen, (255, 255, 255), rect, width=4, border_radius=20)
    
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Botões do Menu Principal
btn_width = 800
btn_height = 150
btn_4ano_rect = pygame.Rect(SCREEN_WIDTH // 2 - btn_width // 2, 400, btn_width, btn_height)
btn_5ano_rect = pygame.Rect(SCREEN_WIDTH // 2 - btn_width // 2, 600, btn_width, btn_height)
btn_sair_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 850, 300, 80)

# --- LOOP PRINCIPAL ---
def main():
    global current_state, current_quiz, current_question_index, score, is_correct
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        # Tratamento de Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if current_state == STATE_MENU:
                        running = False
                    else:
                        current_state = STATE_MENU
                        current_question_index = 0
                        score = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Clique do botão esquerdo
                    mouse_clicked = True
                    
        # Limpar tela
        screen.fill(COLOR_BG)
        
        # Lógica de Renderização por Estado
        if current_state == STATE_MENU:
            draw_text_center("QUIZ MAKER", font_title, (255, 220, 50), 200)
            
            # Checar hover (mouse em cima do botão) e desenhar
            color_4 = COLOR_BTN_HOVER if btn_4ano_rect.collidepoint(mouse_pos) else COLOR_BTN_4ANO
            draw_button(btn_4ano_rect, color_4, "4º Ano - Desafio Solar", font_button, COLOR_TEXT)
            
            color_5 = COLOR_BTN_HOVER if btn_5ano_rect.collidepoint(mouse_pos) else COLOR_BTN_5ANO
            draw_button(btn_5ano_rect, color_5, "5º Ano - A Água Invisível", font_button, COLOR_TEXT)
            
            color_sair = COLOR_BTN_HOVER if btn_sair_rect.collidepoint(mouse_pos) else (100, 100, 100)
            draw_button(btn_sair_rect, color_sair, "Sair", font_button, COLOR_TEXT)
            
            # Lógica de Clique no Menu
            if mouse_clicked:
                if btn_4ano_rect.collidepoint(mouse_pos):
                    current_quiz = "4ano"
                    current_question_index = 0
                    score = 0
                    current_state = STATE_QUESTION
                elif btn_5ano_rect.collidepoint(mouse_pos):
                    current_quiz = "5ano"
                    current_question_index = 0
                    score = 0
                    current_state = STATE_QUESTION
                elif btn_sair_rect.collidepoint(mouse_pos):
                    running = False
                    
        elif current_state == STATE_QUESTION:
            question_data = QUIZ_DATA[current_quiz][current_question_index]
            draw_text_wrapped(question_data["pergunta"], font_title, COLOR_TEXT, 200, SCREEN_WIDTH - 200)
            
            options = question_data["opcoes"]
            num_options = len(options)
            
            # Dinamicamente calcular a posição dos botões
            btn_w = 400 if num_options > 2 else 600
            btn_h = 150
            spacing = 50
            total_width = (btn_w * num_options) + (spacing * (num_options - 1))
            start_x = (SCREEN_WIDTH - total_width) // 2
            
            option_rects = []
            for i, option_text in enumerate(options):
                rect = pygame.Rect(start_x + (btn_w + spacing) * i, 600, btn_w, btn_h)
                option_rects.append((rect, option_text))
                
                # Check hover
                color = COLOR_BTN_HOVER if rect.collidepoint(mouse_pos) else (COLOR_BTN_4ANO if current_quiz == "4ano" else COLOR_BTN_5ANO)
                draw_button(rect, color, option_text, font_button, COLOR_TEXT)
                
            draw_text_center(f"Pontuação da Sala: {score}", font_button, (200, 255, 200), SCREEN_HEIGHT - 100)
            
            if mouse_clicked:
                for rect, option_text in option_rects:
                    if rect.collidepoint(mouse_pos):
                        if option_text == question_data["resposta"]:
                            score += 1
                            is_correct = True
                        else:
                            is_correct = False
                        current_state = STATE_FEEDBACK
            
        elif current_state == STATE_FEEDBACK:
            question_data = QUIZ_DATA[current_quiz][current_question_index]
            
            msg = "RESPOSTA CORRETA!" if is_correct else "RESPOSTA INCORRETA!"
            color_msg = (100, 255, 100) if is_correct else (255, 100, 100)
            
            draw_text_center(msg, font_title, color_msg, 200)
            
            # Mostrar curiosidade
            curiosidade = question_data["curiosidade"]
            draw_text_wrapped(curiosidade, font_button, COLOR_TEXT, 400, SCREEN_WIDTH - 300)
            
            # Botão Avançar
            btn_avancar_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 750, 400, 120)
            color_avancar = COLOR_BTN_HOVER if btn_avancar_rect.collidepoint(mouse_pos) else (150, 150, 150)
            draw_button(btn_avancar_rect, color_avancar, "Avançar", font_button, COLOR_TEXT)
            
            if mouse_clicked and btn_avancar_rect.collidepoint(mouse_pos):
                current_question_index += 1
                if current_question_index >= len(QUIZ_DATA[current_quiz]):
                    current_state = STATE_END
                else:
                    current_state = STATE_QUESTION
        
        elif current_state == STATE_END:
            draw_text_center("FIM DE JOGO, TURMA!", font_title, (255, 220, 50), 300)
            
            total_perguntas = len(QUIZ_DATA[current_quiz])
            score_text = f"Vocês acertaram {score} de {total_perguntas} perguntas!"
            draw_text_center(score_text, font_button, COLOR_TEXT, 500)
            
            # Botão Voltar ao Menu
            btn_voltar_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, 750, 600, 120)
            color_voltar = COLOR_BTN_HOVER if btn_voltar_rect.collidepoint(mouse_pos) else (50, 150, 255)
            draw_button(btn_voltar_rect, color_voltar, "Voltar ao Menu", font_button, COLOR_TEXT)
            
            if mouse_clicked and btn_voltar_rect.collidepoint(mouse_pos):
                current_state = STATE_MENU
                current_question_index = 0
                score = 0

        # Atualizar Tela
        pygame.display.flip()
        
        # Limite de FPS (60 quadros por segundo)
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
