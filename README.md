
# Assignment 3: Image Processing with Concurrency

This program processes images using single-threaded and multi-threaded methods. It applies block-wise averaging to modify the image and shows progress in a GUI.

---

## Features
- Processes any `.jpg` image.
- Two modes:
  - **Single-threaded (S):** Processes sequentially.
  - **Multi-threaded (M):** Uses parallel threads.
- Real-time GUI:
  - Updates display block-by-block.
  - Resizes large images for better display.
- Saves the processed image as `result.jpg`.

---

## Requirements
- **Java JDK 8 or higher**

---

## Usage
Run the program with:
```
java ImageProcessor <file_name> <block_size> <mode>
```

### Arguments:
- `file_name`: Name of the `.jpg` file to process.
- `block_size`: Size of blocks (e.g., `20` for 20x20 blocks).
- `mode`: 
  - `S`: Single-threaded.
  - `M`: Multi-threaded.

### Example:
```
java ImageProcessor input.jpg 20 M
```
This processes `input.jpg` in multi-threaded mode with a block size of 20.

---

## Program Behavior
1. Loads the image and resizes it if needed.
2. Divides the image into blocks and computes the average color for each.
3. Updates the GUI in real-time while processing.
4. Saves the result as `result.jpg`.
