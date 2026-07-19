
"""
rsa_visual.py

Interactive RSA visualization using Tkinter.
- Converts text message -> integer and back
- Generates RSA keypair (small demo sizes)
- Shows square-and-multiply steps for modular exponentiation
- Interactive stepping through encryption/decryption steps

Run: python rsa_visual.py

Requires only Python standard library.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import random
import math
import sys

# ----------------- Number / Text conversion -----------------

def text_to_int(s: str) -> int:
    # encode as UTF-8 bytes then big-endian integer
    b = s.encode('utf-8')
    return int.from_bytes(b, byteorder='big')

def int_to_text(n: int) -> str:
    if n == 0:
        return ''
    # detect length by bit-length -> bytes
    length = (n.bit_length() + 7) // 8
    b = n.to_bytes(length, byteorder='big')
    try:
        return b.decode('utf-8')
    except Exception:
        return '<invalid utf-8>'

# ----------------- Primality / key generation -----------------

def is_probable_prime(n: int, k: int = 8) -> bool:
    if n < 2:
        return False
    small_primes = [2,3,5,7,11,13,17,19,23,29]
    for p in small_primes:
        if n % p == 0:
            return n == p
    # write n-1 = 2^r * d
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randrange(2, n-1)
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        composite = True
        for _ in range(r-1):
            x = (x * x) % n
            if x == n-1:
                composite = False
                break
        if composite:
            return False
    return True

def generate_prime(bits: int) -> int:
    while True:
        p = random.getrandbits(bits) | (1 << (bits-1)) | 1
        if is_probable_prime(p):
            return p

def egcd(a: int, b: int):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def modinv(a: int, m: int) -> int:
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError('modular inverse does not exist')
    return x % m

def generate_rsa(bits: int = 32):
    # Very small by default for demonstration; increase for stronger keys
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    while q == p:
        q = generate_prime(bits // 2)
    n = p * q
    phi = (p-1)*(q-1)
    e = 65537
    if math.gcd(e, phi) != 1:
        # fallback find small odd e
        for cand in range(3, 1<<16, 2):
            if math.gcd(cand, phi) == 1:
                e = cand
                break
    d = modinv(e, phi)
    return {'p':p,'q':q,'n':n,'e':e,'d':d}

# ----------------- Modular exponentiation with steps -----------------

def modular_pow_steps(base: int, exponent: int, modulus: int):
    """Square-and-multiply with recorded steps for visualization.
    Returns list of step dicts with keys: step_index, bit, result, base_power
    """
    steps = []
    result = 1
    base_power = base % modulus
    binexp = bin(exponent)[2:]
    # process highest-to-lowest bit
    # Use left-to-right (MSB-first) square-and-multiply.
    # Keep base_power as the original base mod modulus for display (does not change in MSB algorithm).
    for i, ch in enumerate(binexp):
        bit = int(ch)
        steps.append({'phase':'inspect_bit', 'bit':bit, 'result':result, 'base_power':base_power, 'desc':f'Inspect bit {bit} (from MSB)'} )
        # square result
        result = (result * result) % modulus
        steps.append({'phase':'square', 'bit':bit, 'result':result, 'base_power':base_power, 'desc':'Square result'})
        if bit == 1:
            # multiply by base (original base mod modulus)
            result = (result * base_power) % modulus
            steps.append({'phase':'multiply', 'bit':bit, 'result':result, 'base_power':base_power, 'desc':'Multiply by base'})
        # For MSB-first we do not update base_power; append a no-op step for clarity
        steps.append({'phase':'base_power_unchanged', 'bit':bit, 'result':result, 'base_power':base_power, 'desc':'Base (a) unchanged in MSB algorithm'})
    # final result step
    steps.append({'phase':'final', 'bit':None, 'result':result, 'base_power':base_power, 'desc':'Final result'})
    return steps

# Note: Alternative variant processes bits LSB-first; above uses MSB-first but includes squaring before multiply to align with common algorithm.

# ----------------- GUI -----------------

class RSAVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('RSA Visualizer')
        self.geometry('900x600')
        self.resizable(True, True)

        # state
        self.keys = None
        self.steps = []
        self.step_index = 0
        self.current_operation = None  # 'encrypt' or 'decrypt'

        self._build_ui()

    def _build_ui(self):
        frm = ttk.Frame(self)
        frm.pack(fill='both', expand=True, padx=8, pady=8)

        left = ttk.Frame(frm)
        left.pack(side='left', fill='y')

        ttk.Label(left, text='Message:').pack(anchor='w')
        self.msg_entry = ttk.Entry(left, width=40)
        self.msg_entry.insert(0, 'Hello')
        self.msg_entry.pack(anchor='w', pady=4)

        ttk.Label(left, text='Key size (bits):').pack(anchor='w', pady=(8,0))
        self.bits_var = tk.IntVar(value=32)
        ttk.Spinbox(left, from_=16, to=1024, increment=8, textvariable=self.bits_var, width=10).pack(anchor='w')

        ttk.Button(left, text='Generate keys', command=self.generate_keys).pack(fill='x', pady=(8,2))
        ttk.Button(left, text='Encrypt', command=self.encrypt).pack(fill='x', pady=2)
        ttk.Button(left, text='Decrypt', command=self.decrypt).pack(fill='x', pady=2)

        stepfrm = ttk.Frame(left)
        stepfrm.pack(fill='x', pady=8)
        ttk.Button(stepfrm, text='Prev', command=self.prev_step).pack(side='left', fill='x', expand=True)
        ttk.Button(stepfrm, text='Next', command=self.next_step).pack(side='left', fill='x', expand=True)

        ttk.Label(left, text='Numeric values:').pack(anchor='w', pady=(8,0))
        self.values_text = scrolledtext.ScrolledText(left, width=40, height=15)
        self.values_text.pack(fill='both', expand=False)

        # Right side: steps and details
        right = ttk.Frame(frm)
        right.pack(side='left', fill='both', expand=True, padx=(8,0))

        ttk.Label(right, text='Square-and-Multiply Steps:').pack(anchor='w')
        self.steps_list = tk.Listbox(right)
        self.steps_list.pack(fill='both', expand=True)

        ttk.Label(right, text='Details:').pack(anchor='w', pady=(8,0))
        self.details = scrolledtext.ScrolledText(right, height=6)
        self.details.pack(fill='x', expand=False)

        # status bar
        self.status = ttk.Label(self, text='Ready', anchor='w')
        self.status.pack(fill='x', side='bottom')

    def _set_status(self, txt: str):
        self.status.config(text=txt)

    def generate_keys(self):
        bits = self.bits_var.get()
        if bits < 16:
            messagebox.showerror('Error', 'Key size too small')
            return
        self._set_status('Generating keys... (may take a while for large sizes)')
        self.update()
        try:
            self.keys = generate_rsa(bits)
            self._display_values('Keys generated')
            self._set_status('Keys generated')
        except Exception as e:
            messagebox.showerror('Error', str(e))
            self._set_status('Error')

    def _display_values(self, header=''):
        self.values_text.delete('1.0', tk.END)
        if header:
            self.values_text.insert(tk.END, header + '\n\n')
        if self.keys:
            k = self.keys
            self.values_text.insert(tk.END, f"p = {k['p']}\n")
            self.values_text.insert(tk.END, f"q = {k['q']}\n")
            self.values_text.insert(tk.END, f"n = {k['n']}\n")
            self.values_text.insert(tk.END, f"e = {k['e']}\n")
            self.values_text.insert(tk.END, f"d = {k['d']}\n")
            self.values_text.insert(tk.END, '\n')
        msg = self.msg_entry.get()
        m_int = text_to_int(msg)
        self.values_text.insert(tk.END, f"message (text) = {msg}\n")
        self.values_text.insert(tk.END, f"message (int)  = {m_int}\n")

    def encrypt(self):
        if not self.keys:
            messagebox.showinfo('Info', 'Generate keys first')
            return
        msg = self.msg_entry.get()
        m_int = text_to_int(msg)
        n = self.keys['n']
        if m_int >= n:
            messagebox.showwarning('Warning', 'Message integer >= n. Choose larger key or shorter message.')
            return
        e = self.keys['e']
        self.current_operation = 'encrypt'
        self.steps = modular_pow_steps(m_int, e, n)
        self.step_index = 0
        self._populate_steps_list()
        self._update_step_view()
        self._set_status('Encryption steps ready')

    def decrypt(self):
        if not self.keys:
            messagebox.showinfo('Info', 'Generate keys first')
            return
        # get ciphertext from the last final step if available
        n = self.keys['n']
        d = self.keys['d']
        # If we have just done encrypt, take its final result
        ciphertext = None
        if self.current_operation == 'encrypt' and self.steps:
            ciphertext = self.steps[-1]['result']
        else:
            # ask user for ciphertext as int via prompt
            ans = simpledialog.askstring('Ciphertext', 'Enter ciphertext integer to decrypt:')
            if ans is None:
                return
            try:
                ciphertext = int(ans.strip())
            except Exception:
                messagebox.showerror('Error', 'Invalid integer')
                return
        if ciphertext >= n:
            messagebox.showwarning('Warning', 'Ciphertext >= n; decryption will still compute but value seems invalid')
        self.current_operation = 'decrypt'
        self.steps = modular_pow_steps(ciphertext, d, n)
        self.step_index = 0
        self._populate_steps_list()
        self._update_step_view()
        self._set_status('Decryption steps ready')
        # show resulting plaintext text
        final = self.steps[-1]['result']
        try:
            plaintext = int_to_text(final)
        except Exception:
            plaintext = '<cannot decode>'
        self._display_values(f'Result after operation ({self.current_operation}):')
        self.values_text.insert(tk.END, f"final_int = {final}\n")
        self.values_text.insert(tk.END, f"decoded text = {plaintext}\n")

    def _populate_steps_list(self):
        self.steps_list.delete(0, tk.END)
        for i, s in enumerate(self.steps):
            txt = f"{i:03d}: {s['phase']} | bit={s['bit']} | result={s['result']} | base_power={s['base_power']}"
            self.steps_list.insert(tk.END, txt)

    def _update_step_view(self):
        if not self.steps:
            return
        i = max(0, min(self.step_index, len(self.steps)-1))
        self.steps_list.selection_clear(0, tk.END)
        self.steps_list.selection_set(i)
        self.steps_list.see(i)
        s = self.steps[i]
        self.details.delete('1.0', tk.END)
        self.details.insert(tk.END, f"Step {i}/{len(self.steps)-1}\n")
        self.details.insert(tk.END, f"Phase: {s['phase']}\n")
        self.details.insert(tk.END, f"Bit: {s['bit']}\n")
        self.details.insert(tk.END, f"Result: {s['result']}\n")
        self.details.insert(tk.END, f"Base power: {s['base_power']}\n")
        self.details.insert(tk.END, f"Desc: {s.get('desc','')}\n")

    def next_step(self):
        if not self.steps:
            return
        self.step_index = min(self.step_index + 1, len(self.steps)-1)
        self._update_step_view()

    def prev_step(self):
        if not self.steps:
            return
        self.step_index = max(self.step_index - 1, 0)
        self._update_step_view()


if __name__ == '__main__':
    app = RSAVisualizer()
    app.mainloop()