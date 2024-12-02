
# Assignment 3. Concurrency

This task demonstrates how to process images using **single-threaded** and **multi-threaded** approaches. The program applies a block-wise averaging operation on an image, progressively updating the display for each block in a graphical interface (GUI). It also allows for real-time visualization of progress.

---

## **Features**

- Processes any `.jpg` image, regardless of size.
- Supports two modes of operation:
  - **Single-threaded**: Processes the image sequentially.
  - **Multi-threaded**: Uses parallel threads to process different regions of the image.
- Real-time GUI visualization:
  - Updates the image display block-by-block as it is processed.
  - Automatically resizes large images for display while processing the original resolution.
- Saves the final processed image as `result.jpg`.

---

## **Requirements**

- **Python 3.6** or higher
- Required libraries:
  - `Pillow` (for image processing)
  - `numpy` (for numerical operations)
  - `tkinter` (built-in library for GUI)

Install the required libraries using the following command:

```bash
pip install pillow numpy
```

---

## **Usage**

### **Command-Line Syntax**
```bash
python task_3.py <file_name> <square_size> <mode>
```

### **Arguments**

1. `file_name`: The name of the input image file (must be a `.jpg` file).
2. `square_size`: The size of the square block (e.g., 20 for 20x20 blocks).
3. `mode`: Processing mode:
   - `S`: Single-threaded mode.
   - `M`: Multi-threaded mode.

### **Example**

```bash
python task_3.py input.jpg 20 M
```

This processes `input.jpg` in **multi-threaded mode** with block size 20 pixels.

---

## **Program Behavior**

### **Input**
- The program loads a `.jpg` file specified by `file_name`.

### **Block Processing**
- The image is divided into square blocks of size `(square_size)x(square_size)`.
- For each block:
  - The average color is calculated based on its pixels.
  - All pixels in the block are replaced with this average color.

### **Modes**
- **Single-threaded (S):**
  - Processes blocks sequentially, from top to bottom and left to right.
- **Multi-threaded (M):**
  - Divides the image into regions, processing each region in parallel using a thread pool.
  - The number of threads is determined by the system's CPU cores.

### **Real-Time Visualization**
- Displays the image in a GUI window as it is processed block-by-block.
- For images larger than the screen size, the display is automatically resized for visualization, while the processing happens on the original resolution.

### **Output**
- The final processed image is saved as `result.jpg` in the current working directory.

---

## **How It Works**

### **Core Workflow**
1. **Load Image**:
   - The image is loaded and converted to an array using `Pillow` and `numpy`.
2. **Block Processing**:
   - Each block is processed by calculating its average color and applying it to the block.
3. **Single or Multi-threading**:
   - Single-threading processes each block sequentially.
   - Multi-threading assigns blocks to threads for parallel processing.
4. **GUI Visualization**:
   - A `Tkinter` GUI displays the image and updates its progress after processing each block.
   - Resizes the display for large images while preserving the original resolution during processing.
5. **Save Results**:
   - The processed image is saved as `result.jpg`.

---

## **Known Issues**
- Large images may take slightly longer to process in single-threaded mode.
- Multi-threaded processing is faster but may show minor variations due to threading behavior.

---


