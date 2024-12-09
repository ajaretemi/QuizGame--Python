import pygame
import json
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

# Fonts
pygame.font.init()
FONT_LARGE = pygame.font.Font(None, 50)
FONT_MEDIUM = pygame.font.Font(None, 36)
FONT_SMALL = pygame.font.Font(None, 28)

# Load question bank
with open("questions.json", "r") as f:
    QUESTIONS = json.load(f)

# Scoring based on difficulty
DIFFICULTY_POINTS = {"Easy": 10, "Medium": 20, "Hard": 30}

# Timer
TIME_LIMIT = 15  # Seconds per question

# High score file
SCORE_FILE = "high_scores.txt"

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quiz Game")
clock = pygame.time.Clock()

def draw_text(text, font, color, x, y, center=False):
    """Draw text on the screen, optionally centering it."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


def draw_text_wrapped(text, font, color, x, y, max_width):
    """Draw text that wraps within a specified width."""
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = " ".join(current_line + [word])
        if font.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]

    lines.append(" ".join(current_line))

    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        screen.blit(line_surface, (x, y + i * font.get_linesize()))


def load_question(question_pool):
    """Randomly select a question from the remaining pool."""
    if question_pool:
        return random.choice(question_pool)
    return None


def save_high_score(score):
    """Save high score to a file."""
    try:
        with open(SCORE_FILE, "a") as f:
            f.write(f"{score}\n")
    except Exception as e:
        print("Error saving high score:", e)


def main():
    """Main game loop."""
    running = True
    question_pool = QUESTIONS.copy()
    question = load_question(question_pool)
    question_start_time = time.time()
    score = 0
    answered = False
    selected_option = None
    time_left = TIME_LIMIT

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                # Check if an answer button is clicked
                for i, option in enumerate(question["options"]):
                    if 150 <= mx <= 650 and 200 + i * 80 <= my <= 250 + i * 80:
                        selected_option = option
                        answered = True

        # Timer calculation
        elapsed_time = time.time() - question_start_time
        time_left = max(0, TIME_LIMIT - int(elapsed_time))

        if time_left == 0 and not answered:
            answered = True

        # Check for end condition: Incorrect answer or timeout
        if answered:
            if selected_option != question["answer"]:  # Incorrect answer
                running = False  # End the game
            elif selected_option == question["answer"]:  # Correct answer
                score += DIFFICULTY_POINTS[question["difficulty"]]

            # Load the next question if available
            question_pool.remove(question)
            question = load_question(question_pool)
            if question:  # Reset for the next question
                question_start_time = time.time()
                answered = False
                selected_option = None
            else:
                running = False  # No more questions

        # Draw question and options
        question_box_y = 50
        pygame.draw.rect(screen, GRAY, (50, question_box_y, 700, 150))
        if question:
            draw_text_wrapped(
                question["question"], FONT_SMALL, BLACK, 60, question_box_y + 10, 680
            )

        for i, option in enumerate(question["options"]):
            color = (
                GREEN
                if answered and option == question["answer"]
                else RED
                if answered and option == selected_option
                else GRAY
            )
            pygame.draw.rect(screen, color, (150, 200 + i * 80, 500, 50))
            draw_text(option, FONT_MEDIUM, BLACK, 400, 225 + i * 80, center=True)

        # Draw timer bar
        pygame.draw.rect(screen, GRAY, (150, 550, 500, 20))
        pygame.draw.rect(screen, BLUE, (150, 550, 500 * (time_left / TIME_LIMIT), 20))

        # Score display
        draw_text(f"Score: {score}", FONT_SMALL, BLACK, 10, 10)

        pygame.display.flip()
        clock.tick(30)

    # Display game over screen
    screen.fill(WHITE)
    draw_text("Game Over!", FONT_LARGE, BLACK, WIDTH // 2, HEIGHT // 3, center=True)
    draw_text(f"Your Score: {score}", FONT_MEDIUM, BLACK, WIDTH // 2, HEIGHT // 2, center=True)
    draw_text("Press any key to exit", FONT_SMALL, BLACK, WIDTH // 2, HEIGHT * 2 // 3, center=True)
    pygame.display.flip()

    # Wait for player to exit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                waiting = False

    save_high_score(score)
    pygame.quit()

if __name__ == "__main__":
    main()
