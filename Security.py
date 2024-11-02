import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Tool")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')

        self.cover_image = None
        self.result_image = None
        self.secret_data = ""

        self.setup_ui()

    def setup_ui(self):
        # Frames for each section
        self.cover_frame = tk.Frame(self.root, width=350, height=400, bd=2, relief=tk.GROOVE, bg='#34495e')
        self.cover_frame.grid(row=0, column=0, padx=20, pady=20, sticky='n')
        tk.Label(self.cover_frame, text="Cover Image", bg='#34495e', fg='white', font=('Helvetica', 16, 'bold')).pack(pady=10)

        self.secret_frame = tk.Frame(self.root, width=350, height=400, bd=2, relief=tk.GROOVE, bg='#34495e')
        self.secret_frame.grid(row=0, column=1, padx=20, pady=20, sticky='n')
        tk.Label(self.secret_frame, text="Secret Text Input", bg='#34495e', fg='white', font=('Helvetica', 16, 'bold')).pack(pady=10)

        self.result_frame = tk.Frame(self.root, width=350, height=400, bd=2, relief=tk.GROOVE, bg='#34495e')
        self.result_frame.grid(row=0, column=2, padx=20, pady=20, sticky='n')
        tk.Label(self.result_frame, text="Result Image", bg='#34495e', fg='white', font=('Helvetica', 16, 'bold')).pack(pady=10)

        # Buttons for functionality
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.grid(row=1, column=0, columnspan=3, pady=20)

        button_style = {'bg': '#1abc9c', 'fg': 'white', 'font': ('Helvetica', 14, 'bold'), 'width': 18}

        tk.Button(button_frame, text="Load Cover Image", command=self.load_cover_image, **button_style).grid(row=0, column=0, padx=15, pady=10)
        tk.Button(button_frame, text="Hide Secret Text", command=self.hide_secret, **button_style).grid(row=0, column=1, padx=15, pady=10)
        tk.Button(button_frame, text="Restore Secret Text", command=self.restore_secret, **button_style).grid(row=0, column=2, padx=15, pady=10)
        tk.Button(button_frame, text="Save Result Image", command=self.save_result_image, **button_style).grid(row=1, column=0, padx=15, pady=10)
        tk.Button(button_frame, text="Show Hidden Text", command=self.show_hidden_text, **button_style).grid(row=1, column=1, padx=15, pady=10)
        tk.Button(button_frame, text="Clear All", command=self.clear_all, bg='#e74c3c', fg='white', font=('Helvetica', 14, 'bold'), width=18).grid(row=1, column=2, padx=15, pady=10)

        # Bit selection option
        selection_frame = tk.Frame(self.root, bg='#2c3e50')
        selection_frame.grid(row=2, column=0, columnspan=3, pady=10)

        self.bit_selection = tk.IntVar(value=1)
        tk.Label(selection_frame, text="Select number of LSBs:", bg='#2c3e50', fg='white', font=('Helvetica', 14)).grid(row=0, column=0, padx=5, pady=10)
        tk.OptionMenu(selection_frame, self.bit_selection, 1, 2, 3).grid(row=0, column=1, padx=5, pady=10)

    def load_cover_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("BMP files", "*.bmp")])
        if not file_path:
            return
        self.cover_image = Image.open(file_path)
        cover_img_display = ImageTk.PhotoImage(self.cover_image.resize((330, 330)))
        for widget in self.cover_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget != self.cover_frame.winfo_children()[0]:
                widget.destroy()
        tk.Label(self.cover_frame, image=cover_img_display).pack(pady=10)
        self.cover_frame.image = cover_img_display  # Keep a reference to avoid garbage collection

    def hide_secret(self):
        if not self.cover_image:
            messagebox.showerror("Error", "Please load a cover image first.")
            return
        secret_text = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not secret_text:
            return
        with open(secret_text, 'r') as f:
            self.secret_data = f.read()

        # Show secret text before hiding
        messagebox.showinfo("Secret Text", f"Secret Text to Hide:\n{self.secret_data}")

        # Convert text to binary
        secret_bits = ''.join(format(ord(c), '08b') for c in self.secret_data)
        num_bits = self.bit_selection.get()

        # Process image
        cover_array = np.array(self.cover_image, dtype=np.uint8)
        max_bits = cover_array.size * num_bits
        if len(secret_bits) > max_bits:
            messagebox.showerror("Error", "Secret text is too large to hide in the given image.")
            return

        # Embed secret bits into the cover image
        flat_cover = cover_array.flatten()
        mask = (0xFF << num_bits) & 0xFF
        for i in range(len(secret_bits)):
            bit = int(secret_bits[i])
            flat_cover[i] = (flat_cover[i] & mask) | bit

        # Reshape and save result
        result_array = flat_cover.reshape(cover_array.shape)
        self.result_image = Image.fromarray(result_array.astype(np.uint8))
        result_img_display = ImageTk.PhotoImage(self.result_image.resize((330, 330)))
        for widget in self.result_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget != self.result_frame.winfo_children()[0]:
                widget.destroy()
        tk.Label(self.result_frame, image=result_img_display).pack(pady=10)
        self.result_frame.image = result_img_display  # Keep a reference to avoid garbage collection

    def restore_secret(self):
        if not self.result_image:
            messagebox.showerror("Error", "Please hide a secret first.")
            return
        restored_text = self.extract_secret(self.result_image)
        if restored_text.strip():
            messagebox.showinfo("Restored Secret Text", f"Restored Secret Text:\n{restored_text}")
        else:
            messagebox.showinfo("Restored Secret Text", "No valid hidden text found.")

    def show_hidden_text(self):
        if not self.result_image:
            messagebox.showerror("Error", "No modified image to extract text from.")
            return
        hidden_text = self.extract_secret(self.result_image)
        if hidden_text.strip():
            messagebox.showinfo("Hidden Secret Text", f"Hidden Secret Text:\n{hidden_text}")
        else:
            messagebox.showinfo("Hidden Secret Text", "No valid hidden text found.")

    def extract_secret(self, image):
        num_bits = self.bit_selection.get()
        result_array = np.array(image).flatten()
        secret_bits = ''
        for i in range(0, len(result_array), 8 // num_bits):
            secret_bits += ''.join(str((result_array[i] >> (8 - num_bits)) & 1) for _ in range(num_bits))

        # Convert bits to characters
        secret_chars = []
        for i in range(0, len(secret_bits), 8):
            byte = secret_bits[i:i+8]
            if len(byte) == 8:
                secret_chars.append(chr(int(byte, 2)))
        restored_text = ''.join(secret_chars)
        return restored_text

    def save_result_image(self):
        if not self.result_image:
            messagebox.showerror("Error", "No result image to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=[("BMP files", "*.bmp")])
        if file_path:
            self.result_image.save(file_path)

    def clear_all(self):
        # Clear the images and frames
        for widget in self.cover_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget != self.cover_frame.winfo_children()[0]:
                widget.destroy()
        for widget in self.secret_frame.winfo_children():
            widget.destroy()
        for widget in self.result_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget != self.result_frame.winfo_children()[0]:
                widget.destroy()
        self.cover_image = None
        self.result_image = None
        self.secret_data = ""
        messagebox.showinfo("Clear All", "All data has been cleared.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()