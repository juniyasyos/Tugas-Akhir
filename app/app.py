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
class BerandaFrame(ctk.CTkTabview):
    def __init__(self, master):
        super().__init__(master)
        
        # Inisiai tab didalam beranda
        self.add("Rencana")
        self.add("Progres")
        self.add("Selesai")

        self.models = Models()
        self.models.load_file()
        
        # Setting tampilan
        self.pack(side="top", fill="x", padx=10)

        data_hash = self.models.get_hash_data()
        
        # >> Start Style Tab Rencana << 
        rencana_btn = [["Eksekusi Rencana",self.execution_plan]]
        self.set_tab_beranda("Rencana", data=self.models.get_queue_data(), btn=rencana_btn)
        
        # >> Start Style Tab Rencana << 
        self.set_tab_beranda("Progres", data=self.models.get_hash_data()['Progres'])
        
        # # >> Start Style Tab Rencana << 
        self.set_tab_beranda("Selesai", data=self.models.get_hash_data()['Selesai'])


    def execution_plan(self):
        # Buat pop up
        popup = ctk.CTk()
        popup.title("Konfirmasi Menjalankan Rencana")
        popup.geometry("320x180")
        
        # Fungsi mengambil prioritas tertinggi dalam antian dan status berubah menjadi progres
        def dequeue():
            self.models.data_hash.set_status(self.models.queue_plan.peek()[0], status="progres")
            self.models.queue_plan.dequeue()
            self.models.save_file()
            popup.destroy()

        # Tambahkan label
        label = ctk.CTkLabel(popup, text="Apakah Anda yakin ingin menjalankan rencana?\n"+self.models.queue_plan.peek()[0])
        label.pack(pady=15)

        # Tambahkan tombol ya
        btn_ya = ctk.CTkButton(popup, text="Ya", command=lambda:dequeue())
        btn_ya.pack(side="right", padx=15)

        # Tambahkan tombol tidak
        btn_tidak = ctk.CTkButton(popup, text="Tidak", command=lambda: popup.destroy())
        btn_tidak.pack(side="right", padx=15)

        # Tampilkan pop up
        popup.mainloop()

    
    def set_status_tabprogres(self, key):
        # Buat pop up
        popup = ctk.CTk()
        popup.title("Konfirmasi Merubah Status Rencana")
        popup.geometry("320x180")
        
        # Fungsi mengambil prioritas tertinggi dalam antian dan status berubah menjadi progres
        def set_status():
            self.models.data_hash.set_status(key, status="selesai")
            self.models.save_file()
            popup.destroy()

        # Tambahkan label
        label = ctk.CTkLabel(popup, text="Apakah Anda yakin rencana sudah selesai dijalankan?")
        label.pack(pady=15)

        # Tambahkan tombol ya
        btn_ya = ctk.CTkButton(popup, text="Ya", command=lambda:set_status())
        btn_ya.pack(side="right", padx=15)

        # Tambahkan tombol tidak
        btn_tidak = ctk.CTkButton(popup, text="Tidak", command=lambda: popup.destroy())
        btn_tidak.pack(side="right", padx=15)

        # Tampilkan pop up
        popup.mainloop()
        

    def data_beranda(self, data):
        # Tampilan jika tidak ada data
        if len(data) == 0:
            label_zonk = ctk.CTkLabel(self.body_frame, text="Tidak ada data di dalam tab ini")
            label_zonk.pack(fill="y")
            label_zonk.configure(fg_color="transparent")
        
        # Tampilkan data di body frame
        for i, data in enumerate(data):
            label_no = ctk.CTkFrame(self.body_frame[i])
            label_no_val = ctk.CTkLabel(label_no, text=f"No. {i + 1}")
            label_no_val.pack(side="left", fill="x", padx=10)
            label_no.pack(side="top", fill="x", padx=5, pady=5)

            label_judul_val = ctk.CTkLabel(label_no, text=data["judul"])
            label_judul_val.pack(side="left", fill="x", padx=10)

            label_deskripsi = ctk.CTkFrame(self.body_frame[i])
            label_deskripsi_val = ctk.CTkTextbox(label_deskripsi)
            label_deskripsi_val.grid(row=0, column=0, )
            label_deskripsi_val.insert("0.0", data["deskripsi"])
            label_deskripsi_val.configure(state="disable", width=900)
            
            label_deskripsi_val.pack(side="left", fill="x")
            label_deskripsi.pack(side="top", fill="x", padx=5, pady=5)
            label_deskripsi.configure(fg_color="transparent")

            footer_data = ctk.CTkFrame(self.body_frame[i])

            if data['status'] == "progres":
                btn_set_status_frame = ctk.CTkFrame(footer_data)
                btn_set_status = ctk.CTkButton(btn_set_status_frame, text="Status", command=lambda:self.set_status_tabprogres(data['judul']))
                btn_set_status.pack(side="left", pady=10)
                btn_set_status_frame.pack(side="left", fill="x")
                btn_set_status_frame.configure(fg_color="transparent")
            
            label_prioritas = ctk.CTkFrame(footer_data)
            lebel_prioritas_val = ctk.CTkLabel(label_prioritas, text=f"Prioritas: {data['prioritas']}")
            lebel_prioritas_val.pack(side="right", fill="x", padx=10, pady=5)
            label_prioritas.pack(side="right", fill="x", padx=5, pady=8)
            label_prioritas.configure(fg_color="transparent")
            
            footer_data.pack(side="bottom", fill="x", padx=5)
            footer_data.configure(fg_color="transparent")
        

    def set_tab_beranda(self, tab_name, data, btn=[]):
        # Judul
        self.title_frame = ctk.CTkFrame(self.tab(tab_name))
        
        # Body
        self.body_parent = ctk.CTkScrollableFrame(self.tab(tab_name), height=650)
        self.body_frame = [ctk.CTkFrame(self.body_parent) for i in range(len(data))] if len(data) > 0 else ctk.CTkFrame(self.body_parent)

        # Footer
        self.footer_frame = ctk.CTkFrame(self.tab(tab_name))

        # Judul Beranda
        self.label_judul = ctk.CTkLabel(self.title_frame, text=f"Beranda: {tab_name}")
        self.label_judul.pack(side="left", fill="x", padx=5)
        self.label_judul.configure(font=("Serif", 20))
        
        # generate data didalam beranda
        self.data_beranda(data)

        # Generate btn
        for button_data in btn:
            button = ctk.CTkButton(self.footer_frame, text=button_data[0], command=button_data[1])
            button.pack(padx=35, pady=10, side="right")

        # >> Start Eksekusi sub frame di dalam frame <<
        self.title_frame.pack(side="top", fill="x", padx=10, pady=5)
        
        if len(data) > 0:
            for frame in self.body_frame:
                frame.pack(side="top", fill="x", padx=10, pady=10)
        else:
            self.body_frame.pack(side="top", fill="x", padx=10, pady=10)
            
        self.body_parent.pack(fill="x")
        
        self.footer_frame.pack(side="top", fill="x")
        # >> End Eksekusi << 

        
# Kelas untuk SidebarFrame
class SidebarFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Tombol Beranda
        self.btn_beranda = ctk.CTkButton(self, text="Beranda", command=lambda: master.switch_frame(BerandaFrame(master)))
        self.btn_beranda.pack(padx=35, pady=20)

        # Tombol Manajemen
        self.btn_manajemen = ctk.CTkButton(self, text="Manajemen", command=lambda: master.switch_frame(ManajemenFrame(master)))
        self.btn_manajemen.pack(padx=35, pady=10)

    def switch_frame(self, frame):
        # Alihkan frame jendela utama ke frame yang ditentukan
        self.master.main_window = frame
        self.master.main_window.pack()

# Kelas untuk ManajemenFrame
class ManajemenFrame(ctk.CTkTabview):
    def __init__(self, master):
        super().__init__(master)
        self.configure(anchor="nw")
        
        # Inisiai tab didalam beranda
        self.add("Tambah Rencana Baru")
        self.add("Edit Rencana")

        self.models = Models()
        self.models.load_file()
        
        # Setting tampilan
        self.pack(side="top", fill="x", padx=10)

        # >> Start Style Tab Rencana << 
        self.set_tab_manajemen("Tambah Rencana Baru", func=lambda: self.set_plan())
        
        # >> Start Style Tab Rencana << 
        self.set_tab_manajemen("Edit Rencana")

    def remove_plan(self, key):
        # Buat pop up
        popup = ctk.CTk()
        popup.title("Konfirmasi Menghapus Rencana Pembangunan")
        popup.geometry("320x180")
        
        def remove_plan(key):
            self.models.data_hash.remove(key=key)
            self.models.queue_plan.remove(key)
            self.models.save_file()
            self.models.load_file()
            popup.destroy()
        
        # Tambahkan label
        label = ctk.CTkLabel(popup, text="Apakah Anda yakin ingin menghapus rencana?\n"+key)
        label.pack(pady=15)

        # Tambahkan tombol ya
        btn_ya = ctk.CTkButton(popup, text="Ya", command=lambda:remove_plan(key=key))
        btn_ya.pack(side="right", padx=15)

        # Tambahkan tombol tidak
        btn_tidak = ctk.CTkButton(popup, text="Tidak", command=lambda: popup.destroy())
        btn_tidak.pack(side="right", padx=15)

        # Tampilkan pop up
        popup.mainloop()
        
        
    
    def data_Manajemen(self, data):
        # Tampilkan data di body frame
        for i, data in enumerate(data):
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
        

    def set_tab_manajemen(self, tab_name, func=None):
        # Judul
        self.title_frame = ctk.CTkFrame(self.tab(tab_name))
        
        # Body
        self.body_parent = ctk.CTkScrollableFrame(self.tab(tab_name), height=650)
        if tab_name != "Tambah Rencana Baru":
            data = self.models.get_hash_data(all_category=True)
            self.body_frame = [ctk.CTkFrame(self.body_parent) for i in range(len(data))] if len(data) > 0 else ctk.CTkFrame(self.body_parent)
        else:
            self.body_frame = ctk.CTkFrame(self.body_parent)
        
        # Footer
        self.footer_frame = ctk.CTkFrame(self.tab(tab_name))

        # Judul Manajemen
        self.label_judul = ctk.CTkLabel(self.title_frame, text=tab_name)
        self.label_judul.pack(side="left", fill="x")
        self.label_judul.configure(font=("Serif", 15))
        
        # generate data dalam frame
        if tab_name != "Tambah Rencana Baru":
            self.body_manejemen(self.models.get_hash_data(all_category=True))
        
        # generate aksi di dalam frame nya
        if func is not None:
            func()

        # >> Start Eksekusi sub frame di dalam frame <<
        self.title_frame.pack(side="top", fill="x", padx=10, pady=5)

        if type(self.body_frame) is list:
            ic("masuk kok")
            for frame in self.body_frame:
                frame.pack(side="top", fill="x", padx=10, pady=10)
        else:
            self.body_frame.pack(side="top", fill="x", padx=10, pady=10)
            
        self.body_parent.pack(fill="x")
        
        self.footer_frame.pack(side="top", fill="x")
    
    
    def body_manejemen(self, data):
        # Tampilan jika tidak ada data
        if len(data) == 0:
            label_zonk = ctk.CTkLabel(self.body_parent, text="Tidak ada data di dalam tab ini")
            label_zonk.pack(fill="y")
            label_zonk.configure(fg_color="transparent")
        
        # Tampilkan data di body frame
        for i, data in enumerate(data):
            label_no = ctk.CTkFrame(self.body_frame[i])
            label_no_val = ctk.CTkLabel(label_no, text=f"No. {i + 1}")
            label_no_val.pack(side="left", fill="x", padx=10)
            label_no.pack(side="top", fill="x", padx=5, pady=5)

            label_judul_val = ctk.CTkLabel(label_no, text=data["judul"])
            label_judul_val.pack(side="left", fill="x", padx=10)

            label_deskripsi = ctk.CTkFrame(self.body_frame[i])
            label_deskripsi_val = ctk.CTkTextbox(label_deskripsi)
            label_deskripsi_val.grid(row=0, column=0, )
            label_deskripsi_val.insert("0.0", data["deskripsi"])
            label_deskripsi_val.configure(state="disable", width=900)
            
            label_deskripsi_val.pack(side="left", fill="x")
            label_deskripsi.pack(side="top", fill="x", padx=5, pady=5)
            label_deskripsi.configure(fg_color="transparent")

            footer_data = ctk.CTkFrame(self.body_frame[i])

            btn_set_status_frame = ctk.CTkFrame(footer_data)
            
            btn_set_status = ctk.CTkButton(btn_set_status_frame, text="Edit", command=lambda:self.set_plan(action="edit", data=data))
            btn_set_status.pack(side="left", pady=10)
            btn_set_status_frame.pack(side="left", fill="x")

            btn_set_status = ctk.CTkButton(btn_set_status_frame, text="Hapus", command=lambda:self.remove_plan(key=data["judul"]))
            btn_set_status.pack(side="left", pady=10, padx=15)
            btn_set_status_frame.pack(side="left", fill="x")

            btn_set_status_frame.configure(fg_color="transparent")
            
            label_prioritas = ctk.CTkFrame(footer_data)
            lebel_prioritas_val = ctk.CTkLabel(label_prioritas, text=f"Prioritas: {data['prioritas']}")
            lebel_prioritas_val.pack(side="right", fill="x", padx=10, pady=5)
            label_prioritas.pack(side="right", fill="x", padx=5, pady=8)
            label_prioritas.configure(fg_color="transparent")
            
            footer_data.pack(side="bottom", fill="x", padx=5)
            footer_data.configure(fg_color="transparent")
    
      
    def set_plan(self, action='add', data={}):
        if type(self.body_frame) == list:
            for frame in self.body_frame:
                frame.pack_forget()
        
        # Label Judul
        judul_frame = ctk.CTkFrame(self.body_parent)
        label_judul = ctk.CTkLabel(judul_frame, text="Judul Projek")
        label_judul.pack(side="left")
        judul_frame.pack(side="top", fill="x", padx=5)
        judul_frame.configure(fg_color="transparent")
        
        # Text input Judul
        input_judul_frame = ctk.CTkFrame(self.body_parent)
        input_judul = ctk.CTkEntry(input_judul_frame)
        if action != "add":
            input_judul.insert(0, str(data['judul']))
        input_judul.pack(side="left")
        input_judul_frame.pack(side="top", fill="x", padx=5, pady=15)
        var_judul = input_judul.get()
        
        # Label Deskripsi
        deskripsi_frame = ctk.CTkFrame(self.body_parent)
        label_deskripsi = ctk.CTkLabel(deskripsi_frame, text="Deskripsi")
        label_deskripsi.pack(side="left")
        deskripsi_frame.pack(side="top", fill="x", padx=5)
        deskripsi_frame.configure(fg_color="transparent")
        
        # Text input deskripsi
        input_deskripsi_frame = ctk.CTkFrame(self.body_parent)
        input_deskripsi = ctk.CTkTextbox(input_deskripsi_frame, width=400, corner_radius=1)
        input_deskripsi.grid(row=0, column=0, sticky="nsew")
        if action != "add":
            input_deskripsi.insert("0.0", data['deskripsi'])
        else:
            input_deskripsi.insert("0.0", "Tulis Deskripsi disini")
        input_deskripsi_frame.pack(side="top", fill="x", padx=5, pady=15)
        
        # Label prioritas
        prioritas_frame = ctk.CTkFrame(self.body_parent)
        label_prioritas = ctk.CTkLabel(prioritas_frame, text="Nilai Prioritas")
        label_prioritas.pack(side="left")
        prioritas_frame.pack(side="top", fill="x", padx=5)
        prioritas_frame.configure(fg_color="transparent")
        
        # Text input prioritas
        input_prioritas_frame = ctk.CTkFrame(self.body_parent)
        input_prioritas = ctk.CTkEntry(input_prioritas_frame)
        if action != "add":
            input_prioritas.insert(0, data['prioritas'])
        input_prioritas.pack(side="left")
        input_prioritas_frame.pack(side="top", fill="x", padx=5, pady=15)
        
        # Label status
        status_frame = ctk.CTkFrame(self.body_parent)
        label_status = ctk.CTkLabel(status_frame, text="Pilihlah status dari projek")
        label_status.pack(side="left")
        status_frame.pack(side="top", fill="x", padx=5)
        status_frame.configure(fg_color="transparent")
        
        radio_btn_status = ctk.CTkFrame(self.body_parent)
        var_status = tk.IntVar(value=0)
        btn_rencana = ctk.CTkRadioButton(radio_btn_status, text="Rencana", variable=var_status, value=1)
        btn_progres = ctk.CTkRadioButton(radio_btn_status, text="Progres", variable=var_status, value=2)
        btn_selesai = ctk.CTkRadioButton(radio_btn_status, text="Selesai", variable=var_status, value=3)
        
        if action != "add":
            if data['status'] == 'rencana':
                btn_rencana.select()
            if data['status'] == 'progres':
                btn_progres.select()
            if data['status'] == 'selesai':
                btn_selesai.select()
        else:
            btn_rencana.select()
        
        btn_rencana.pack(side="right")
        btn_progres.pack(side="right")
        btn_selesai.pack(side="right")  
        radio_btn_status.pack(side="left", pady=15)
        
        def action():
            # Ambil nilai dari input user
            var_judul = input_judul.get()
            var_prioritas = input_prioritas.get()
            var_deskripsi = input_deskripsi.get("0.0","end")
            
            if var_status.get() == 1:
                status = "rencana"
            elif var_status.get() == 2:
                status = "progres"
            elif var_status.get() == 3:
                status = "selesai"
            
            
            if var_judul != '' and var_prioritas != '':
                self.models.add_data(var_judul, {'deskripsi':var_deskripsi, 'status':status, 'priority':int(var_prioritas)})
                self.models.save_file()
                
                tkinter.messagebox.showinfo("Rencana ditambahkan", "Rencana berhasil ditambahkan kedalam antrian")
            else:
                tkinter.messagebox.showinfo("Terdapat Kesalahan", "Pastikan judul sudah terisi dan nilai prioritas merupakan angka")
        
        btn_action = ctk.CTkButton(self.footer_frame, text="Simpan Rencana", command=action)
        btn_action.pack(padx=35, pady=10, side="right")


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
