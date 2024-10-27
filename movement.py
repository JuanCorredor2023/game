import random

class MovementFunctions:
    @staticmethod
    def move_to(target_x, target_y, current_x, current_y, speed):
        # Calculate the direction to move in
        delta_x = target_x - current_x
        delta_y = target_y - current_y
        
        # Normalize the direction and scale by speed
        distance = (delta_x**2 + delta_y**2) ** 0.5
        if distance > speed:  # Only move if the distance is greater than the speed
            current_x += speed * (delta_x / distance)
            current_y += speed * (delta_y / distance)
        
        return current_x, current_y

    @staticmethod
    def random_move(current_x, current_y, screen_width, screen_height, speed):
        # Increase randomness: new random target every few frames, and larger distances
        target_x = random.randint(0, screen_width)
        target_y = random.randint(0, screen_height)

        # Add variation to the speed to make movements faster sometimes
        speed = random.randint(1, speed * 2)  # Randomize the speed for more varied movements

        # Move towards the random target using the move_to function
        return MovementFunctions.move_to(target_x, target_y, current_x, current_y, speed)