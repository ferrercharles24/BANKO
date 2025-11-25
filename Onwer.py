
import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Styling ----------
PRIMARY = "#4C6EF5"
ACCENT = "#22C55E"
BG = "#F4F6FB"
CARD = "#FFFFFF"
TEXT = "#0F172A"
SIDEBAR_BG = "#0F172A"
SIDEBAR_FG = "#FFFFFF"

def setup_styles():
    style = ttk.Style()
    style.theme_use("default")

    style.configure("TFrame", background=BG)
    style.configure("Topbar.TFrame", background=PRIMARY)
    style.configure("Sidebar.TFrame", background=SIDEBAR_BG)
    style.configure("Card.TFrame", background=CARD, relief="flat", borderwidth=0)
    style.configure("TLabel", background=BG, foreground=TEXT, font=("Inter", 11))
    style.configure("Header.TLabel", background=PRIMARY, foreground="white", font=("Inter", 14, "bold"))
    style.configure("Sidebar.TLabel", background=SIDEBAR_BG, foreground=SIDEBAR_FG, font=("Inter", 11))
    style.configure("TButton", font=("Inter", 10))
    style.map("Accent.TButton", background=[("active", "#1B9C4A"), ("!disabled", ACCENT)])

# ---------- UI Components ----------
class AdminUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BANKO")
        self.geometry("1280x800")
        self.configure(bg=BG)
        setup_styles()
        self.create_topbar()
        self.create_sidebar()
        self.create_main_area()
        self.load_demo_data()

    def create_topbar(self):
        top = ttk.Frame(self, style="Topbar.TFrame", height=60)
        top.pack(side="top", fill="x")

        # Left: App name / logo
        left = ttk.Frame(top, style="Topbar.TFrame")
        left.pack(side="left", padx=18)
        ttk.Label(left, text="🏦 BANKO", style="Header.TLabel").pack(side="left")

        # Center: Search
        center = ttk.Frame(top, style="Topbar.TFrame")
        center.pack(side="left", expand=True)
        search = ttk.Entry(center, width=50)
        search.pack(pady=12)
        search.insert(0, "")

        # Right: profile & actions
        right = ttk.Frame(top, style="Topbar.TFrame")
        right.pack(side="right", padx=18)
        ttk.Button(right, text="🔔", command=lambda: messagebox.showinfo("Notifications", "No new notifications")).pack(side="left", padx=6)
        ttk.Button(right, text="Profile ▾", command=self.show_profile).pack(side="left", padx=6)

    def create_sidebar(self):
        side = ttk.Frame(self, style="Sidebar.TFrame", width=220)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)

        # Admin info
        ttk.Label(side, text="Admin", style="Sidebar.TLabel").pack(pady=(18,6))
        ttk.Label(side, text="Charles", style="Sidebar.TLabel").pack()
        ttk.Separator(side, orient="horizontal").pack(fill="x", padx=12, pady=12)

        # Menu buttons
        self.menu_buttons = {}
        menu_items = [
            ("Dashboard", self.show_dashboard),
            ("User Account Management", self.show_customers),
            ("Transaction Monitoring", self.show_transactions),
            ("Loan Management", self.show_loans),
            ("System & Security Management", self.show_tickets),
            ("Financial Reporting", self.show_reports),
            ("Accout Control & Verification", self.show_settings),
        ]
        for txt, cmd in menu_items:
            b = ttk.Button(side, text=txt, style="TButton", command=cmd)
            b.pack(fill="x", padx=12, pady=6)
            self.menu_buttons[txt] = b

        ttk.Label(side, text="", style="Sidebar.TLabel").pack(expand=True)  # spacer
        ttk.Button(side, text="Logout", command=self.show_quit).pack(padx=12, pady=12)

    def create_main_area(self):
        self.main = ttk.Frame(self, style="TFrame")
        self.main.pack(side="left", fill="both", expand=True, padx=18, pady=12)

        # Dashboard view container (we'll swap views here)
        self.view_container = ttk.Frame(self.main, style="TFrame")
        self.view_container.pack(fill="both", expand=True)

        # Start with dashboard
        self.show_dashboard()

    # -------------------- Views --------------------
    def clear_view(self):
        for widget in self.view_container.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_view()
        # Top cards
        cards_row = ttk.Frame(self.view_container, style="TFrame")
        cards_row.pack(fill="x", pady=6)
        stats = [
            ("Total Customers", "1,234", "👥"),
            ("Total Balance", "₱ 12,345,678", "💰"),
            ("Loans Outstanding", "₱ 2,345,600", "📄"),
            ("Suspicious Tx (24h)", "2", "⚠️")
        ]
        for i, (title, value, icon) in enumerate(stats):
            card = ttk.Frame(cards_row, style="Card.TFrame", width=230, height=90)
            card.pack_propagate(False)
            card.pack(side="left", padx=10)
            ttk.Label(card, text=icon + "  " + title, font=("Inter", 10)).pack(anchor="w", pady=(12,0), padx=12)
            ttk.Label(card, text=value, font=("Inter", 16, "bold")).pack(anchor="w", padx=12, pady=(6,0))

        # Recent transactions table
        table_frame = ttk.Frame(self.view_container, style="TFrame")
        table_frame.pack(fill="both", expand=True, pady=10)

        ttk.Label(table_frame, text="Recent Transactions", font=("Inter", 12, "bold")).pack(anchor="w")

        columns = ("id", "customer", "type", "amount", "time")
        self.tx_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.tx_table.heading(col, text=col.capitalize())
            self.tx_table.column(col, anchor="center")
        self.tx_table.pack(fill="both", expand=True, pady=8)

        # Action buttons
        actions = ttk.Frame(self.view_container, style="TFrame")
        actions.pack(fill="x")
        ttk.Button(actions, text="Add Transaction", style="Accent.TButton", command=self.open_add_tx).pack(side="left")
        ttk.Button(actions, text="View All Customers", command=self.show_customers).pack(side="left", padx=8)

    def show_customers(self):
        self.clear_view()
        header = ttk.Frame(self.view_container)
        header.pack(fill="x")
        ttk.Label(header, text="Customers", font=("Inter", 14, "bold")).pack(side="left")
        ttk.Button(header, text="Create Customer", command=self.open_create_customer).pack(side="right")

        cols = ("id", "name", "age", "balance", "status")
        tree = ttk.Treeview(self.view_container, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c.capitalize())
            tree.column(c, anchor="center")
        tree.pack(fill="both", expand=True, pady=12)
        # populate demo data
        for cust in getattr(self, "_demo_customers", []):
            tree.insert("", "end", values=(cust["id"], cust["name"], cust["age"], f"₱{cust['balance']}", cust["status"]))

    def show_transactions(self):
        self.clear_view()
        ttk.Label(self.view_container, text="Transactions", font=("Inter", 14, "bold")).pack(anchor="w")
        cols = ("id", "customer", "type", "amount", "note", "time")
        tree = ttk.Treeview(self.view_container, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c.capitalize())
            tree.column(c, anchor="center")
        tree.pack(fill="both", expand=True, pady=12)
        for tx in getattr(self, "_demo_transactions", []):
            tree.insert("", "end", values=(tx["id"], tx["customer"], tx["type"], f"₱{tx['amount']}", tx["note"], tx["time"]))

    def show_loans(self):
        self.clear_view()
        ttk.Label(self.view_container, text="Loans", font=("Inter", 14, "bold")).pack(anchor="w")
        cols = ("id", "customer", "amount", "term", "status")
        tree = ttk.Treeview(self.view_container, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c.capitalize())
            tree.column(c, anchor="center")
        tree.pack(fill="both", expand=True, pady=12)

    def show_tickets(self):
        self.clear_view()
        ttk.Label(self.view_container, text="Support Tickets", font=("Inter", 14, "bold")).pack(anchor="w")
        cols = ("id", "customer", "title", "status", "created")
        tree = ttk.Treeview(self.view_container, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c.capitalize())
            tree.column(c, anchor="center")
        tree.pack(fill="both", expand=True, pady=12)

    def show_reports(self):
        self.clear_view()
        ttk.Label(self.view_container, text="Reports", font=("Inter", 14, "bold")).pack(anchor="w")
        ttk.Label(self.view_container, text="(Reports area - integrate your backend functions here)", font=("Inter", 10)).pack(anchor="w", pady=8)

    def show_settings(self):
        self.clear_view()
        ttk.Label(self.view_container, text="Settings", font=("Inter", 14, "bold")).pack(anchor="w")
        ttk.Label(self.view_container, text="(Add admin management, audit logs, and other settings here)", font=("Inter", 10)).pack(anchor="w", pady=8)

    # -------------------- Dialogs / Modals --------------------
    def open_create_customer(self):
        dlg = tk.Toplevel(self)
        dlg.title("Create Customer")
        dlg.geometry("360x260")
        ttk.Label(dlg, text="Name").pack(pady=(12,4))
        name_e = ttk.Entry(dlg)
        name_e.pack()
        ttk.Label(dlg, text="Age").pack(pady=(8,4))
        age_e = ttk.Entry(dlg)
        age_e.pack()
        def submit():
            name = name_e.get().strip()
            age = age_e.get().strip()
            if not name:
                messagebox.showerror("Error", "Name required")
                return
            new = {"id": gen_short_id("C"), "name": name, "age": age, "balance": 0.0, "status": "active"}
            self._demo_customers.append(new)
            messagebox.showinfo("Success", f"Customer {name} created")
            dlg.destroy()
        ttk.Button(dlg, text="Create", command=submit).pack(pady=12)

    def open_add_tx(self):
        dlg = tk.Toplevel(self)
        dlg.title("Add Transaction")
        dlg.geometry("420x320")
        ttk.Label(dlg, text="Customer ID").pack(pady=(12,4))
        cid_e = ttk.Entry(dlg)
        cid_e.pack()
        ttk.Label(dlg, text="Type (deposit/withdraw)").pack(pady=(8,4))
        type_e = ttk.Entry(dlg)
        type_e.pack()
        ttk.Label(dlg, text="Amount").pack(pady=(8,4))
        amt_e = ttk.Entry(dlg)
        amt_e.pack()
        ttk.Label(dlg, text="Note (optional)").pack(pady=(8,4))
        note_e = ttk.Entry(dlg)
        note_e.pack()

        def submit_tx():
            cid = cid_e.get().strip()
            ttype = type_e.get().strip().lower()
            try:
                amt = float(amt_e.get().strip())
            except:
                messagebox.showerror("Error", "Invalid amount")
                return
            tx = {"id": gen_short_id("T"), "customer": cid or "C000", "type": ttype, "amount": amt, "note": note_e.get().strip(), "time": "now"}
            self._demo_transactions.insert(0, tx)
            messagebox.showinfo("Success", "Transaction added")
            dlg.destroy()
        ttk.Button(dlg, text="Add Transaction", command=submit_tx).pack(pady=12)

    def show_profile(self):
        messagebox.showinfo("Profile", "Admin: Katie Richard\nRole: Superadmin")

    def show_quit(self):
        dlgg = tk.Toplevel(self)
        dlgg.title("Log-out")
        dlgg.geometry("260x150")
        ttk.Label(dlgg, text="Are you sure you want to Log-out?").pack(pady=(12,4))
        
        def yes():
            dlgg.quit()
        def no():
            dlgg.destroy()
        ttk.Button(dlgg, text="yes", command=yes).pack(pady=12,padx=2)
        ttk.Button(dlgg, text="no", command=no).pack(pady=12, padx=3)

    # -------------------- Demo Data --------------------
    def load_demo_data(self):
        # simple demo datasets to populate UI
        self._demo_customers = [
        ]
        self._demo_transactions = [
            ]
        # populate tx table if present
        if hasattr(self, "tx_table"):
            for tx in self._demo_transactions:
                self.tx_table.insert("", "end", values=(tx["id"], tx["customer"], tx["type"], f"₱{tx['amount']}", tx["time"]))

# ---------- small helpers ----------
import random, string
def gen_short_id(prefix="X"):
    return prefix + "".join(random.choices(string.ascii_uppercase + string.digits, k=4))

# ---------- Run ----------
if __name__ == "__main__":
    app = AdminUI()
    app.mainloop()