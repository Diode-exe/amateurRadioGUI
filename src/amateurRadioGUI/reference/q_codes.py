import tkinter as tk
from tkinter import ttk


class QCodes:
    """A window showing Q-codes in a searchable lookup table.

    The class builds a Toplevel window containing a search entry and a
    `ttk.Treeview` populated with Q-code/meaning pairs. Double-clicking a
    row opens a detail window with the full text.
    """

    def __init__(self, parent):
        """Create the Q-codes window and populate the lookup table.

        Args:
            parent: The application GUI instance that contains `root`.
        """
        self.parent = parent
        self.q_codes_window = tk.Toplevel(self.parent.root)
        self.q_codes_window.title("Q-Codes Reference")
        self.q_codes_window.geometry("600x600")
        self.q_codes_window.transient(self.parent.root)
        self.q_codes_window.lift()
        self.q_codes_window.focus_force()
        self.q_codes_window.bind("<Escape>", lambda event: self.q_codes_window.destroy())

        # Search box
        search_frame = tk.Frame(self.q_codes_window)
        search_frame.pack(fill="x", padx=8, pady=6)
        tk.Label(search_frame, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=(6, 0))
        search_entry.bind("<KeyRelease>", self._on_search)

        # Treeview as a lookup table
        columns = ("code", "meaning")
        self.tree = ttk.Treeview(self.q_codes_window, columns=columns, show="headings")
        self.tree.heading("code", text="Code")
        self.tree.heading("meaning", text="Meaning / Example")
        self.tree.column("code", width=90, anchor="center")
        self.tree.column("meaning", width=450, anchor="w")

        vsb = ttk.Scrollbar(self.q_codes_window, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=6)
        vsb.pack(side="right", fill="y", pady=6)

        # Double-click to view full text
        self.tree.bind("<Double-1>", self._on_double_click)

        self.q_codes = [
            'QRA What is the name (or call sign) of your station? - The name (or call sign) of my station is ____\n\n',
            'QRG Will you tell me my exact frequency (or that of ____)? - Your exact frequency (or that of ____ ) is ____ kHz (or MHz).\n\n',
            'QRH Does my frequency vary? - Your frequency varies.\n\n',
            'QRI How is the tone of my transmission? - The tone of your transmission is (1. Good; 2. Variable; 3. Bad)\n\n',
            'QRJ How many voice contacts do you want to make? - I want to make ____ voice contacts.\n\n',
            'QRK What is the readability of my signals (or those of ____)? - The readability of your signals (or those of ____) is ____ (1 to 5).\n\n',
            'QRL Are you busy? - I am busy (in contact with ____ ). Please do not interfere.\n\n',
            'QRM Do you have interference? - I have interference.\n\n',
            'QRN Are you troubled by static? - I am troubled by static.\n\n',
            'QRO Shall I increase power? - Increase power.\n\n',
            'QRP Shall I decrease power? - Decrease power.\n\n',
            'QRQ Shall I send faster? - Send faster (____wpm).\n\n',
            'QRS Shall I send more slowly? - Send more slowly (____wpm).\n\n',
            'QRT Shall I stop sending? - Stop sending.[25]Often heard colloquially as:I am suspending operation / shutting off the radio.\n\n',
            'QRU Have you anything for me? - I have ____ messages for you.\n\n',
            'QRV Are you ready? - I am ready.\n\n',
            'QRW Shall I inform ____ that you are calling (him) on ____ kHz (or MHz)? - Please inform ____ that I am calling (him) on ____ kHz (or MHz).\n\n',
            'QRX Shall I standby? / When will you call me again? - Please standby / I will call you again at ____ (hours) on ____ kHz (or MHz)\n\n',
            'QRZ Who is calling me? - You are being called by ____ on ____ kHz (or MHz)\n\n',
            'QSA What is the strength of my signals (or those of ____ )? - The strength of your signals (or those of ____) is ____ (1 to 5).\n\n',
            'QSB Are my signals fading? - Your signals are fading.\n\n',
            'QSD Is my keying defective? - Your keying is defective.\n\n',
            'QSG Shall I send ____ telegrams (messages) at a time? - Send ____ telegrams (messages) at a time.\n\n',
            'QSK Can you hear me between your signals? - I can hear you between my signals.\n\n',
            'QSL Can you acknowledge receipt? - I will acknowledge receipt.\n\n',
            'QSM Shall I repeat the last telegram (message) which I sent yo\n+\n+u, or some previous telegram (message)? - Repeat the last telegram (message) which you sent me (or telegram(s) / message(s) numbers(s) ____ ).\n\n',
            'QSN Did you hear me (or ____ (call sign)) on ____ kHz (or MHz)? - I did hear you (or ____ (call sign)) on ____ kHz (or MHz).\n\n',
            'QSO Can you communicate with ____ direct or by relay? - I can communicate with ____ direct (or by relay through ____ ).\n\n',
            'QSP Will you relay a message to ____\xa0? - I will relay a message to ____ .\n\n',
            'QSR Do you want me to repeat my call? - Please repeat your call; I did not hear you.\n\n',
            'QSS What working frequency will you use? - I will use the working frequency ____ kHz (or MHz).\n\n',
            'QST Should I repeat the prior message to all amateurs I contact? - Here follows a broadcast message to all amateurs.\n\n',
            'QSU Shall I send or reply on this frequency (or on ____ kHz (or MHz))? - Send or reply on this frequency (or on ____ kHz (or MHz)).\n\n',
            'QSW Will you send on this frequency (or on ____ kHz (or MHz))? - I am going to send on this frequency (or on ____ kHz (or MHz)).\n\n',
            'QSX Will you listen to ____ (call sign(s) on ____ kHz (or MHz))? - I am listening to ____ (call sign(s) on ____ kHz (or MHz))\n\n',
            'QSY Shall I change to transmission on another frequency? - Change to transmission on another frequency (or on ____ kHz (or MHz)).\n\n',
            'QSZ Shall I send each word or group more than once? - Send each word or group twice (or ____ times).\n\n',
            'QTA Shall I cancel telegram (message) number ____ as if it had not been sent? - Cancel telegram (message) number ____ as if it had not been sent.\n\n',
            'QTC How many telegrams (messages) have you to send? - I have ____ telegrams (messages) for you (or for ____ ).\n\n',
            'QTH What is your position in latitude and longitude? (or according to any other indication) - My position is ____ latitude ____ longitude.\n\n',
            'QTR What is the correct time? - The correct time is ____ hoursUTC.\n\n',
            'QTU At what times are you operating? - I am operating from ____ to ____ hours.\n\n',
            'QTX Will you keep your station open for further communication with me until further notice (or until ____ hours)? - I will keep my station open for further communication with you until further notice (or until ____ hours).\n\n',
            'QUA Have you news of ____ (call sign)? - Here is news of ____ (call sign).\n\n',
            'QUC What is the number (or other indication) of the last message you received from me (or from ____ (call sign))? - The number (or other indication) of the last message I received from you (or from ____ (call sign)) is ____.\n\n',
            'QUD Have you received the urgency signal sent by ____ (call sign of mobile station)? - I have received the urgency signal sent by ____ (call sign of mobile station) at ____ hours.\n\n',
            'QUE Can you speak in ____ (language) – with interpreter if necessary – if s\n+\no, on what frequencies? - I can speak in ____ (language) on ____ kHz (or MHz).\n\n',
            'QUF Have you received the distress signal sent by ____ (call sign of mobile station)? - I have received the distress signal sent by ____ (call sign of mobile station) at ____ hours.\n\n'
        ]

        # Parse into (code, meaning) tuples
        self.entries = []
        for item in self.q_codes:
            text = item.strip()
            if not text:
                continue
            parts = text.split(" ", 1)
            code = parts[0].strip()
            meaning = parts[1].strip() if len(parts) > 1 else ""
            self.entries.append((code, meaning))

        self._populate_tree(self.entries)

    def _populate_tree(self, entries):
        """Populate the `Treeview` with the provided entries.

        Each entry is a `(code, meaning)` tuple. Meanings are collapsed into
        a single-line preview to keep the table compact.

        Args:
            entries: Iterable of `(code, meaning)` tuples to insert.
        """
        self.tree.delete(*self.tree.get_children())
        for code, meaning in entries:
            preview = " ".join(meaning.splitlines())
            if len(preview) > 240:
                preview = preview[:237] + "..."
            self.tree.insert("", "end", values=(code, preview))

    def _on_search(self, event=None):
        """Filter the displayed entries using the search box content.

        Performs a case-insensitive substring match against the code and
        meaning fields and repopulates the tree with the filtered results.

        Args:
            event: Optional Tk event passed from the key release binding.
        """
        q = self.search_var.get().strip().lower()
        if not q:
            self._populate_tree(self.entries)
            return
        filtered = [e for e in self.entries if q in e[0].lower() or q in e[1].lower()]
        self._populate_tree(filtered)

    def _on_double_click(self, event):
        """Open a detail window showing the full meaning for the clicked row.

        The method identifies the row under the mouse `event`, looks up the
        full meaning from the stored entries, and opens a read-only `Text`
        window to present the full content.

        Args:
            event: Tk event from the double-click binding.
        """
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return
        code, preview = self.tree.item(item_id, "values")
        # Find full meaning
        full = next((m for c, m in self.entries if c == code), preview)
        detail = tk.Toplevel(self.q_codes_window)
        detail.title(code)
        detail.geometry("500x400")
        detail.bind("<Escape>", lambda e: detail.destroy())
        tk.Label(detail, text=code, font=("Arial", 14, "bold")).pack(padx=8, pady=(8, 0))
        txt = tk.Text(detail, wrap="word")
        txt.pack(fill="both", expand=True, padx=8, pady=8)
        txt.insert("1.0", full)
        txt.config(state="disabled")
