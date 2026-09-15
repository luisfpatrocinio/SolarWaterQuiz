import pygame
import sys
import json
import os
import webbrowser

# --- CONFIGURAÇÕES INICIAIS ---
pygame.init()
pygame.font.init()

# Informações da tela (Full HD)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Cores (Paleta Neon Maker)
COLOR_BG = "#1E1E2F"          # Fundo escuro/Navy
COLOR_TEXT = "#F8F9FA"        # Branco Puro / Gelo
COLOR_BTN_SOLAR = "#FF9F1C"   # Laranja Vibrante
COLOR_BTN_WATER = "#00B4D8"   # Ciano/Azul Claro
COLOR_CORRECT = "#2ECC71"     # Verde Neon
COLOR_WRONG = "#E74C3C"       # Vermelho Vibrante
COLOR_BTN_OPTION = "#2B2D42"  # Cinza escuro azulado
COLOR_BTN_HOVER = "#4A4D6D"   # Hover padrão para opções

# Inicia a tela sem bordas, mas escalada para preencher a tela atual
is_fullscreen = True
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME | pygame.SCALED)
pygame.display.set_caption("Quiz Maker - Educacional")
clock = pygame.time.Clock()

# --- CARREGAMENTO DE FONTES ---
def get_font(size):
    try:
        return pygame.font.Font("assets/fonte.ttf", size)
    except:
        return pygame.font.SysFont("arial", size, bold=True)

font_title = get_font(90)
font_button = get_font(45)
font_option = get_font(35)
font_credits = get_font(25)

# --- CARREGAMENTO DOS DADOS ---
def load_questions():
    file_path = "perguntas.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao ler perguntas.json: {e}")
    else:
        print("Arquivo perguntas.json não encontrado!")
        
    print("Carregando perguntas de reserva (fallback)...")
    # Fallback caso o arquivo não exista ou esteja corrompido
    return {
        "4ano": [{"pergunta": "Pergunta de teste 4º Ano?", "opcoes": ["A", "B"], "resposta": "A", "curiosidade": "Teste de fallback."}],
        "5ano": [{"pergunta": "Pergunta de teste 5º Ano?", "opcoes": ["A", "B"], "resposta": "B", "curiosidade": "Teste de fallback."}]
    }

QUIZ_DATA = load_questions()

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

is_transitioning = False
fade_alpha = 0
fade_state = 1
next_game_state = None
fade_speed = 15

fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
fade_surface.fill((0, 0, 0))

def change_state(new_state):
    global is_transitioning, fade_alpha, fade_state, next_game_state
    next_game_state = new_state
    is_transitioning = True
    fade_alpha = 0
    fade_state = 1

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
    pygame.draw.rect(screen, color, rect, border_radius=15)
    # Adicionando um leve brilho/borda (Branco)
    pygame.draw.rect(screen, "#FFFFFF", rect, width=3, border_radius=15)
    
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
    global current_state, current_quiz, current_question_index, score, is_correct, is_fullscreen
    global is_transitioning, fade_alpha, fade_state, next_game_state
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        # Tratamento de Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME | pygame.SCALED)
                    else:
                        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
                elif event.key == pygame.K_ESCAPE:
                    if current_state == STATE_MENU:
                        running = False
                    else:
                        current_question_index = 0
                        score = 0
                        change_state(STATE_MENU)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not is_transitioning: # Clique do botão esquerdo
                    mouse_clicked = True
                    
        # Limpar tela
        screen.fill(COLOR_BG)
        
        # Lógica de Renderização por Estado
        if current_state == STATE_MENU:
            draw_text_center("QUIZ MAKER", font_title, COLOR_BTN_SOLAR, 200)
            
            # Checar hover (mouse em cima do botão) e desenhar
            color_4 = "#FFAF40" if btn_4ano_rect.collidepoint(mouse_pos) else COLOR_BTN_SOLAR
            draw_button(btn_4ano_rect, color_4, "4º Ano - Desafio Solar", font_button, COLOR_TEXT)
            
            color_5 = "#33C3F0" if btn_5ano_rect.collidepoint(mouse_pos) else COLOR_BTN_WATER
            draw_button(btn_5ano_rect, color_5, "5º Ano - A Água Invisível", font_button, COLOR_TEXT)
            
            color_sair = COLOR_BTN_HOVER if btn_sair_rect.collidepoint(mouse_pos) else COLOR_BTN_OPTION
            draw_button(btn_sair_rect, color_sair, "Sair", font_button, COLOR_TEXT)
            
            draw_text_center("Criado por PatrocinioLuisF", font_credits, COLOR_TEXT, SCREEN_HEIGHT - 40)
            
            # Lógica de Clique no Menu
            if mouse_clicked:
                if btn_4ano_rect.collidepoint(mouse_pos):
                    current_quiz = "4ano"
                    current_question_index = 0
                    score = 0
                    change_state(STATE_QUESTION)
                elif btn_5ano_rect.collidepoint(mouse_pos):
                    current_quiz = "5ano"
                    current_question_index = 0
                    score = 0
                    change_state(STATE_QUESTION)
                elif btn_sair_rect.collidepoint(mouse_pos):
                    running = False
                    
        elif current_state == STATE_QUESTION:
            question_data = QUIZ_DATA[current_quiz][current_question_index]
            
            # Identidade Visual da Turma
            theme_color = COLOR_BTN_SOLAR if current_quiz == "4ano" else COLOR_BTN_WATER
            next_y = draw_text_wrapped(question_data["pergunta"], font_title, theme_color, 100, SCREEN_WIDTH - 200)
            
            options = question_data["opcoes"]
            num_options = len(options)
            
            # Botões das opções dispostos VERTICALMENTE
            btn_w = 1400
            btn_h = 100
            spacing = 30
            start_y = max(400, next_y + 80)
            
            option_rects = []
            for i, option_text in enumerate(options):
                rect = pygame.Rect((SCREEN_WIDTH - btn_w) // 2, start_y + (btn_h + spacing) * i, btn_w, btn_h)
                option_rects.append((rect, option_text))
                
                # Check hover
                color = COLOR_BTN_HOVER if rect.collidepoint(mouse_pos) else COLOR_BTN_OPTION
                draw_button(rect, color, option_text, font_option, COLOR_TEXT)
                
            draw_text_center(f"Pontuação da Sala: {score}", font_button, COLOR_CORRECT, SCREEN_HEIGHT - 60)
            
            if mouse_clicked:
                for rect, option_text in option_rects:
                    if rect.collidepoint(mouse_pos):
                        if option_text == question_data["resposta"]:
                            score += 1
                            is_correct = True
                        else:
                            is_correct = False
                        change_state(STATE_FEEDBACK)
            
        elif current_state == STATE_FEEDBACK:
            question_data = QUIZ_DATA[current_quiz][current_question_index]
            
            msg = "RESPOSTA CORRETA!" if is_correct else "RESPOSTA INCORRETA!"
            color_msg = COLOR_CORRECT if is_correct else COLOR_WRONG
            
            draw_text_center(msg, font_title, color_msg, 120)
            
            # Mostrar curiosidade
            curiosidade = question_data["curiosidade"]
            next_y = draw_text_wrapped(curiosidade, font_button, COLOR_TEXT, 220, SCREEN_WIDTH - 300)
            
            button_y = max(550, next_y + 60)
            
            # Botão Saiba Mais (Link)
            link = question_data.get("link", "")
            btn_link_rect = None
            if link != "":
                btn_link_rect = pygame.Rect(SCREEN_WIDTH // 2 - 400, button_y, 800, 80)
                color_link = "#8E44AD" if btn_link_rect.collidepoint(mouse_pos) else "#9B59B6"
                draw_button(btn_link_rect, color_link, "[ Assistir Vídeo / Saiba Mais ]", font_button, COLOR_TEXT)
                button_y += 120
            
            # Botão Avançar
            btn_avancar_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, button_y, 400, 100)
            color_avancar = COLOR_BTN_HOVER if btn_avancar_rect.collidepoint(mouse_pos) else COLOR_BTN_OPTION
            draw_button(btn_avancar_rect, color_avancar, "Avançar", font_button, COLOR_TEXT)
            
            if mouse_clicked:
                if btn_avancar_rect.collidepoint(mouse_pos):
                    current_question_index += 1
                    if current_question_index >= len(QUIZ_DATA[current_quiz]):
                        change_state(STATE_END)
                    else:
                        change_state(STATE_QUESTION)
                elif btn_link_rect and btn_link_rect.collidepoint(mouse_pos):
                    webbrowser.open(link)
        
        elif current_state == STATE_END:
            draw_text_center("FIM DE JOGO, TURMA!", font_title, COLOR_BTN_SOLAR, 300)
            
            total_perguntas = len(QUIZ_DATA[current_quiz])
            score_text = f"Vocês acertaram {score} de {total_perguntas} perguntas!"
            draw_text_center(score_text, font_button, COLOR_TEXT, 500)
            
            # Botão Voltar ao Menu
            btn_voltar_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, 750, 600, 120)
            color_voltar = COLOR_BTN_HOVER if btn_voltar_rect.collidepoint(mouse_pos) else COLOR_BTN_OPTION
            draw_button(btn_voltar_rect, color_voltar, "Voltar ao Menu", font_button, COLOR_TEXT)
            
            if mouse_clicked and btn_voltar_rect.collidepoint(mouse_pos):
                current_question_index = 0
                score = 0
                change_state(STATE_MENU)

        # --- Lógica de Transição (Fade) ---
        if is_transitioning:
            fade_alpha += fade_speed * fade_state
            if fade_alpha >= 255:
                fade_alpha = 255
                current_state = next_game_state
                fade_state = -1
            elif fade_alpha <= 0 and fade_state == -1:
                fade_alpha = 0
                is_transitioning = False
            
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))

        # Atualizar Tela
        pygame.display.flip()
        
        # Limite de FPS (60 quadros por segundo)
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
