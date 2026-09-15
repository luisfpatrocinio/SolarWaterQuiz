# Quiz Maker - Educacional

## 📖 Sobre o Projeto

O **Quiz Maker - Educacional** é um jogo de perguntas e respostas interativo desenvolvido em Python utilizando a biblioteca **Pygame**. O projeto foi criado com o objetivo de ensinar conceitos importantes sobre sustentabilidade, meio ambiente e ciências de forma divertida e engajadora para alunos do Ensino Fundamental (4º e 5º anos).

O jogo apresenta uma interface moderna com "Paleta Neon Maker", suporte a tela cheia e transições suaves entre as telas.

## 🚀 Funcionalidades

- **Múltiplos Temas (Turmas):**
  - **4º Ano - Desafio Solar:** Perguntas focadas em energia solar, mitos e verdades, e curiosidades sobre o sol.
  - **5º Ano - A Água Invisível:** Perguntas focadas no consumo de água (pegada hídrica), tecnologias de irrigação e preservação.
- **Sistema de Feedback Rico:** Após responder cada pergunta, o jogador recebe um feedback imediato (Correto/Incorreto) e uma **curiosidade** que explica o contexto da resposta.
- **Links de Aprofundamento:** Algumas respostas fornecem links externos (como vídeos no YouTube) para que os alunos possam aprender mais sobre o assunto.
- **Pontuação da Sala:** O jogo rastreia a pontuação coletiva da turma ao longo das perguntas.
- **Design Responsivo e Moderno:** Interface projetada para Full HD (1920x1080) com botões interativos (efeitos de hover) e cores vibrantes.
- **Máquina de Estados:** A arquitetura do jogo é baseada em uma máquina de estados (State Machine) para transições fluidas entre Menu, Pergunta, Feedback e Fim de Jogo.
- **Fallback de Dados:** Caso o arquivo de perguntas apresente problemas, o jogo carrega perguntas de reserva automaticamente para não interromper a experiência.

## 🛠️ Tecnologias Utilizadas

- **[Python 3](https://www.python.org/):** Linguagem de programação principal.
- **[Pygame](https://www.pygame.org/):** Biblioteca utilizada para renderização gráfica, controle de eventos (teclado/mouse) e lógica do jogo.
- **JSON:** Utilizado para armazenar as perguntas, respostas, curiosidades e links de forma estruturada e facilmente editável (`perguntas.json`).

## 📂 Estrutura do Projeto

- `main.py`: Arquivo principal contendo a lógica do jogo, renderização da interface e controle da máquina de estados.
- `perguntas.json`: Banco de dados das perguntas do quiz, separado por turmas ("4ano" e "5ano").
- `assets/fonte.ttf`: Fonte customizada utilizada no jogo (opcional, o jogo possui fallback para fonte do sistema).
- `.gitignore`: Arquivo para ignorar arquivos desnecessários no controle de versão.

## 🎮 Como Jogar

1. **Pré-requisitos:** Certifique-se de ter o Python e a biblioteca Pygame instalados.
   ```bash
   pip install pygame
   ```
2. **Executar o Jogo:**
   No terminal, navegue até a pasta do projeto e execute:
   ```bash
   python main.py
   ```
3. **Controles:**
   - **Mouse:** Clique com o botão esquerdo para selecionar as opções.
   - **F11:** Alternar entre modo de Janela e Tela Cheia.
   - **ESC:** Voltar ao Menu Principal ou Sair do jogo.

## 🧠 Arquitetura do Código (Detalhes Técnicos)

O jogo no arquivo `main.py` foi estruturado de forma modular e organizada:
- **Configurações:** Definição de constantes de cores (ex: `COLOR_BG`, `COLOR_BTN_SOLAR`), resoluções e estado inicial da janela.
- **Carregamento de Dados (`load_questions`):** Função robusta que lê o arquivo `perguntas.json` e possui tratamento de erros com dados de "fallback".
- **Máquina de Estados:** Variáveis como `current_state` gerenciam o fluxo do jogo:
  - `STATE_MENU`: Tela inicial de seleção de turmas.
  - `STATE_QUESTION`: Tela onde a pergunta e as opções são exibidas.
  - `STATE_FEEDBACK`: Tela que mostra se a resposta estava correta, exibe a curiosidade e o link extra.
  - `STATE_END`: Tela final com a pontuação total da turma.
- **Funções de Desenho:** Helpers como `draw_text_wrapped` e `draw_button` simplificam a renderização de elementos na tela e tratam quebra de linha de textos longos.
- **Transições (`is_transitioning`, `fade_alpha`):** Efeitos de "fade in/out" usando uma superfície preta com transparência para suavizar a mudança de telas.

## 👨‍💻 Autor
Criado por **PatrocinioLuisF**.
