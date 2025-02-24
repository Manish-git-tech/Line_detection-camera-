

# **Line Detection and Occupancy Grid Mapping**  

This project detects a black line in a video and represents it as an occupancy grid, similar to a **ROS-style** mapping system. It processes video frames in real time using **OpenCV**, applies image processing techniques, and generates an adjustable occupancy grid using **NumPy**.  

---

## **Features**  
✅ Detects a black line from video frames  
✅ Generates an occupancy grid without using ROS  
✅ Adjustable grid size for different use cases  
✅ Real-time processing with OpenCV  
✅ Highlights line direction and contours for visualization  

---

## **How It Works**  

1. **Preprocessing:**  
   - Convert each video frame to grayscale.  
   - Apply Gaussian blur to reduce noise.  
   - Use binary thresholding to highlight the black line.  

2. **Line Detection:**  
   - Identify contours in the image.  
   - Select the largest contour as the black line.  
   - Fit a direction line using `cv2.fitLine()`.  

3. **Grid Mapping:**  
   - Resize the detected line into a **100x100** (or custom) occupancy grid.  
   - Use NumPy to assign grid values:  
     - `100` for occupied (line detected)  
     - `0` for free space  

4. **Visualization:**  
   - Display the original video frame with detected contours.  
   - Generate a zoomed-in occupancy grid with grid lines and labels.  
   - Highlight the detected path’s direction using a red guiding line.  

---

## **Installation**  

### **Requirements**  
- Python 3.x  
- OpenCV (`pip install opencv-python`)  
- NumPy (`pip install numpy`)  

### **Running the Project**  
1. Clone the repository:  
   ```sh
   git clone https://github.com/Line_detection-camera-.git
   cd Line_detection-camera-
   ```  
2. Place your video file in the project directory.  
3. Update the video path in `line.py`:  
   ```python
   video_path = "vid.mp4"  # Change this to your video file path
   ```  
4. Run the script:  
   ```sh
   python line.py
   ```  
5. Press **'q'** to exit the visualization.  

---

## **Code Overview**  

### `line.py`  
🔹 Reads video frames and applies preprocessing.  
🔹 Detects the largest black contour as the main path.  
🔹 Fits a directional line for better visualization.  
🔹 Generates and displays an occupancy grid.  

### **Adjustable Parameters**  
- `grid_size`: Changes the occupancy grid resolution.  
- `line_length`: Adjusts the detected path’s guide line length.  

---

## **Example Output**  

🖼 **Real-time Frame with Line Detection**  
![Frame with Detection](example_frame.png)  

🖼 **Generated Occupancy Grid**  
![Occupancy Grid](example_grid.png)  

---

## **Challenges & Solutions**  
🔸 **No ROS Support:** Used NumPy to manually create an occupancy grid.  
🔸 **Noisy Image Data:** Applied Gaussian blur and thresholding.  
🔸 **Processing Speed:** Resized frames for faster performance.  
🔸 **Unwanted Contours:** Selected only the largest detected contour.  

---

## **Future Improvements**  
🚀 Integrate with **robot navigation** for path-following applications.  
🎯 Enhance contour filtering to handle complex environments.  
📡 Expand to multi-line detection for lane tracking.  

 

---

## **Contributors**  
👤 **Manish Kumar**

