import cv2
import numpy as np

# Path to the video file
video_path = "D:\\vid.mp4"

# Initialize video capture
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Open Error")
    exit()

# grid size (100 x 100)
grid_size = 50  # Change this to control the occupancy grid size
thresh = []

while cap.isOpened():
    # Capture each frame
    ret, frame = cap.read()
    if not ret:
        print("End of video reached or failed to read frame.")
        break

    # the image is resized
    frame = cv2.resize(frame, (800, 600))

    # the image is converted to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # the video provided also contains small black spots(dust or leftover tape) which create noises when detecting black line
    # image is blurred with Gaussian Blur, we do this to smoothen these small black spots
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Binary Thresholding (invert to make the black line white)
    _, binary = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY_INV)
    
    # This is the threshold value. Any pixels in `blurred` with intensity values above 70 will be set to
    # white (255), and those below 70 will be set to black (0).

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # RETR_EXTERNAL: Finds only the outermost contours 
    # this returns arrays of points of the boundarys of the countours

    # Visually representing the contours (boundary)
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
    # Here we draw the contours on the frame
    #-1 means all contours draw, (0,255,0) is colour of line, 2 is the thickness of line

    # We assume that the contour of the black line would always be the maximum in the image
    # So, here we find the largest contour
    if contours:
        largest_contour = max(contours, key=cv2.contourArea) # contourArea calculates the area of the given contour

        # Create a mask for the largest contour
        mask = np.zeros_like(binary)  # This creates a blank image with all pixel values 0
        cv2.drawContours(mask, [largest_contour], -1, 255, thickness=cv2.FILLED)

        # Apply the mask to keep only the largest contour in the binary image
        binary = cv2.bitwise_and(binary, mask)

        # Fit a line to the largest contour using cv2.fitLine()
        # This function returns a 4-element vector (vx, vy, x0, y0) which is the direction and a point on the line
        # vx, vy are the direction vector of the line, and (x0, y0) is a point on the line
        [vx, vy, x0, y0] = cv2.fitLine(largest_contour, cv2.DIST_L2, 0, 0.01, 0.01)

        # Negate the direction vector to reverse the direction (pointing in the correct direction)
        vx, vy = -vx, -vy  # Flip the direction

        # Length of the line to draw
        line_length = 60  # You can adjust the length of the line

        # Calculate two points for the line (one at the start and one at the end)
        # Extend the line in both directions to create a longer line
        point1 = (int(x0 - line_length * vx), int(y0 - line_length * vy))
        point2 = (int(x0 + line_length * vx), int(y0 + line_length * vy))

        # Draw the straight line on the frame
        cv2.line(frame, point1, point2, (0, 0, 255), 3)



    # Resize to the specified grid size
    resized_grid = cv2.resize(binary, (grid_size, grid_size), interpolation=cv2.INTER_NEAREST)

    # Map binary values to occupancy grid values (0 and 100)
    occupancy_grid = np.where(resized_grid == 255, 100, 0)
    # np.where() applies a condition to the resized_grid and creates a new grid
    # it turns the pixels where pixel value is 255 (white) to 100 and others to 0

    # Create a larger visual representation of the grid
    visual_grid = cv2.resize(occupancy_grid.astype(np.uint8), (900, 900), interpolation=cv2.INTER_NEAREST)

    # Map values to colors: 0 -> white (free), 100 -> black (occupied)
    visual_grid_color = np.zeros((900, 900, 3), dtype=np.uint8)
    visual_grid_color[visual_grid == 0] = [255, 255, 255]  # Free space (white)
    visual_grid_color[visual_grid == 100] = [0, 0, 0]      # Occupied space (black)

    # Add grid lines and numbers to the visualization
    cell_size = 900 // grid_size  # Size of each grid cell in the visual grid
    for i in range(grid_size):
        for j in range(grid_size):
            # Draw grid lines
            cv2.rectangle(visual_grid_color, (j * cell_size, i * cell_size),
                          ((j + 1) * cell_size, (i + 1) * cell_size), (0, 255, 0), 1)

            # Add numbers (0 or 100) inside each cell
            value = occupancy_grid[i, j]
            text_position = (j * cell_size + cell_size // 4, i * cell_size + cell_size // 2)
            cv2.putText(visual_grid_color, str(value), text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

    # Show the processed video frame with contours
    cv2.imshow("Original Frame with Contours", frame)

    # Show the occupancy grid visualization
    cv2.imshow("Occupancy Grid", visual_grid_color)
    # Display the grid lines together with the values

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
