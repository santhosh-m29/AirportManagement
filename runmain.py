import pygame
import cv2
import os

def play_video(video_path):
    if not os.path.exists(video_path):
        print(f"Video file not found at: {video_path}")
        print("Skipping intro video...")
        return

    pygame.init()
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        pygame.quit()
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30 # Fallback FPS

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Initialize Pygame screen
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Intro Video")
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Allow user to skip video by pressing Escape or Enter
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    running = False
                    
        if not running:
            break

        ret, frame = cap.read()
        if not ret:
            break # End of video
            
        # Convert BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # OpenCV image is (H, W, C). Pygame surface expects (W, H, C)
        frame = frame.swapaxes(0, 1)
        
        # Create pygame surface from numpy array
        surface = pygame.surfarray.make_surface(frame)
        
        screen.blit(surface, (0, 0))
        pygame.display.flip()
        clock.tick(fps)
        
    # Clean up
    cap.release()
    pygame.display.quit()
    pygame.quit()

if __name__ == "__main__":
    play_video('./assets/finalappintro.mp4')
    # After the video has finished playing (or if skipped/missing), run main.py
    import main
