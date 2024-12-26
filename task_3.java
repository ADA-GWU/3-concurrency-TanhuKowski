package main; //include your package name

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class ImageProcessor {

    public static void main(String[] args) {
        try {
            // Load input parameters
            String imagePath = args[0];
            int blockSize = Integer.parseInt(args[1]);
            String threadMode = args[2];

            // Read the image file
            BufferedImage sourceImage = ImageIO.read(new File(imagePath));

            // Determine the original dimensions of the image
            int imageWidth = sourceImage.getWidth();
            int imageHeight = sourceImage.getHeight();

            // Get screen dimensions for potential resizing
            Dimension screenResolution = Toolkit.getDefaultToolkit().getScreenSize();
            int maxScreenWidth = (int) screenResolution.getWidth();
            int maxScreenHeight = (int) screenResolution.getHeight();

            // Resize image if necessary
            BufferedImage processedImage;
            boolean resized = false;
            if (imageWidth > maxScreenWidth || imageHeight > maxScreenHeight) {
                processedImage = resizeImage(sourceImage, maxScreenWidth, maxScreenHeight);
                resized = true;
            } else {
                processedImage = sourceImage;
            }

            // Display the image in a GUI
            JFrame displayFrame = new JFrame("Processed Image Display");
            JLabel imageLabel = new JLabel(new ImageIcon(processedImage));
            displayFrame.add(imageLabel);
            displayFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            displayFrame.pack();
            displayFrame.setVisible(true);

            // Determine thread configuration
            int threadCount;
            if ("S".equalsIgnoreCase(threadMode)) {
                threadCount = 1;
            } else if ("M".equalsIgnoreCase(threadMode)) {
                threadCount = Runtime.getRuntime().availableProcessors();
            } else {
                throw new IllegalArgumentException("Unsupported thread mode: " + threadMode);
            }

            // Set up thread pool for parallel processing
            ExecutorService executor = Executors.newFixedThreadPool(threadCount);

            int rowsPerThread = imageHeight / threadCount;
            for (int y = 0; y < imageHeight; y += rowsPerThread) {
                int startRow = y;
                executor.submit(() -> applyAverageColor(processedImage, blockSize, startRow, rowsPerThread, imageLabel));
            }

            executor.shutdown();
            executor.awaitTermination(Long.MAX_VALUE, TimeUnit.MILLISECONDS);

            // Save the resulting image
            File outputImageFile = new File("output_image.jpg");
            if (resized) {
                ImageIO.write(applyAverageColorToOriginal(sourceImage, blockSize), "jpg", outputImageFile);
            } else {
                ImageIO.write(processedImage, "jpg", outputImageFile);
            }

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }

    private static BufferedImage resizeImage(BufferedImage original, int maxWidth, int maxHeight) {
        int newType = original.getType() == 0 ? BufferedImage.TYPE_INT_RGB : original.getType();
        Image scaled = original.getScaledInstance(maxWidth, maxHeight, Image.SCALE_SMOOTH);
        BufferedImage resized = new BufferedImage(maxWidth, maxHeight, newType);
        Graphics2D g = resized.createGraphics();
        g.drawImage(scaled, 0, 0, null);
        g.dispose();
        return resized;
    }

    private static void applyAverageColor(BufferedImage image, int blockSize, int startRow, int height, JLabel label) {
        int imageWidth = image.getWidth();
        for (int y = startRow; y < startRow + height && y < image.getHeight(); y += blockSize) {
            for (int x = 0; x < imageWidth; x += blockSize) {
                int avgRed = 0, avgGreen = 0, avgBlue = 0, count = 0;
                for (int i = x; i < x + blockSize && i < imageWidth; i++) {
                    for (int j = y; j < y + blockSize && j < image.getHeight(); j++) {
                        int color = image.getRGB(i, j);
                        avgRed += (color >> 16) & 0xFF;
                        avgGreen += (color >> 8) & 0xFF;
                        avgBlue += color & 0xFF;
                        count++;
                    }
                }
                avgRed /= count;
                avgGreen /= count;
                avgBlue /= count;
                int avgColor = (avgRed << 16) | (avgGreen << 8) | avgBlue;
                for (int i = x; i < x + blockSize && i < imageWidth; i++) {
                    for (int j = y; j < y + blockSize && j < image.getHeight(); j++) {
                        image.setRGB(i, j, avgColor);
                    }
                }
                label.setIcon(new ImageIcon(image));
                try {
                    Thread.sleep(40);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        }
    }

    private static BufferedImage applyAverageColorToOriginal(BufferedImage image, int blockSize) {
        int width = image.getWidth();
        int height = image.getHeight();
        for (int y = 0; y < height; y += blockSize) {
            for (int x = 0; x < width; x += blockSize) {
                int avgRed = 0, avgGreen = 0, avgBlue = 0, count = 0;
                for (int i = x; i < x + blockSize && i < width; i++) {
                    for (int j = y; j < y + blockSize && j < height; j++) {
                        int color = image.getRGB(i, j);
                        avgRed += (color >> 16) & 0xFF;
                        avgGreen += (color >> 8) & 0xFF;
                        avgBlue += color & 0xFF;
                        count++;
                    }
                }
                avgRed /= count;
                avgGreen /= count;
                avgBlue /= count;
                int avgColor = (avgRed << 16) | (avgGreen << 8) | avgBlue;
                for (int i = x; i < x + blockSize && i < width; i++) {
                    for (int j = y; j < y + blockSize && j < height; j++) {
                        image.setRGB(i, j, avgColor);
                    }
                }
            }
        }
        return image;
    }
}
