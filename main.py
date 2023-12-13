from datetime import datetime
import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import showerror, showwarning
from keys_generator import keys_generator
from Enum_Class import Direction
from make_session_key import generate_session_key
from elgamal import el_gamal as eg
from Blowfish import Blowfish as bw
from Blowfish_Mode import blowfish_mode as bw_mode
from Save_File import save_data_to_file
from IV import Create_IV
from Read_File import chunk_reader
import threading

# создаём рабочую папку клиента; предварительно удаляем с таким же именем, если есть
def create_client_work_folder():
    if clientNameEntry.get() == '':
        showwarning(title="Внимание!", message="Не указано имя клиента!")
    else:
        client_folder_name = os.path.join(os.getcwd(), clientNameEntry.get())
        if os.path.exists(client_folder_name):
            shutil.rmtree(client_folder_name)
            log_update("Удалена папка " + client_folder_name)
        os.mkdir(client_folder_name)
        log_update("Создана папка " + client_folder_name)

# создаём рабочую папку чата
def create_chat_folder():
    if clientNameEntry.get() == '':
        showwarning(title="Внимание!", message="Не указано имя клиента!")
        return False
    elif abonentNameEntry.get() == '':
        showwarning(title="Внимание!", message="Не указано имя абонента!")
        return False
    else:
        client_folder_name = clientNameEntry.get()
        abonent_folder_name = abonentNameEntry.get()
        if os.path.exists(client_folder_name + "_" + abonent_folder_name) or os.path.exists(abonent_folder_name + 
                                                                                            "_" + client_folder_name):
            log_update("Текущая папка чата существует")
        else:
            chatname = client_folder_name + "_" + abonent_folder_name
            os.mkdir(chatname)
            log_update("Создана папка " + client_folder_name + "_" + abonent_folder_name)
        return True

# открываем диалог выбора файла для шифрования и вставляем имя файла в текстовое поле
def select_enc_file_name():
    filepath = filedialog.askopenfilename()
    encFilePathEnt.insert(0, filepath)
    log_update("Для шифрования выбран файл " + filepath)


# открываем диалог выбора файла для дешифрования и вставляем имя файла в текстовое поле
def select_dec_file_name():
    filepath = filedialog.askopenfilename()
    decFilePathEnt.insert(0, filepath)
    log_update("Для дешифрации выбран файл " + filepath)

# меняем имя клиента в заголовке главного окна
def client_name_change(event):
    mainWindow.title("Имя клиента: " + clientNameEntry.get())

# записиываем в лог изменение имени клиента
def client_name_changed(event):
    if clientNameEntry.get() == abonentNameEntry.get():
        showerror(title="Ошибка!", message="У клиента и абонента должны быть разные имена!")
        clientNameEntry.delete(0, tk.END)
    else:
        if clientNameEntry.get() != "":
            log_update("Имя клиента изменено на " + clientNameEntry.get())

# записываем в лог изменение имени абонента
def abonent_name_changed(event):
    if abonentNameEntry.get() == clientNameEntry.get():
        showerror(title="Ошибка!", message="У абонента и клиента должны быть разные имена!")
        abonentNameEntry.delete(0, tk.END)
    else:
        if abonentNameEntry.get() != "":
            log_update("Имя абонента изменено на " + abonentNameEntry.get())

# записываем в лог изменение режима шифрования
def blowfish_encrypt_mode_changed(event):
    log_update("Выбран режим шифрования " + blowfishEncryptModeCombobox.get())

# записываем в лог изменение метода проверки простоты
def prime_test_changed(event):
    log_update("Выбран метод проверки простоты " + primeCheckMethodsCombobox.get())

# добавляем строку в окно лога
def log_update(message_string):
    current_time = datetime.now().strftime("%d.%m.%y %H:%M:%S ")
    logText.configure(state=tk.NORMAL)
    logText.insert("1.0", current_time + message_string + "\n")
    logText.configure(state=tk.DISABLED)

def choose_prime_method():
    if primeCheckMethodsCombobox.get() == "Ферма":
        return Direction.FERMA
    if primeCheckMethodsCombobox.get() == "Соловей-Штрассен":
        return Direction.SOLOWAY_STRASSEN    
    if primeCheckMethodsCombobox.get() == "Миллер-Рабин":
        return Direction.MILLER_RABIN
    
# генерируем ключи ассиметричного шифрования El Gamal
def generate_assync_keys():
        open_keys, client_close_key, abonent_key = keys_generator(choose_prime_method(), 64)
        p, g, y = open_keys[0], open_keys[1], open_keys[2]
        x = client_close_key
        k = abonent_key

        return p, g, y, x, k

# Метод расшаривания ключей между пользователями
def shared_keys():
    if create_chat_folder():
        p, g, y, x, k = generate_assync_keys()
        log_update("Сгенерирован открытый ключ ассиметричного шифрования " + str(p) + " " 
                   + str(g) + " " + str(y))

        abonent_folder_name = os.path.join(os.getcwd(), abonentNameEntry.get())
        client_folder_name = os.path.join(os.getcwd(), clientNameEntry.get())
        pk_file_path = os.path.join(abonent_folder_name, clientNameEntry.get() + ".PK")
        with open(pk_file_path, "w") as file:
            file.write(str(p) + " " +  str(g) + " " + str(y))
            file.close()
        log_update("Открыте ключи переданы пользователю: " + abonentNameEntry.get())

        sessionKey = generate_session_key(20)
        log_update("Сгенерирован сессионный ключ: " + sessionKey)

        sk_file_path = os.path.join(abonent_folder_name, clientNameEntry.get() + ".SK")
        with open(sk_file_path, "w") as file:
            file.write(sessionKey)
            file.close()
        
        client_encrypted_sk_file_path = os.path.join(os.path.join(client_folder_name,"encrypted_keys_" 
                                                        + abonentNameEntry.get() + ".SK"))
        client_sk_file_path = os.path.join(os.path.join(client_folder_name, abonentNameEntry.get() + ".SK"))
        eg.encrypt(p, g, y, k, sk_file_path, client_encrypted_sk_file_path)
        eg.decrypt(p, x, client_encrypted_sk_file_path, client_sk_file_path)
        os.remove(client_encrypted_sk_file_path)

        log_update("Получен секретный ключ: " + sessionKey)

def choose_mode_blowfish():
    if blowfishEncryptModeCombobox.get() == "ECB":
        return bw_mode.ECB
    if blowfishEncryptModeCombobox.get() == "CBC":
        return bw_mode.CBC
    if blowfishEncryptModeCombobox.get() == "OFB":
        return bw_mode.OFB
    if blowfishEncryptModeCombobox.get() == "CFB":
        return bw_mode.CFB

def find_format_file(path_format: str):
    for i in range(len(path_format) - 1, 0, -1):
        if path_format[i] == ".":
            path_format = path_format[i:]
            return path_format   

def encrypt_files_threaded():
    threading.Thread(target=encrypt_files).start()

def encrypt_files():
    file_to_encrypt = encFilePathEnt.get()

    if not(os.path.exists(file_to_encrypt)):
        showwarning("Не выбран файл", "Выберите файл для шифрования!")
    elif clientNameEntry.get() == "":
        showwarning("Имя пользователя не указано", "Укажите имя пользователя!")
    elif abonentNameEntry.get() == "":
        showwarning("Имя абонента не указано", "Укажите имя абонента!")
    else:
        with open(os.path.join(clientNameEntry.get(), abonentNameEntry.get() + ".SK"), "r") as file:
            session_key = file.read()
            file.close()

        format_file = find_format_file(encFilePathEnt.get())
 
        if os.path.exists(clientNameEntry.get() + "_" + abonentNameEntry.get()):
            enc_file_path = os.path.join(clientNameEntry.get() + "_" + abonentNameEntry.get(), 
                                         "enc_file_" + datetime.now().strftime("%d.%m.%y.%H.%M.%S") + format_file)
        else:
            enc_file_path = os.path.join(abonentNameEntry.get() +  "_" + clientNameEntry.get(), 
                                         "enc_file_" + datetime.now().strftime("%d.%m.%y.%H.%M.%S") + format_file)
        
        IV = Create_IV.generate_random_iv(4)
        encProgress["value"] = 0

        enc = bw(session_key, IV, choose_mode_blowfish())
        cypher_text = bytearray() 
        with open(file_to_encrypt, "rb") as file:
            total_size = os.path.getsize(file_to_encrypt)
            bytes_read = 0
            for chunk, is_last in chunk_reader(file, 4):
                if is_last:      
                    while len(chunk) < 4:
                        chunk += b'0'  
                IV, chunk = enc.encrypt(chunk)
                cypher_text.extend(chunk)
                
                # Для прогресс бара
                bytes_read += len(chunk)
                progress = int(bytes_read / total_size * 100)
                encProgress["value"] = progress
                encProgress.update()
        save_data_to_file(cypher_text, enc_file_path)                

        encProgress["value"] = 100

        IV_path = os.path.join(abonentNameEntry.get(), clientNameEntry.get() + ".IV")
        IV_path_self = os.path.join(clientNameEntry.get(), abonentNameEntry.get() + ".IV")
        
        save_data_to_file(IV, IV_path)
        save_data_to_file(IV, IV_path_self)

        log_update("Передан вектор инициализации (IV)")
        log_update("Зашифрованный файл находится в папке: " + enc_file_path)

def decrypt_files_threaded():
    threading.Thread(target=decrypt_files).start()

def decrypt_files():
    decProgress["value"] = 0
    file_to_decrypt = decFilePathEnt.get()
    if not(os.path.exists(file_to_decrypt)):
        showwarning("Не выбран файл", "Выберите файл для шифрования!")
    elif clientNameEntry.get() == "":
        showwarning("Имя пользователя не указано", "Укажите имя пользователя!")
    elif abonentNameEntry.get() == "":
        showwarning("Имя абонента не указано", "Укажите имя абонента!")
    else:
        with open(os.path.join(clientNameEntry.get(), abonentNameEntry.get() + ".SK"), "r") as file:
            session_key = file.read()
        file.close()

        IV_path = os.path.join(clientNameEntry.get(), abonentNameEntry.get() + ".IV")
        with open(IV_path, "rb") as file:
            for chunk, is_last in chunk_reader(file, 4):
                IV = chunk
        file.close()

        log_update("Получен вектор инициализации (IV)")
        format_file = find_format_file(decFilePathEnt.get()) 

        dec_file_path = os.path.join(clientNameEntry.get(), "dec_file_" + 
                                     datetime.now().strftime("%d.%m.%y.%H.%M.%S") + format_file)
        dec = bw(session_key, IV, choose_mode_blowfish())
        decrypt_text = bytearray()
        with open(file_to_decrypt, "rb") as file:
            total_size = os.path.getsize(file_to_decrypt)
            bytes_read = 0
            for chunk, is_last in chunk_reader(file, 4):
                chunk = dec.decrypt(chunk)
                if is_last:
                    chunk = bytearray(chunk)
                    chunk = chunk.replace(b'0', b'')
                decrypt_text.extend(chunk)

                bytes_read += len(chunk)
                progress = int(bytes_read / total_size * 100)
                decProgress["value"] = progress
                decProgress.update()
        save_data_to_file(decrypt_text, dec_file_path)
        decProgress["value"] = 100
        log_update("Расшифрованный файл находится в папке: " + dec_file_path)


# главное окно
mainWindow = tk.Tk()
mainWindow.title("Имя клиента:")
mainWindow.geometry("692x602")
mainWindow.resizable(False, False)

# поле ввода с именем клиента + кнопка создания рабочей папки клиента
tk.Label(text="Имя клиента ").grid(row=1, column=1, sticky=tk.E)
#
clientNameEntry = tk.Entry(width=60)
clientNameEntry.bind("<KeyRelease>", client_name_change)
clientNameEntry.bind("<FocusOut>", client_name_changed)
clientNameEntry.grid(row=1, column=2)
#
createClientWorkFolderBtn = ttk.Button(text="Создать папку", width=28, command=create_client_work_folder)
createClientWorkFolderBtn.grid(row=1, column=3, columnspan=2, sticky=tk.W)

createChatFolderBtn = ttk.Button(text="Начать", width=28, command=shared_keys)
createChatFolderBtn.grid(row=2, column=3, columnspan=2, sticky=tk.W)

# поле ввода с именем абонента
tk.Label(text="Имя абонента ").grid(row=2, column=1, sticky=tk.E)
#
abonentNameEntry = tk.Entry(width=60)
abonentNameEntry.bind("<FocusOut>", abonent_name_changed)
abonentNameEntry.grid(row=2, column=2)

# выпадающий список с режимами шифрования blowfish
tk.Label(text="Режим шифрования").grid(row=6, column=1, sticky=tk.E)
#
blowfishEncryptMode = ["ECB", "CBC", "CFB", "OFB"]
blowfishEncryptModeCombobox = ttk.Combobox(values=blowfishEncryptMode, width=57)
blowfishEncryptModeCombobox.insert(0, "ECB")  # значение при создании
blowfishEncryptModeCombobox.bind("<<ComboboxSelected>>", blowfish_encrypt_mode_changed)
blowfishEncryptModeCombobox.grid(row=6, column=2)

tk.Label(text="Метод проверки простоты").grid(row=7, column=1, sticky=tk.E)
primeCheckMethods = ["Ферма", "Соловей-Штрассен", "Миллер-Рабин"]
primeCheckMethodsCombobox = ttk.Combobox(values=primeCheckMethods, width=57)
primeCheckMethodsCombobox.insert(0, "Ферма")  # значение при создании
primeCheckMethodsCombobox.bind("<<ComboboxSelected>>", prime_test_changed)
primeCheckMethodsCombobox.grid(row=7, column=2)

# диалог выбора файла для шифрования
tk.Label(text="Файл для шифрования ").grid(row=8, column=1, sticky=tk.E)
#
encFilePathEnt = tk.Entry(width=60)
encFilePathEnt.grid(row=8, column=2, sticky=tk.W)
#
selectEncFileNameBtn = ttk.Button(text="...", command=select_enc_file_name)
selectEncFileNameBtn.grid(row=8, column=3, sticky=tk.W)
#
encFileBtn = ttk.Button(text="Зашифровать", width=15, command=encrypt_files_threaded)
encFileBtn.grid(row=8, column=4, sticky=tk.W)

# прогресс-бар шифрования
encProgress = ttk.Progressbar(orient="horizontal", length=688, value=0, mode="determinate")
encProgress.grid(row=9, column=1, columnspan=4)

# диалог выбора файла для дешифрования
tk.Label(text="Файл для дешифрации ").grid(row=10, column=1, sticky=tk.E)
#
decFilePathEnt = tk.Entry(width=60)
decFilePathEnt.grid(row=10, column=2, sticky=tk.W)
#
openDecFileBtn = ttk.Button(text="...", command=select_dec_file_name)
openDecFileBtn.grid(row=10, column=3, sticky=tk.W)
#
decFileBtn = ttk.Button(text="Дешифровать", width=15, command=decrypt_files_threaded)
decFileBtn.grid(row=10, column=4, sticky=tk.W)

# прогресс-бар дешифрования
decProgress = ttk.Progressbar(orient="horizontal", length=688, value=0)
decProgress.grid(row=11, column=1, columnspan=4)

# окно протокола
logText = ScrolledText(height=24, width=95, state=tk.DISABLED, font=("Courier New", 9))
logText.grid(row=12, column=1, columnspan=4)

log_update("Начало работы клиента")
log_update("Выбран режим шифрования ECB")

mainWindow.mainloop()