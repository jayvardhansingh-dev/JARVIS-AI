# vision/vision.py

import os
import time
from datetime import datetime

import cv2
from PIL import ImageGrab


class JarvisVision:
    """
    Vision system for JARVIS.

    Features:
    - Camera preview
    - Capture camera image
    - Capture screen
    - Basic image information
    - OCR text extraction
    """

    def __init__(self):

        self.camera = None

    # ==========================================
    # INITIALIZE CAMERA
    # ==========================================

    def initialize_camera(self, camera_index=0):

        self.camera = cv2.VideoCapture(camera_index)

        if not self.camera.isOpened():

            self.camera = None

            return (
                "Sir, I couldn't access the camera."
            )

        return "Camera initialized, sir."

    # ==========================================
    # CAMERA PREVIEW
    # ==========================================

    def camera_preview(self):

        if self.camera is None:

            result = self.initialize_camera()

            if self.camera is None:

                return result

        print(
            "JARVIS: Camera preview started."
        )

        print(
            "Press Q to close the camera."
        )

        while True:

            success, frame = self.camera.read()

            if not success:

                break

            cv2.imshow(
                "JARVIS Vision",
                frame
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):

                break

        self.release_camera()

        return "Camera preview closed, sir."

    # ==========================================
    # CAPTURE CAMERA IMAGE
    # ==========================================

    def capture_camera_image(self):

        if self.camera is None:

            result = self.initialize_camera()

            if self.camera is None:

                return result

        success, frame = self.camera.read()

        if not success:

            return (
                "Sir, I couldn't capture an image."
            )

        os.makedirs(
            "data/vision",
            exist_ok=True
        )

        filename = (
            "camera_"
            + datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )
            + ".jpg"
        )

        path = os.path.join(
            "data",
            "vision",
            filename
        )

        cv2.imwrite(
            path,
            frame
        )

        return (
            f"Camera image saved to {path}, sir."
        )

    # ==========================================
    # SCREEN CAPTURE
    # ==========================================

    def capture_screen(self):

        try:

            os.makedirs(
                "data/vision",
                exist_ok=True
            )

            filename = (
                "screen_"
                + datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )
                + ".png"
            )

            path = os.path.join(
                "data",
                "vision",
                filename
            )

            screenshot = ImageGrab.grab()

            screenshot.save(path)

            return (
                f"Screen captured and saved "
                f"to {path}, sir."
            )

        except Exception as error:

            return (
                f"Unable to capture screen: "
                f"{error}"
            )

    # ==========================================
    # IMAGE INFORMATION
    # ==========================================

    def image_information(self, image_path):

        if not os.path.exists(image_path):

            return (
                f"Sir, I couldn't find "
                f"{image_path}."
            )

        try:

            image = Image.open(image_path)

            width, height = image.size

            return (
                f"Image information:\n"
                f"Width: {width}px\n"
                f"Height: {height}px\n"
                f"Format: {image.format}\n"
                f"Mode: {image.mode}"
            )

        except Exception as error:

            return (
                f"Unable to analyze image: "
                f"{error}"
            )

    # ==========================================
    # OCR
    # ==========================================

    def extract_text(self, image_path):

        if not os.path.exists(image_path):

            return (
                f"Sir, I couldn't find "
                f"{image_path}."
            )

        try:

            import pytesseract

            image = Image.open(image_path)

            text = pytesseract.image_to_string(
                image
            )

            text = text.strip()

            if not text:

                return (
                    "Sir, I couldn't find "
                    "any readable text."
                )

            return (
                "Text detected:\n\n"
                + text
            )

        except ImportError:

            return (
                "OCR requires the "
                "pytesseract package."
            )

        except Exception as error:

            return (
                f"OCR failed: {error}"
            )

    # ==========================================
    # RELEASE CAMERA
    # ==========================================

    def release_camera(self):

        if self.camera is not None:

            self.camera.release()

            self.camera = None

        cv2.destroyAllWindows()


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    vision = JarvisVision()

    print("=" * 50)
    print("       JARVIS VISION SYSTEM TEST")
    print("=" * 50)

    while True:

        print("\n1. Camera preview")
        print("2. Capture camera image")
        print("3. Capture screen")
        print("4. Image information")
        print("5. Extract text from image")
        print("6. Exit")

        choice = input("\nChoose: ")

        if choice == "1":

            print(
                vision.camera_preview()
            )

        elif choice == "2":

            print(
                vision.capture_camera_image()
            )

            vision.release_camera()

        elif choice == "3":

            print(
                vision.capture_screen()
            )

        elif choice == "4":

            path = input(
                "Image path: "
            )

            print(
                vision.image_information(path)
            )

        elif choice == "5":

            path = input(
                "Image path: "
            )

            print(
                vision.extract_text(path)
            )

        elif choice == "6":

            vision.release_camera()

            print(
                "JARVIS: Vision system offline, sir."
            )

            break

        else:

            print(
                "JARVIS: Invalid command."
            )