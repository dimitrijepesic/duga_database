import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

DB_NAME = "roba.db"

def initialize_database():
    """Kreira tabelu robe ako ne postoji sa novim kolonama."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roba (
            sifra TEXT PRIMARY KEY,
            naziv TEXT NOT NULL,
            prodajna_cena REAL NOT NULL,
            kupovna_cena REAL NOT NULL,
            dobavljac TEXT,
            telefon TEXT,
            kolicina INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# Funkcije za rad sa bazom podataka

def add_product_db(sifra, naziv, prodajna_cena, kupovna_cena, dobavljac, telefon, kolicina):
    """Dodaje proizvod u bazu."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO roba (sifra, naziv, prodajna_cena, kupovna_cena, dobavljac, telefon, kolicina)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (sifra, naziv, prodajna_cena, kupovna_cena, dobavljac, telefon, kolicina))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def get_all_products_db():
    """Vraća sve proizvode iz baze."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sifra, naziv, prodajna_cena, kupovna_cena, dobavljac, telefon, kolicina 
        FROM roba
    """)
    products = cursor.fetchall()
    conn.close()
    return products

def update_product_quantity_db(sifra, nova_kolicina):
    """Ažurira količinu proizvoda u bazi."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE roba SET kolicina = ? WHERE sifra = ?", (nova_kolicina, sifra))
    conn.commit()
    conn.close()

def buy_product_db(sifra, dodatna_kolicina):
    """Povećava količinu proizvoda (kupovina)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT kolicina FROM roba WHERE sifra = ?", (sifra,))
    result = cursor.fetchone()
    if result:
        nova_kolicina = result[0] + dodatna_kolicina
        cursor.execute("UPDATE roba SET kolicina = ? WHERE sifra = ?", (nova_kolicina, sifra))
        conn.commit()
        success = True
    else:
        success = False
    conn.close()
    return success

def sell_product_db(sifra, prodaja_kolicina):
    """Smanjuje količinu proizvoda (prodaja)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT kolicina FROM roba WHERE sifra = ?", (sifra,))
    result = cursor.fetchone()
    if result:
        if result[0] < prodaja_kolicina:
            success = False
        else:
            nova_kolicina = result[0] - prodaja_kolicina
            cursor.execute("UPDATE roba SET kolicina = ? WHERE sifra = ?", (nova_kolicina, sifra))
            conn.commit()
            success = True
    else:
        success = False
    conn.close()
    return success

def total_inventory_value_db():
    """Računa ukupnu vrednost robe (prodajna cena * količina za svaki proizvod)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT prodajna_cena, kolicina FROM roba")
    rows = cursor.fetchall()
    conn.close()
    ukupna_vrednost = sum(prodajna_cena * kolicina for prodajna_cena, kolicina in rows)
    return ukupna_vrednost

def update_product_db(sifra, naziv, prodajna_cena, kupovna_cena, dobavljac, telefon, kolicina):
    """Izmena podataka o proizvodu u bazi."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE roba
        SET naziv = ?, prodajna_cena = ?, kupovna_cena = ?, dobavljac = ?, telefon = ?, kolicina = ?
        WHERE sifra = ?
    """, (naziv, prodajna_cena, kupovna_cena, dobavljac, telefon, kolicina, sifra))
    conn.commit()
    conn.close()

def remove_product_db(sifra):
    """Uklanja proizvod iz baze."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM roba WHERE sifra = ?", (sifra,))
    conn.commit()
    conn.close()

# GUI funkcije

def dodaj_proizvod_gui():
    win = tk.Toplevel()
    win.title("Dodaj proizvod")
    
    tk.Label(win, text="Šifra:").grid(row=0, column=0, sticky="e")
    entry_sifra = tk.Entry(win)
    entry_sifra.grid(row=0, column=1)
    
    tk.Label(win, text="Naziv:").grid(row=1, column=0, sticky="e")
    entry_naziv = tk.Entry(win)
    entry_naziv.grid(row=1, column=1)
    
    tk.Label(win, text="Prodajna cena:").grid(row=2, column=0, sticky="e")
    entry_prodajna = tk.Entry(win)
    entry_prodajna.grid(row=2, column=1)
    
    tk.Label(win, text="Kupovna cena:").grid(row=3, column=0, sticky="e")
    entry_kupovna = tk.Entry(win)
    entry_kupovna.grid(row=3, column=1)
    
    tk.Label(win, text="Dobavljač:").grid(row=4, column=0, sticky="e")
    entry_dobavljac = tk.Entry(win)
    entry_dobavljac.grid(row=4, column=1)
    
    tk.Label(win, text="Telefon dobavljača:").grid(row=5, column=0, sticky="e")
    entry_telefon = tk.Entry(win)
    entry_telefon.grid(row=5, column=1)
    
    tk.Label(win, text="Količina:").grid(row=6, column=0, sticky="e")
    entry_kolicina = tk.Entry(win)
    entry_kolicina.grid(row=6, column=1)
    
    def submit():
        sifra = entry_sifra.get()
        naziv = entry_naziv.get()
        try:
            prodajna_cena = float(entry_prodajna.get())
        except ValueError:
            messagebox.showerror("Greška", "Nevažeća prodajna cena.")
            return
        try:
            kupovna_cena = float(entry_kupovna.get())
        except ValueError:
            messagebox.showerror("Greška", "Nevažeća kupovna cena.")
            return
        dobavljac = entry_dobavljac.get()
        telefon = entry_telefon.get()
        try:
            kolicina = int(entry_kolicina.get())
        except ValueError:
            messagebox.showerror("Greška", "Nevažeća količina.")
            return
        if add_product_db(sifra, naziv, prodajna_cena, kupovna_cena, dobavljac, telefon, kolicina):
            messagebox.showinfo("Uspeh", "Proizvod dodat uspešno.")
            win.destroy()
        else:
            messagebox.showerror("Greška", "Proizvod sa tom šifrom već postoji.")
    
    tk.Button(win, text="Dodaj", command=submit).grid(row=7, column=0, columnspan=2)

def prikazi_proizvode_gui():
    win = tk.Toplevel()
    win.title("Prikaz proizvoda")
    
    # Postavljanje stila za Treeview
    style = ttk.Style(win)
    style.theme_use("clam")
    style.configure("Treeview",
                    background="white",
                    fieldbackground="white",
                    foreground="black",
                    borderwidth=1,
                    relief="solid")
    style.configure("Treeview.Heading",
                    background="#A9A9A9",  # tamnija pozadina zaglavlja
                    foreground="black",
                    borderwidth=1,
                    relief="solid")
    
    # Definišemo kolone, uključujući i maržu
    columns = ("sifra", "naziv", "prodajna_cena", "kupovna_cena", "marza", "dobavljac", "telefon", "kolicina")
    tree = ttk.Treeview(win, columns=columns, show="headings")
    
    # Definisanje zaglavlja kolona
    tree.heading("sifra", text="Šifra")
    tree.heading("naziv", text="Naziv")
    tree.heading("prodajna_cena", text="Prodajna cena")
    tree.heading("kupovna_cena", text="Kupovna cena")
    tree.heading("marza", text="Marža")
    tree.heading("dobavljac", text="Dobavljač")
    tree.heading("telefon", text="Telefon")
    tree.heading("kolicina", text="Količina")
    
    # Podešavanje širina kolona i poravnanje svih ćelija levo
    tree.column("sifra", width=80, anchor="w")
    tree.column("naziv", width=200, anchor="w")
    tree.column("prodajna_cena", width=120, anchor="w")
    tree.column("kupovna_cena", width=120, anchor="w")
    tree.column("marza", width=100, anchor="w")
    tree.column("dobavljac", width=150, anchor="w")
    tree.column("telefon", width=120, anchor="w")
    tree.column("kolicina", width=80, anchor="w")
    
    # Učitavanje podataka iz baze i unos u Treeview
    products = get_all_products_db()
    for p in products:
        # p = (sifra, naziv, prodajna_cena, kupovna_cena, dobavljac, telefon, kolicina)
        marza = p[2] - p[3]  # Marža = prodajna cena - kupovna cena
        tree.insert("", tk.END, values=(p[0], p[1], f"{p[2]:.2f}", f"{p[3]:.2f}", f"{marza:.2f}", p[4], p[5], p[6]))
    
    tree.pack(expand=True, fill="both")
    
    # Dodavanje vertikalnog scrollbar-a
    scrollbar = tk.Scrollbar(win, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

def popis_gui():
    win = tk.Toplevel()
    win.title("Popis - Resetovanje zaliha")
    
    products = get_all_products_db()
    entries = {}
    row = 0
    if not products:
        tk.Label(win, text="Nema proizvoda u bazi.").grid(row=row, column=0)
        return
    
    tk.Label(win, text="Šifra").grid(row=row, column=0)
    tk.Label(win, text="Naziv").grid(row=row, column=1)
    tk.Label(win, text="Nova količina").grid(row=row, column=2)
    row += 1
    
    for p in products:
        sifra, naziv, _, _, _, _, _ = p
        tk.Label(win, text=sifra).grid(row=row, column=0)
        tk.Label(win, text=naziv).grid(row=row, column=1)
        entry = tk.Entry(win)
        entry.grid(row=row, column=2)
        entries[sifra] = entry
        row += 1
    
    def sacuvaj_popis():
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE roba SET kolicina = 0")
        conn.commit()
        for sifra, entry in entries.items():
            try:
                nova_kolicina = int(entry.get())
            except ValueError:
                messagebox.showerror("Greška", f"Nevažeća količina za proizvod sa šifrom {sifra}.")
                conn.close()
                return
            cursor.execute("UPDATE roba SET kolicina = ? WHERE sifra = ?", (nova_kolicina, sifra))
        conn.commit()
        conn.close()
        messagebox.showinfo("Uspeh", "Popis je uspešno sačuvan.")
        win.destroy()
    
    tk.Button(win, text="Sačuvaj popis", command=sacuvaj_popis).grid(row=row, column=0, columnspan=3)

def kupi_proizvod_gui():
    win = tk.Toplevel()
    win.title("Kupovina proizvoda")
    
    tk.Label(win, text="Šifra:").grid(row=0, column=0, sticky="e")
    entry_sifra = tk.Entry(win)
    entry_sifra.grid(row=0, column=1)
    
    tk.Label(win, text="Količina za kupovinu:").grid(row=1, column=0, sticky="e")
    entry_kolicina = tk.Entry(win)
    entry_kolicina.grid(row=1, column=1)
    
    def submit():
        sifra = entry_sifra.get()
        try:
            dodatna_kolicina = int(entry_kolicina.get())
        except ValueError:
            messagebox.showerror("Greška", "Nevažeća količina.")
            return
        if buy_product_db(sifra, dodatna_kolicina):
            messagebox.showinfo("Uspeh", "Kupovina je uspešno zabeležena.")
            win.destroy()
        else:
            messagebox.showerror("Greška", "Proizvod nije pronađen.")
    
    tk.Button(win, text="Kupi", command=submit).grid(row=2, column=0, columnspan=2)

def prodaj_proizvod_gui():
    win = tk.Toplevel()
    win.title("Prodaja proizvoda")
    
    tk.Label(win, text="Šifra:").grid(row=0, column=0, sticky="e")
    entry_sifra = tk.Entry(win)
    entry_sifra.grid(row=0, column=1)
    
    tk.Label(win, text="Količina za prodaju:").grid(row=1, column=0, sticky="e")
    entry_kolicina = tk.Entry(win)
    entry_kolicina.grid(row=1, column=1)
    
    def submit():
        sifra = entry_sifra.get()
        try:
            prodaja_kolicina = int(entry_kolicina.get())
        except ValueError:
            messagebox.showerror("Greška", "Nevažeća količina.")
            return
        if sell_product_db(sifra, prodaja_kolicina):
            messagebox.showinfo("Uspeh", "Prodaja je uspešno zabeležena.")
            win.destroy()
        else:
            messagebox.showerror("Greška", "Proizvod nije pronađen ili nema dovoljno robe.")
    
    tk.Button(win, text="Prodaj", command=submit).grid(row=2, column=0, columnspan=2)

def ukupna_vrednost_roba_gui():
    ukupna = total_inventory_value_db()
    messagebox.showinfo("Ukupna vrednost", f"Ukupna vrednost robe: {ukupna:.2f}")

def izmeni_i_obrisi_proizvod_gui():
    """Pretraga proizvoda po šifri i mogućnost izmene svih podataka ili brisanja artikla."""
    win = tk.Toplevel()
    win.title("Izmena/Brisanje proizvoda")
    
    tk.Label(win, text="Unesite šifru proizvoda:").grid(row=0, column=0, sticky="e")
    entry_search = tk.Entry(win)
    entry_search.grid(row=0, column=1)
    
    def search():
        sifra = entry_search.get()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sifra, naziv, prodajna_cena, kupovna_cena, dobavljac, telefon, kolicina
            FROM roba WHERE sifra = ?
        """, (sifra,))
        product = cursor.fetchone()
        conn.close()
        if product:
            # Kreiramo formu za izmenu
            edit_frame = tk.Frame(win)
            edit_frame.grid(row=2, column=0, columnspan=2, pady=10)
            
            tk.Label(edit_frame, text="Naziv:").grid(row=0, column=0, sticky="e")
            entry_naziv = tk.Entry(edit_frame)
            entry_naziv.grid(row=0, column=1)
            entry_naziv.insert(0, product[1])
            
            tk.Label(edit_frame, text="Prodajna cena:").grid(row=1, column=0, sticky="e")
            entry_prodajna = tk.Entry(edit_frame)
            entry_prodajna.grid(row=1, column=1)
            entry_prodajna.insert(0, str(product[2]))
            
            tk.Label(edit_frame, text="Kupovna cena:").grid(row=2, column=0, sticky="e")
            entry_kupovna = tk.Entry(edit_frame)
            entry_kupovna.grid(row=2, column=1)
            entry_kupovna.insert(0, str(product[3]))
            
            tk.Label(edit_frame, text="Dobavljač:").grid(row=3, column=0, sticky="e")
            entry_dobavljac = tk.Entry(edit_frame)
            entry_dobavljac.grid(row=3, column=1)
            entry_dobavljac.insert(0, product[4])
            
            tk.Label(edit_frame, text="Telefon:").grid(row=4, column=0, sticky="e")
            entry_telefon = tk.Entry(edit_frame)
            entry_telefon.grid(row=4, column=1)
            entry_telefon.insert(0, product[5])
            
            tk.Label(edit_frame, text="Količina:").grid(row=5, column=0, sticky="e")
            entry_kolicina = tk.Entry(edit_frame)
            entry_kolicina.grid(row=5, column=1)
            entry_kolicina.insert(0, str(product[6]))
            
            def update():
                try:
                    nova_prodajna = float(entry_prodajna.get())
                    nova_kupovna = float(entry_kupovna.get())
                    nova_kolicina = int(entry_kolicina.get())
                except ValueError:
                    messagebox.showerror("Greška", "Nevažeći unos za cenu ili količinu.")
                    return
                novo_naziv = entry_naziv.get()
                novi_dobavljac = entry_dobavljac.get()
                novi_telefon = entry_telefon.get()
                update_product_db(sifra, novo_naziv, nova_prodajna, nova_kupovna, novi_dobavljac, novi_telefon, nova_kolicina)
                messagebox.showinfo("Uspeh", "Proizvod izmenjen uspešno.")
                win.destroy()
            
            def remove():
                if messagebox.askyesno("Potvrda", "Da li ste sigurni da želite da uklonite ovaj proizvod?"):
                    remove_product_db(sifra)
                    messagebox.showinfo("Uspeh", "Proizvod uklonjen.")
                    win.destroy()
            
            tk.Button(edit_frame, text="Sačuvaj izmene", command=update).grid(row=6, column=0, pady=5)
            tk.Button(edit_frame, text="Obriši proizvod", command=remove).grid(row=6, column=1, pady=5)
        else:
            messagebox.showerror("Greška", "Proizvod nije pronađen.")
    
    tk.Button(win, text="Pretraži", command=search).grid(row=1, column=0, columnspan=2, pady=5)

def main_gui():
    root = tk.Tk()
    root.title("Praćenje robe")
    
    tk.Button(root, text="Dodaj proizvod", width=30, command=dodaj_proizvod_gui).pack(pady=5)
    tk.Button(root, text="Prikaži proizvode", width=30, command=prikazi_proizvode_gui).pack(pady=5)
    tk.Button(root, text="Popis (resetovanje zaliha)", width=30, command=popis_gui).pack(pady=5)
    tk.Button(root, text="Kupovina proizvoda", width=30, command=kupi_proizvod_gui).pack(pady=5)
    tk.Button(root, text="Prodaja proizvoda", width=30, command=prodaj_proizvod_gui).pack(pady=5)
    tk.Button(root, text="Ukupna vrednost robe", width=30, command=ukupna_vrednost_roba_gui).pack(pady=5)
    tk.Button(root, text="Izmena/Brisanje proizvoda", width=30, command=izmeni_i_obrisi_proizvod_gui).pack(pady=5)
    tk.Button(root, text="Izlaz", width=30, command=root.destroy).pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    initialize_database()
    main_gui()