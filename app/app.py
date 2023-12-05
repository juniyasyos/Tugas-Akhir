from dbsm import HashTable, PriorityQueue, Models
import json
import tkinter as tk
import tkinter.messagebox
import customtkinter as ctk
from icecream import ic


# Class untuk MenubarFrame
class MenubarFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Create File menu
        self.filemenu = tk.Menu(self.master)
        self.filemenu.add_command(label="New")
        self.filemenu.add_command(label="Open Project")

        # Create Setting menu
        self.settingmenu = tk.Menu(self.master)
        self.settingmenu.add_command(label="Theme")
        self.settingmenu.add_command(label="Setting Priority")

        # Create main menu bar
        self.menubar = tk.Menu(self.master)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Setting", menu=self.settingmenu)
        
        # Pack the menubar
        self.master.config(menu=self.menubar)

# Kelas untuk BerandaFrame
class BerandaFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.models = Models()
        self.models.load_file()
        
        self.data = self.models.get_queue_data()
        
        # Setting tampilan
        self.pack(side="top", fill="x", padx=10)

        # Judul
        self.title_frame = ctk.CTkFrame(self)

        # Body
        self.body_parent = ctk.CTkScrollableFrame(self, height=460)
        self.body_frame = [ctk.CTkFrame(self.body_parent) for i in range(len(self.data))]

        # Footer
        self.footer_frame = ctk.CTkFrame(self)

        # Judul Beranda
        self.label_judul = ctk.CTkLabel(self.title_frame, text="Beranda")
        self.label_judul.pack(side="left", fill="x", padx=5)
        self.label_judul.configure(font=("Serif", 20))
        
        # generate data didalam beranda    
        self.data_beranda()

        # Tombol Aksi Beranda
        self.btn_action_beranda = ctk.CTkButton(self.footer_frame, text="Tambah Rencana", command=self.action_beranda)
        self.btn_action_beranda.pack(padx=35, pady=10, side="right")
        
        # Tombol eksekusi rencana
        self.btn_execution = ctk.CTkButton(self.footer_frame, text="Eksekusi Rencana")
        self.btn_execution.pack(padx=5, pady=10, side="right")

        # >> Start Eksekusi sub frame di dalam frame <<
        self.title_frame.pack(side="top", fill="x", padx=10, pady=5)
        
        for frame in self.body_frame:
            frame.pack(side="top", fill="x", padx=10, pady=10)
            
        self.body_parent.pack(fill="x")
        
        self.footer_frame.pack(side="top", fill="x")
        # >>>> End <<<<

    def action_beranda(self):
        # Implementasi tindakan Beranda
        tkinter.messagebox.showinfo("Action Beranda", "Tindakan Beranda berhasil dijalankan")

    def data_beranda(self):

        ic(self.data)
        ic(len(self.data))
        # Tampilkan data di body frame
        for i, data in enumerate(self.data):
            label_no = ctk.CTkFrame(self.body_frame[i])
            label_no_val = ctk.CTkLabel(label_no, text=f"No. {i + 1}")
            label_no_val.pack(side="left", fill="x", padx=10)
            label_no.pack(side="top", fill="x", padx=5, pady=5)

            label_judul_val = ctk.CTkLabel(label_no, text=data["judul"])
            label_judul_val.pack(side="left", fill="x", padx=10)

            label_deskripsi = ctk.CTkFrame(self.body_frame[i])
            label_deskripsi_val = ctk.CTkLabel(label_deskripsi, text=data["deskripsi"])
            label_deskripsi_val.pack(side="left", fill="x", padx=10)
            label_deskripsi.pack(side="top", fill="x", padx=5, pady=5)
            label_deskripsi.configure(fg_color="transparent")

            label_prioritas = ctk.CTkFrame(self.body_frame[i])
            lebel_prioritas_val = ctk.CTkLabel(label_prioritas, text=f"Prioritas: {data['prioritas']}")
            lebel_prioritas_val.pack(side="right", fill="x", padx=10, pady=5)
            label_prioritas.pack(side="bottom", fill="x", padx=5, pady=8)
            label_prioritas.configure(fg_color="transparent")
        
# Kelas untuk SidebarFrame
class SidebarFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Tombol Beranda
        self.btn_beranda = ctk.CTkButton(self, text="Beranda", command=lambda: master.switch_frame(BerandaFrame(master)))
        self.btn_beranda.pack(padx=35, pady=10)

        # Tombol Manajemen
        self.btn_manajemen = ctk.CTkButton(self, text="Manajemen", command=lambda: master.switch_frame(ManajemenFrame(master)))
        self.btn_manajemen.pack(padx=35, pady=10)

    def switch_frame(self, frame):
        # Alihkan frame jendela utama ke frame yang ditentukan
        self.master.main_window = frame
        self.master.main_window.pack()

# Kelas untuk ManajemenFrame
class ManajemenFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(side="top", fill="x", padx=10)
        
        # Judul Manajemen
        self.label_judul = ctk.CTkLabel(self, text="Manajemen")
        self.label_judul.pack(side="top", fill="x")

        # Tombol Aksi Manajemen
        self.btn_action_manajemen = ctk.CTkButton(self, text="Action Manajemen", command=self.action_manajemen)
        self.btn_action_manajemen.pack(padx=35, pady=10)

    def action_manajemen(self):
        # Implementasi tindakan Manajemen
        tkinter.messagebox.showinfo("Action Manajemen", "Tindakan Manajemen berhasil dijalankan")

# Kelas untuk App
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Konfigurasi judul jendela, geometri, dll.
        self.title("Manajamen Proyek Perencanaan Pembangunan")
        self.geometry("1100x580")

        # Tambahkan menu File dan Setting dengan opsi yang relevan
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.setting = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="Setting", menu=self.setting)
        self.filemenu.add_command(label="New")
        self.filemenu.add_command(label="Open Project")
        self.setting.add_command(label="Theme")
        self.setting.add_command(label="Setting Priority")
        

        # Buat frame sidebar
        self.sidebard_frame = SidebarFrame(self)
        self.sidebard_frame.pack(side="left", fill="y")
        
        # Buat frame menu bar 
        self.menubar_frame = MenubarFrame(self)

        # Buat frame jendela utama dan initiasi awal tampilan
        self.main_window = BerandaFrame(self)

    def switch_frame(self, frame):
        # Mengalihkan frame jendela utama ke frame yang ditentukan
        self.main_window.pack_forget()
        self.main_window = frame
        self.main_window.pack()      
        
# Eksekusi kode
if __name__ == "__main__":
    app = App()
    app.mainloop()
