import tkinter as tk
from tkinter import messagebox, ttk

class AppGara:
    def __init__(self, root):
        self.root = root
        self.root.title("Virus Super Potente")
        self.root.geometry("600x550")
        self.root.configure(bg="#f0f0f0")
        
        self.partecipanti = []

        # stile di sto cazzo di programma
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=25)
        style.configure("TButton", font=("Segoe UI", 10))

        # titolo della sborra
        lbl_titolo = tk.Label(root, text="Programma Gara", font=("Segoe UI", 18, "bold"), bg="#f0f0f0", fg="#333")
        lbl_titolo.pack(pady=15)

        # frame input or something idk lmfao
        frame_input = tk.Frame(root, bg="#ffffff", padx=20, pady=20, highlightbackground="#cccccc", highlightthickness=1)
        frame_input.pack(padx=20, pady=10, fill="x")

        # tabella input :DDD
        tk.Label(frame_input, text="Nome:", bg="#ffffff", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.ent_nome = tk.Entry(frame_input, font=("Segoe UI", 10))
        self.ent_nome.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_input, text="Cognome:", bg="#ffffff", font=("Segoe UI", 10)).grid(row=0, column=2, sticky="w", pady=5)
        self.ent_cognome = tk.Entry(frame_input, font=("Segoe UI", 10))
        self.ent_cognome.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(frame_input, text="Tempo (s) o NA:", bg="#ffffff", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.ent_tempo = tk.Entry(frame_input, font=("Segoe UI", 10))
        self.ent_tempo.grid(row=1, column=1, padx=10, pady=5)

        self.btn_aggiungi = tk.Button(frame_input, text="AGGIUNGI ATLETA", bg="#4CAF50", fg="white", 
                                      font=("Segoe UI", 10, "bold"), command=self.aggiungi_atleta, relief="flat", cursor="hand2")
        self.btn_aggiungi.grid(row=1, column=2, columnspan=2, sticky="ew", padx=10, pady=5)

        # classificati, truth nuke?
        column_frame = tk.Frame(root, bg="#f0f0f0")
        column_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(column_frame, columns=("Pos", "Nome", "Cognome", "Tempo"), show='headings')
        self.tree.heading("Pos", text="POS.")
        self.tree.heading("Nome", text="NOME")
        self.tree.heading("Cognome", text="COGNOME")
        self.tree.heading("Tempo", text="TEMPO (s)")
        
        # pos colonne, super hard, super sophisticated 
        self.tree.column("Pos", width=50, anchor="center")
        self.tree.column("Tempo", width=100, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)

        # scrollbar se hai troppe persone lol
        scrollbar = ttk.Scrollbar(column_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # credit, sei libera di toglierlo, se sei capace ovviamente
        lbl_footer = tk.Label(root, text="Programmato da @nicotienne_ su IG", font=("Segoe UI", 8, "italic"), bg="#f0f0f0", fg="#888")
        lbl_footer.pack(side="bottom", anchor="e", padx=20, pady=5)

    def aggiungi_atleta(self):
        nome = self.ent_nome.get().strip()
        cognome = self.ent_cognome.get().strip()
        tempo_raw = self.ent_tempo.get().strip().upper()

        if not nome or not cognome or not tempo_raw:
            messagebox.showwarning("Attenzione", "Tutti i campi sono obbligatori!")
            return

        try:
            if tempo_raw == "NA":
                tempo_hex = "0xFFFFFF" # matematica, i think
            else:
                # conversione
                centesimi = int(float(tempo_raw.replace(',', '.')) * 100)
                tempo_hex = hex(centesimi)
            
            self.partecipanti.append({
                "nome": nome.capitalize(),
                "cognome": cognome.capitalize(),
                "tempo_hex": tempo_hex
            })
            
            self.aggiorna_classifica()
            self.pulisci_campi()

        except ValueError:
            messagebox.showerror("Errore", "Il tempo deve essere un numero o 'NA'")

    def aggiorna_classifica(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        # formula hex ordine importantteteeee
        self.partecipanti.sort(key=lambda x: int(x["tempo_hex"], 16))

        for i, p in enumerate(self.partecipanti):
            valore_int = int(p["tempo_hex"], 16)
            
            # convert esa > deca real time, importante
            if valore_int == 0xFFFFFF:
                tempo_display = "NA"
            else:
                tempo_display = f"{valore_int / 100:.2f}"

            self.tree.insert("", "end", values=(i + 1, p['nome'], p['cognome'], tempo_display))

    def pulisci_campi(self):
        self.ent_nome.delete(0, tk.END)
        self.ent_cognome.delete(0, tk.END)
        self.ent_tempo.delete(0, tk.END)
        self.ent_nome.focus()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGara(root)
    root.mainloop()