import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
from threading import Thread

class ImageCopierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Copier")

        # Variables para almacenar las rutas seleccionadas
        self.image_path = ""
        self.roms_folder_path = ""

        # Crear un cuadro para organizar los widgets
        self.frame = tk.Frame(root)

        # Crear widgets
        self.label_image = tk.Label(self.frame, text="Seleccionar Imagen:")
        self.button_browse_image = tk.Button(self.frame, text="Examinar", command=self.browse_image)

        self.image_path_entry = tk.Entry(self.frame, width=50, state='readonly')
        self.image_path_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.label_roms_folder = tk.Label(self.frame, text="Seleccionar Carpeta de ROMs:")
        self.button_browse_roms_folder = tk.Button(self.frame, text="Examinar", command=self.browse_roms_folder)

        self.roms_folder_path_entry = tk.Entry(self.frame, width=50, state='readonly')
        self.roms_folder_path_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.button_copy_images = tk.Button(self.frame, text="Copiar Imágenes", command=self.copy_images)

        # Barra de progreso
        self.progress_bar = ttk.Progressbar(self.frame, mode="indeterminate")

        # Posicionar widgets en el cuadro
        self.label_image.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.button_browse_image.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.label_roms_folder.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.button_browse_roms_folder.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        self.button_copy_images.grid(row=2, column=0, columnspan=3, pady=20)

        self.progress_bar.grid(row=3, column=0, columnspan=3, pady=10)

        # Posicionar el cuadro en la ventana principal
        self.frame.pack(padx=20, pady=20)

    def browse_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.image_path_entry.config(state='normal')
        self.image_path_entry.delete(0, tk.END)
        self.image_path_entry.insert(0, self.image_path)
        self.image_path_entry.config(state='readonly')

    def browse_roms_folder(self):
        self.roms_folder_path = filedialog.askdirectory()
        self.roms_folder_path_entry.config(state='normal')
        self.roms_folder_path_entry.delete(0, tk.END)
        self.roms_folder_path_entry.insert(0, self.roms_folder_path)
        self.roms_folder_path_entry.config(state='readonly')

    def copy_images(self):
        if not self.image_path or not self.roms_folder_path:
            return

        self.progress_bar.start()
        # Utilizar un hilo para no bloquear la interfaz de usuario
        thread = Thread(target=self.copy_images_thread)
        thread.start()

    def copy_images_thread(self):
        try:
            image_name = os.path.basename(self.image_path)
            rom_files = [f for f in os.listdir(self.roms_folder_path) if os.path.isfile(os.path.join(self.roms_folder_path, f))]

            total_roms = len(rom_files)
            progress_step = 100 / total_roms

            for i, rom_file in enumerate(rom_files, start=1):
                rom_name, _ = os.path.splitext(rom_file)
                new_image_name = f"{rom_name}{os.path.splitext(image_name)[1]}"
                shutil.copy(self.image_path, os.path.join(self.roms_folder_path, new_image_name))
                progress_value = i * progress_step
                self.progress_bar['value'] = progress_value
                self.root.update_idletasks()

            self.progress_bar.stop()
            messagebox.showinfo("Copiado completado", "Imágenes copiadas exitosamente.")
        except Exception as e:
            self.progress_bar.stop()
            messagebox.showerror("Error", f"Error al copiar imágenes: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCopierApp(root)
    root.mainloop()
