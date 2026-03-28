import streamlit as st
import math
import random
import string
from sympy import symbols, diff, integrate, solve, simplify, isprime, ntheory, limit, expand, factor, oo, gcd, lcm

# --- CONFIG STREAMLIT ---
st.set_page_config(layout="wide", page_title="ApexTools Pro")

# --- SYMBOLIC ENGINE ---
x, y, z = symbols('x y z')

class ApexTools:
    def __init__(self):
        if 'click_count' not in st.session_state: st.session_state['click_count'] = 0

        self.apply_styles()
        self.render_header()
        
        self.menu_options = [
            'Home', '--- SYSTEM ---', 'Update Log', 'Tutorial', 'System Health',
            '--- MATH CORE ---', 'Pro Calculator', 'GCD & LCM', 'Linear Solver',
            'Quadratic Solver', 'Expand Expression', 'Factorize Polynomial',
            '--- NUMBER THEORY ---', 'Check Square Number', 'Check Prime Number',
            'Prime Factorization', 'Find All Divisors', '--- CALCULUS ---',
            'Derivative (df/dx)', 'Integral (∫dx)', 'Limits (x -> c)',
            '--- CONVERTERS ---', 'Length', 'Mass', 'Time', 'Power', 'Force', 'Voltage', 'Temperature',
            '--- RANDOM TOOLS ---', 'Secure Password Gen', 'Random Color HEX',
            'Dice Roller (d6/d20)', 'Random List Picker', 'Integer RNG (Min/Max)'
        ]

        self.selection = st.sidebar.radio("APEX MAIN MENU", self.menu_options)
        self.router(self.selection)

    def apply_styles(self):
        st.markdown("""
        <style>
            .stApp { background-color: #ffffff; color: #000; }
            .apex-header { 
                background: linear-gradient(90deg, #000040, #000080); 
                color: #fff; padding: 10px; font-weight: bold; border: 2px inset #fff; 
                display: flex; justify-content: space-between; 
            }
            .res-box { 
                background: #fdfdfd; border: 2px inset #808080; padding: 15px; 
                color: #000; font-family: 'Consolas', monospace; 
                font-size: 18px; margin-top: 20px; 
            }
            .marquee-bar { background: #000; color: #0f0; font-family: 'Courier New'; font-size: 13px; border: 1px solid #fff; padding: 3px; }
            .update-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            .update-table th, .update-table td { border: 1px solid #808080; padding: 10px; text-align: left; }
            .update-table th { background-color: #e0e0e0; }
        </style>
        """, unsafe_allow_html=True)

    def render_header(self):
        st.markdown('<div class="apex-header"><span>ApexTools Pro</span><span>CORE: ONLINE</span></div>', unsafe_allow_html=True)
        st.markdown('<marquee class="marquee-bar">System Ready | Engine: SymPy Symbolic | All tools operational | Versioning labels removed...</marquee>', unsafe_allow_html=True)

    def show_res(self, text):
        st.markdown(f'<div class="res-box"><b>ApexTools Log:</b><br>{text}</div>', unsafe_allow_html=True)

    def clean_input(self, text):
        return str(text).replace('^', '**')

    def ui_generic(self, name, placeholder, callback):
        st.subheader(name)
        inp = st.text_input("Input:", placeholder=placeholder, key=f"input_{name}")
        # Đảm bảo nút bấm luôn được render
        if st.button(f"Compute {name}", key=f"btn_{name}"):
            callback(inp)

    def router(self, v):
        if v.startswith('---'): return
        
        # --- SYSTEM ---
        if v == 'Home': self.ui_home()
        elif v == 'Update Log': self.ui_update_log()
        elif v == 'Tutorial': self.ui_manual()
        elif v == 'System Health': self.ui_health()
        
        # --- MATH CORE ---
        elif v == 'Pro Calculator': self.ui_generic("Calculator", "2^50 + 1", self.logic_calc)
        elif v == 'GCD & LCM': self.ui_gcd_lcm()
        elif v == 'Linear Solver': self.ui_generic("Linear Solver", "2*x - 10", self.logic_solve)
        elif v == 'Quadratic Solver': self.ui_generic("Quadratic Solver", "x^2 - 5*x + 6", self.logic_solve)
        elif v == 'Expand Expression': self.ui_generic("Expand", "(x+1)^2", self.logic_expand)
        elif v == 'Factorize Polynomial': self.ui_generic("Factorize", "x^2 - 1", self.logic_factorize)
        
        # --- NUMBER THEORY ---
        elif v == 'Check Square Number': self.ui_generic("Square Check", "2^50", self.logic_square)
        elif v == 'Check Prime Number': self.ui_generic("Prime Check", "2^31 - 1", self.logic_prime)
        elif v == 'Prime Factorization': self.ui_generic("Prime Factorization", "1024", self.logic_p_factors)
        elif v == 'Find All Divisors': self.ui_generic("Divisor Finder", "100", self.logic_divisors)
        
        # --- CALCULUS ---
        elif v == 'Derivative (df/dx)': self.ui_generic("Derivative", "x^3", self.logic_der)
        elif v == 'Integral (∫dx)': self.ui_generic("Integral", "sin(x)", self.logic_int)
        elif v == 'Limits (x -> c)': self.ui_limit()
        
        # --- RANDOM TOOLS ---
        elif v == 'Random List Picker': self.ui_generic("List Picker", "A, B, C", self.logic_picker)
        elif v == 'Secure Password Gen': self.ui_generic("Password Gen", "12", self.logic_pass)
        elif v == 'Random Color HEX': self.ui_color()
        elif v == 'Dice Roller (d6/d20)': self.ui_dice()
        elif v == 'Integer RNG (Min/Max)': self.ui_rng_int()

    # --- LOGIC HANDLERS ---
    def logic_calc(self, v): 
        try: self.show_res(f"Result: {simplify(self.clean_input(v))}")
        except Exception as e: self.show_res(f"Error: {e}")

    def logic_solve(self, v):
        try: self.show_res(f"Solution: {solve(self.clean_input(v), x)}")
        except Exception as e: self.show_res(f"Error: {e}")

    def logic_expand(self, v):
        try: self.show_res(f"Expanded: {expand(self.clean_input(v))}")
        except Exception as e: self.show_res(f"Error: {e}")

    def logic_factorize(self, v):
        try: self.show_res(f"Factored: {factor(self.clean_input(v))}")
        except Exception as e: self.show_res(f"Error: {e}")

    def logic_square(self, v):
        try:
            val = int(simplify(self.clean_input(v)))
            res = val >= 0 and math.isqrt(val)**2 == val
            self.show_res(f"Value: {val}<br><b>Is Perfect Square: {res}</b>")
        except Exception as e: self.show_res(f"Error: {e}")

    def logic_prime(self, v):
        try:
            val = int(simplify(self.clean_input(v)))
            self.show_res(f"Value: {val}<br><b>Is Prime: {isprime(val)}</b>")
        except Exception as e: self.show_res(f"Error: {e}")

    def logic_p_factors(self, v):
        try:
            val = int(simplify(self.clean_input(v)))
            d = ntheory.factorint(val)
            res = " * ".join([f"{p}^{e}" if e > 1 else str(p) for p, e in d.items()])
            self.show_res(f"Factorization: {res}")
        except Exception as e: self.show_res(f"Error: {e}")

    def logic_divisors(self, v):
        try: self.show_res(f"Divisors: {ntheory.divisors(int(simplify(self.clean_input(v))))}")
        except Exception as e: self.show_res(f"Error: {e}")

    def logic_der(self, v):
        try: self.show_res(f"Derivative: {diff(self.clean_input(v), x)}")
        except Exception as e: self.show_res(f"Error: {e}")

    def logic_int(self, v):
        try: self.show_res(f"Integral: {integrate(self.clean_input(v), x)} + C")
        except Exception as e: self.show_res(f"Error: {e}")

    # --- UI SPECIALS ---
    def ui_home(self):
        st.title("🏠 Home")
        st.markdown("""
        <div style="padding:20px; border:2px dashed #000080; background:#f9f9f9;">
            <h3>Welcome to ApexTools Pro</h3>
            <p>Your all-in-one symbolic math and utility suite is ready.</p>
        </div>
        """, unsafe_allow_html=True)

    def ui_update_log(self):
        st.subheader("📜 System Update Log")
        st.markdown("""
        <table class="update-table">
            <tr><th>Date</th><th>Category</th><th>Details</th></tr>
            <tr><td>2026-03-28</td><td><b>Bug Fix</b></td><td><b>CRITICAL:</b> Fixed missing Compute buttons in Math/Solver modules.</td></tr>
            <tr><td>2026-03-28</td><td><b>UI</b></td><td>Cleaned up redundant versioning text.</td></tr>
            <tr><td>2026-03-27</td><td><b>Engine</b></td><td>Enabled symbolic expression support for Prime/Square checks.</td></tr>
        </table>
        """, unsafe_allow_html=True)

    def ui_gcd_lcm(self):
        st.subheader("GCD & LCM")
        n1 = st.number_input("Number 1", value=1)
        n2 = st.number_input("Number 2", value=1)
        if st.button("Compute GCD & LCM"):
            self.show_res(f"GCD: {gcd(int(n1), int(n2))}<br>LCM: {lcm(int(n1), int(n2))}")

    def ui_limit(self):
        st.subheader("Limits")
        expr = st.text_input("Function:", "sin(x)/x")
        target = st.text_input("x approaches:", "0")
        if st.button("Compute Limit"):
            try: self.show_res(f"Limit: {limit(self.clean_input(expr), x, target)}")
            except Exception as e: self.show_res(f"Error: {e}")

    def ui_color(self):
        st.subheader("Color Generator")
        if st.button("Generate HEX"):
            c = "#%06x" % random.randint(0, 0xFFFFFF)
            self.show_res(f"HEX: <b style='color:{c}'>{c}</b>")

    def ui_dice(self):
        st.subheader("Dice Roller")
        d = st.selectbox("Dice:", ["d6", "d20"])
        if st.button("Roll Dice"):
            self.show_res(f"Rolled: {random.randint(1, 6 if d=='d6' else 20)}")

    def ui_rng_int(self):
        st.subheader("Integer RNG")
        mi = st.number_input("Min", value=1)
        ma = st.number_input("Max", value=100)
        if st.button("Generate Random"):
            self.show_res(f"Result: {random.randint(int(mi), int(ma))}")

    def logic_pass(self, v):
        try:
            p = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(int(v)))
            self.show_res(f"Password: <code>{p}</code>")
        except: self.show_res("Invalid Length.")

    def logic_picker(self, v):
        try: self.show_res(f"Picked: {random.choice([i.strip() for i in v.split(',')])}")
        except: self.show_res("Invalid List.")

    def ui_manual(self): st.info("Use '^' for powers (e.g., x^2). Always use '*' for multiplication (e.g., 2*x).")
    def ui_health(self): st.success("Symbolic Engine: Online | UI: Operational")

# Run
ApexTools()
