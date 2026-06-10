import tkinter as tk

class QCodes:
    def __init__(self, parent):
        self.parent = parent
        self.q_codes_window = None

    def open_q_codes(self):
        self.q_codes_window = tk.Toplevel(self.parent.root)
        self.q_codes_window.title("Q-Codes Reference")
        self.q_codes_window.geometry("400x600")
        self.q_codes_window.transient(self.parent.root)
        self.q_codes_window.lift()  # Bring the window to the front
        self.q_codes_window.focus_force()  # Focus on the new window
        self.q_codes_window.bind("<Escape>", lambda event: self.q_codes_window.destroy())  # Bind Escape key to close the window

        q_codes = {'QRA': 'What is the name (or call sign) of your station? - The name (or call sign) of my station is ____',
            'QRG': 'Will you tell me my exact frequency (or that of ____)? - Your exact frequency (or that of ____ ) is ____ kHz (or MHz).',
            'QRH': 'Does my frequency vary? - Your frequency varies.',
            'QRI': 'How is the tone of my transmission? - The tone of your transmission is (1. Good; 2. Variable; 3. Bad)',
            'QRJ': 'How many voice contacts do you want to make? - I want to make ____ voice contacts.',
            'QRK': 'What is the readability of my signals (or those of ____)? - The readability of your signals (or those of ____) is ____ (1 to 5).',
            'QRL': 'Are you busy? - I am busy (in contact with ____ ). Please do not interfere.',
            'QRM': 'Do you have interference? - I have interference.',
            'QRN': 'Are you troubled by static? - I am troubled by static.',
            'QRO': 'Shall I increase power? - Increase power.',
            'QRP': 'Shall I decrease power? - Decrease power.',
            'QRQ': 'Shall I send faster? - Send faster (____wpm).',
            'QRS': 'Shall I send more slowly? - Send more slowly (____wpm).',
            'QRT': 'Shall I stop sending? - Stop sending.[25]Often heard colloquially as:I am suspending operation / shutting off the radio.',
            'QRU': 'Have you anything for me? - I have ____ messages for you.',
            'QRV': 'Are you ready? - I am ready.',
            'QRW': 'Shall I inform ____ that you are calling (him) on ____ kHz (or MHz)? - Please inform ____ that I am calling (him) on ____ kHz (or MHz).',
            'QRX': 'Shall I standby? / When will you call me again? - Please standby / I will call you again at ____ (hours) on ____ kHz (or MHz)',
            'QRZ': 'Who is calling me? - You are being called by ____ on ____ kHz (or MHz)',
            'QSA': 'What is the strength of my signals (or those of ____ )? - The strength of your signals (or those of ____) is ____ (1 to 5).',
            'QSB': 'Are my signals fading? - Your signals are fading.',
            'QSD': 'Is my keying defective? - Your keying is defective.',
            'QSG': 'Shall I send ____ telegrams (messages) at a time? - Send ____ telegrams (messages) at a time.',
            'QSK': 'Can you hear me between your signals? - I can hear you between my signals.',
            'QSL': 'Can you acknowledge receipt? - I will acknowledge receipt.',
            'QSM': 'Shall I repeat the last telegram (message) which I sent you, or some previous telegram (message)? - Repeat the last telegram (message) which you sent me (or telegram(s) / message(s) numbers(s) ____ ).',
            'QSN': 'Did you hear me (or ____ (call sign)) on ____ kHz (or MHz)? - I did hear you (or ____ (call sign)) on ____ kHz (or MHz).',
            'QSO': 'Can you communicate with ____ direct or by relay? - I can communicate with ____ direct (or by relay through ____ ).',
            'QSP': 'Will you relay a message to ____ ? - I will relay a message to ____ .',
            'QSR': 'Do you want me to repeat my call? - Please repeat your call; I did not hear you.',
            'QSS': 'What working frequency will you use? - I will use the working frequency ____ kHz (or MHz).',
            'QST': 'Should I repeat the prior message to all amateurs I contact? - Here follows a broadcast message to all amateurs.',
            'QSU': 'Shall I send or reply on this frequency (or on ____ kHz (or MHz))? - Send or reply on this frequency (or on ____ kHz (or MHz)).',
            'QSW': 'Will you send on this frequency (or on ____ kHz (or MHz))? - I am going to send on this frequency (or on ____ kHz (or MHz)).',
            'QSX': 'Will you listen to ____ (call sign(s) on ____ kHz (or MHz))? - I am listening to ____ (call sign(s) on ____ kHz (or MHz))',
            'QSY': 'Shall I change to transmission on another frequency? - Change to transmission on another frequency (or on ____ kHz (or MHz)).',
            'QSZ': 'Shall I send each word or group more than once? - Send each word or group twice (or ____ times).',
            'QTA': 'Shall I cancel telegram (message) number ____ as if it had not been sent? - Cancel telegram (message) number ____ as if it had not been sent.',
            'QTC': 'How many telegrams (messages) have you to send? - I have ____ telegrams (messages) for you (or for ____ ).',
            'QTH': 'What is your position in latitude and longitude? (or according to any other indication) - My position is ____ latitude ____ longitude.',
            'QTR': 'What is the correct time? - The correct time is ____ hoursUTC.',
            'QTU': 'At what times are you operating? - I am operating from ____ to ____ hours.',
            'QTX': 'Will you keep your station open for further communication with me until further notice (or until ____ hours)? - I will keep my station open for further communication with you until further notice (or until ____ hours).',
            'QUA': 'Have you news of ____ (call sign)? - Here is news of ____ (call sign).',
            'QUC': 'What is the number (or other indication) of the last message you received from me (or from ____ (call sign))? - The number (or other indication) of the last message I received from you (or from ____ (call sign)) is ____.',
            'QUD': 'Have you received the urgency signal sent by ____ (call sign of mobile station)? - I have received the urgency signal sent by ____ (call sign of mobile station) at ____ hours.',
            'QUE': 'Can you speak in ____ (language) – with interpreter if necessary – if so, on what frequencies? - I can speak in ____ (language) on ____ kHz (or MHz).',
            'QUF': 'Have you received the distress signal sent by ____ (call sign of mobile station)? - I have received the distress signal sent by ____ (call sign of mobile station) at ____ hours.'}
