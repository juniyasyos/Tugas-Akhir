import json
from icecream import ic

# Struktur data hashtable
class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [{} for _ in range(size)]

    def hash_function(self, key):
        # Fungsi hash djb2
        hash_value = 5381
        for char in key:
            hash_value = (hash_value * 33) ^ ord(char)
        return hash_value % self.size

    def insert(self, key, details):
        index = self.hash_function(key)
        self.table[index][key] = details

    def get(self, key):
        index = self.hash_function(key)
        slot = self.table[index]
        if slot is not None and key in slot:
            return slot[key]
        raise KeyError("Key not found")

    def remove(self, key):
        index = self.hash_function(key)
        if key in self.table[index]:
            del self.table[index][key]
        else:
            raise KeyError("Key not found")

    def load_data(self, data):
        self.size = data["size"]
        self.table = data["table"]
    
    def get_all(self):
        # Mengembalikan seluruh elemen dalam hashtable
        all_data = []
        for slot in self.table:
            for key, value in slot.items():
                all_data.append({key: value})
        return all_data
    
    def set_status(self, key, status):
        index = self.hash_function(key)
        self.table[index][key]['status'] = status

# Struktur data Priority Queue
class PriorityQueue:
    def __init__(self):
        self.queue = []

    def is_empty(self):
        return len(self.queue) == 0

    def enqueue(self, element, priority):
        # Menambahkan elemen dengan prioritas ke dalam antrian
        item = (element, priority)
        if self.is_empty():
            self.queue.append(item)
        else:
            inserted = False
            for i in range(len(self.queue)):
                if ic(ic(priority) > ic(self.queue[i][1])):
                    self.queue.insert(i, item)
                    inserted = True
                    break
            if not inserted:
                self.queue.append(item)

    def dequeue(self):
        # Menghapus dan mengembalikan elemen dengan prioritas tertinggi
        if not self.is_empty():
            return self.queue.pop(0)
        else:
            raise IndexError("Queue is empty")

    def peek(self):
        # Mengembalikan elemen dengan prioritas tertinggi tanpa menghapusnya
        if not self.is_empty():
            return self.queue[0]
        else:
            raise IndexError("Queue is empty")

    def load_data(self, data):
        self.queue = data.get("queue", [])

    def get_data(self, key):
        # Mengembalikan nilai dari elemen yang memiliki kunci sama dengan parameter
        for data in self.queue:
            if data[0] == key:
                return data[1]  # Mengembalikan nilai elemen jika kunci cocok
        # Jika kunci tidak ditemukan, dapatkan KeyError atau nilai default lainnya
        raise KeyError(f"Key '{key}' not found in the priority queue")

    def get_all(self):
        # Mengembalikan semua data yg tersimpan
        return self.queue

    def edit(self, value:dict):
        # contoh input = {'element': "elemen", 'priority':2}
        for data in self.queue:
            if data[0] == value['element']:
                data = (value['element'], value['priority'])

# Class Operasi dengan database / struktur data 
class Models:
    def __init__(self, file="save/db.json") -> None:
        self.queue_plan = PriorityQueue()
        self.data_hash = HashTable()
        self.file = file
    
    def load_file(self):
        # Mengambil data yang sudah disimpan dalam file tertentu
        with open(self.file, 'r') as load_data:
            data = json.load(load_data)
            self.queue_plan.load_data(data["QueuePriority"])
            self.data_hash.load_data(data["HashTable"])
    
    def save_file(self):
        # Penyimpanan data dalam bentuk dictionary dan disimpan kedalam file json
        data = {
            "QueuePriority": {"queue":self.queue_plan.get_all()},
            "HashTable": {"size":self.data_hash.size,"table":self.data_hash.table}
        }
        
        with open(self.file, 'w') as json_file:
            json.dump(data, json_file)
    
    def add_data(self, key, value):
        # Menambahkan data edalam antrian rencana dan kedalam data hash
        # Contoh input:
        #   key = "Pembangunan A" -> str
        #   value = "{'deskripsi':'Deskripsi 1', 'status':'Do it', 'priority' : 2}" -> dict
        
        if value['status'] == "rencana":
            self.queue_plan.enqueue(key, value['priority'])
        self.data_hash.insert(key, value)
    
    def get_queue_data(self):
        all_data_queue = self.queue_plan.get_all()
        all_data_hash = self.data_hash.get_all()

        result = []
        for queue in all_data_queue:
            for hash_data in all_data_hash:
                if queue[0] == list(hash_data.keys())[0]:
                    result.append({
                        "judul": queue[0],
                        "deskripsi": hash_data[queue[0]]['deskripsi'],
                        "status": hash_data[queue[0]]['status'],
                        "prioritas": hash_data[queue[0]]['priority']
                    })

        # Mengurutkan hasil berdasarkan prioritas tertinggi
        sorted_result = sorted(result, key=lambda x: x["prioritas"], reverse=True)

        return sorted_result

    
    def get_hash_data(self, all_category=False):
        # Mengambil semua data dalam hash table
        all_data_hash = self.data_hash.get_all()
        
        # Mengembalikan semua data tanpa sortir
        if all_category:
            result = []
            for data in all_data_hash:
                data_result = {
                        "judul": list(data)[0],
                        "deskripsi": data[list(data)[0]]['deskripsi'],
                        "status": data[list(data)[0]]['status'],
                        "prioritas": data[list(data)[0]]['priority']
                    }
                result.append(data_result)
            return result

        # Memisahkan data ke dalam kategori
        category = {
            "Rencana": [],
            "Progres": [],
            "Selesai": []
        }

        for data in all_data_hash:
            status = data[list(data)[0]]['status']
            data_result = {
                        "judul": list(data)[0],
                        "deskripsi": data[list(data)[0]]['deskripsi'],
                        "status": data[list(data)[0]]['status'],
                        "prioritas": data[list(data)[0]]['priority']
                    }
            if status == 'rencana':
                category["Rencana"].append(data_result)
            elif status == 'progres':
                category["Progres"].append(data_result)
            elif status == 'selesai':
                category["Selesai"].append(data_result)

        return category
