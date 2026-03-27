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
        if 'matrix_mode' not in st.session_state: st.session_state['matrix_mode'] = False
        if 'click_count' not in st.session_state: st.session_state['click_count'] = 0

        self.apply_styles()
        self.render_header()
        
        # Đầy đủ Menu như yêu cầu
        self.menu_options = [
            'Home', '--- SYSTEM ---', 'Tutorial', 'System Health',
            '--- MATH CORE ---', 'Pro Calculator', 'GCD & LCM', 'Linear Solver',
            'Quadratic Solver', 'Expand Expression', 'Factorize Polynomial',
            '--- NUMBER THEORY ---', 'Check Square Number', 'Check Prime Number',
            'Prime Factorization', 'Find All Divisors', 
            '--- CALCULUS ---', 'Derivative (df/dx)', 'Integral (∫dx)', 'Limits (x -> c)',
            '--- RANDOM TOOLS ---', 'Secure Password Gen', 'Random Color HEX',
            'Dice Roller (d6/d20)', 'Random List Picker', 'Integer RNG (Min/Max)'
        ]

        self.selection = st.sidebar.radio("APEX MAIN MENU", self.menu_options)
        self.router(self.selection)

    def apply_styles(self):
        is_matrix = st.session_state['matrix_mode']
        bg_main = "#000" if is_matrix else "#ffffff"
        text_color = "#0f0" if is_matrix else "#000"
        border_color = "#0f0" if is_matrix else "#808080"
        
        self.css = f"""
        <style>
            .stApp {{ background-color: {bg_main}; color: {text_color}; }}
            .apex-header {{ 
                background: {"linear-gradient(90deg, #003300, #000)" if is_matrix else "linear-gradient(90deg, #000040, #000080)"}; 
                color: #fff; padding: 10px; font-weight: bold; border: 2px inset #fff; 
                display: flex; justify-content: space-between;
            }}
            .res-box {{ 
                background: {"#000" if is_matrix else "#fdfdfd"}; 
                border: 2px inset {border_color}; padding: 15px; 
                color: {text_color}; font-family: 'Consolas', monospace; 
                font-size: 18px; margin-top: 20px; 
            }}
            .marquee-bar {{ background: #000; color: #0f0; font-family: 'Courier New'; font-size: 13px; border: 1px solid #fff; padding: 3px; }}
            .stButton>button[kind="secondary"] {{
                background: transparent !important; color: transparent !important; border: none !important;
                width: 10px !important; height: 10px !important; padding: 0 !important;
                min-width: 0 !important; margin-left: -10px !important;
            }}
        </style>
        """
        st.markdown(self.css, unsafe_allow_html=True)

    def render_header(self):
        st.markdown('<div class="apex-header"><span>ApexTools Pro</span><span>CORE: ONLINE</span></div>', unsafe_allow_html=True)
        st.markdown('<marquee class="marquee-bar">Math Engine: SymPy 1.12 | All modules active | "hack" to switch UI | Try "666" in Prime Check... </marquee>', unsafe_allow_html=True)

    def show_res(self, text):
        st.markdown(f'<div class="res-box"><b>Console_Output:></b><br>{text}</div>', unsafe_allow_html=True)

    def check_global_eggs(self, v):
        low_v = str(v).lower().strip()
        if low_v == "hack":
            st.session_state['matrix_mode'] = not st.session_state['matrix_mode']
            st.rerun()
            return True
        elif low_v == "coffee":
            self.show_res("☕ System energy stabilized.")
            return True
        return False

    def ui_home(self):
        st.title("🏠 Home")
        c1, c2 = st.columns([0.23, 0.77])
        with c1: st.write("Welcome back, Commander.")
        with c2:
            if st.button(" ", key="hidden_secret_btn"):
                st.session_state['click_count'] += 1
                if st.session_state['click_count'] >= 5:
                    st.balloons()
                    self.show_res("🎁 <b>ACCESS GRANTED:</b> System Core Unlocked.")
                else: st.toast(f"Probe: {st.session_state['click_count']}/5")
        st.info("ApexTools is a high-performance symbolic toolkit. Use the sidebar to navigate.")

    def router(self, v):
        if v.startswith('---'): return
        if v == 'Home': self.ui_home()
        # --- MATH CORE ---
        elif v == 'Pro Calculator': self.ui_generic("Calculator", "Enter expression:", "x**2 + 2*x + 1", self.logic_calc)
        elif v == 'GCD & LCM': self.ui_gcd_lcm()
        elif v == 'Linear Solver': self.ui_generic("Linear Solver", "Equation (e.g. 2*x - 4):", "2*x - 4", self.logic_solve)
        elif v == 'Quadratic Solver': self.ui_generic("Quadratic Solver", "Eq (a*x**2 + b*x + c):", "x**2 - 5*x + 6", self.logic_solve)
        elif v == 'Expand Expression': self.ui_generic("Expression Expander", "Input (e.g. (x+1)**3):", "(x+1)**3", self.logic_expand)
        elif v == 'Factorize Polynomial': self.ui_generic("Polynomial Factorizer", "Input:", "x**2 - 1", self.logic_factor)
        # --- NUMBER THEORY ---
        elif v == 'Check Square Number': self.ui_generic("Square Check", "Number:", "1024", self.logic_square)
        elif v == 'Check Prime Number': self.ui_generic("Prime Check", "Number:", "97", self.logic_prime)
        elif v == 'Prime Factorization': self.ui_generic("Prime Factorization", "Number:", "120", self.logic_prime_fact)
        elif v == 'Find All Divisors': self.ui_generic("Divisor Finder", "Number:", "36", self.logic_divisors)
        # --- CALCULUS ---
        elif v == 'Derivative (df/dx)': self.ui_generic("Derivative", "Expression (f(x)):", "sin(x) * x**2", self.logic_diff)
        elif v == 'Integral (∫dx)': self.ui_generic("Integral", "Expression (f(x)):", "exp(x) * cos(x)", self.logic_integ)
        elif v == 'Limits (x -> c)': self.ui_limit_ui()
        # --- RANDOM TOOLS ---
        elif v == 'Secure Password Gen': self.ui_generic("Password Generator", "Length:", "16", self.logic_pass)
        elif v == 'Random Color HEX': self.ui_color_tool()
        elif v == 'Dice Roller (d6/d20)': self.ui_dice_tool()
        elif v == 'Random List Picker': self.ui_generic("List Picker", "Items (comma separated):", "A, B, C", self.logic_picker)
        elif v == 'Integer RNG (Min/Max)': self.ui_rng_tool()
        elif v == 'System Health': self.ui_health()

    # --- UI HELPERS ---
    def ui_generic(self, name, label, placeholder, callback):
        st.subheader(name)
        inp = st.text_input(label, placeholder=placeholder, key=f"inp_{name}")
        if st.button(f"Compute {name}", key=f"btn_{name}"):
            callback(inp)

    # --- LOGIC MATH ---
    def logic_calc(self, v):
        if self.check_global_eggs(v): return
        try: self.show_res(f"Result: {simplify(v.replace('^','**'))}")
        except: self.show_res("Invalid Expression.")

    def logic_solve(self, v):
        try: self.show_res(f"Roots: {solve(v.replace('^','**'), x)}")
        except: self.show_res("Could not solve.")

    def logic_expand(self, v):
        try: self.show_res(f"Expanded: {expand(v.replace('^','**'))}")
        except: self.show_res("Error.")

    def logic_factor(self, v):
        try: self.show_res(f"Factored: {factor(v.replace('^','**'))}")
        except: self.show_res("Error.")

    def logic_diff(self, v):
        try: self.show_res(f"d/dx: {diff(v.replace('^','**'), x)}")
        except: self.show_res("Error in derivative.")

    def logic_integ(self, v):
        try: self.show_res(f"Integral: {integrate(v.replace('^','**'), x)} + C")
        except: self.show_res("Error in integration.")

    def ui_limit_ui(self):
        st.subheader("Limits")
        expr = st.text_input("f(x):", "sin(x)/x")
        c = st.text_input("Approaches (c):", "0")
        if st.button("Compute Limit"):
            try: self.show_res(f"Limit: {limit(expr.replace('^','**'), x, c)}")
            except: self.show_res("Error.")

    # --- LOGIC NUMBER THEORY ---
    def logic_prime(self, v):
        if self.check_global_eggs(v): return
        try:
            n = int(simplify(v.replace('^','**')))
            if n == 666: self.show_res("⚠️ Infernal number. Not Prime."); return
            self.show_res(f"Is Prime: {isprime(n)}")
        except: self.show_res("Input error.")

    def logic_prime_fact(self, v):
        try: self.show_res(f"Factors: {ntheory.primefactors(int(v))}")
        except: self.show_res("Error.")

    def logic_divisors(self, v):
        try: self.show_res(f"Divisors: {ntheory.divisors(int(v))}")
        except: self.show_res("Error.")

    def logic_square(self, v):
        try:
            n = int(simplify(v.replace('^','**')))
            res = n >= 0 and math.isqrt(n)**2 == n
            self.show_res(f"Perfect Square: {res}")
        except: self.show_res("Error.")

    # --- LOGIC RANDOM ---
    def logic_pass(self, v):
        try:
            length = int(v)
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            res = "".join(random.choice(chars) for _ in range(length))
            self.show_res(f"Secure Pass: <code>{res}</code>")
        except: self.show_res("Invalid length.")

    def logic_picker(self, v):
        items = [i.strip() for i in v.split(',') if i.strip()]
        if items: self.show_res(f"Picked: **{random.choice(items)}**")
        else: self.show_res("List is empty.")

    def ui_color_tool(self):
        st.subheader("Random Color HEX")
        if st.button("Generate Color"):
            color = "#%06x" % random.randint(0, 0xFFFFFF)
            self.show_res(f"HEX: <span style='color:{color}'>{color}</span>")

    def ui_dice_tool(self):
        st.subheader("Dice Roller")
        dtype = st.selectbox("Type:", ["d6", "d20"])
        if st.button("Roll"):
            res = random.randint(1, 6 if dtype=="d6" else 20)
            self.show_res(f"Result: 🎲 {res}")

    def ui_rng_tool(self):
        st.subheader("Integer RNG")
        min_v = st.number_input("Min:", value=1)
        max_v = st.number_input("Max:", value=100)
        if st.button("Generate"):
            self.show_res(f"Result: {random.randint(int(min_v), int(max_v))}")

    def ui_gcd_lcm(self):
        st.subheader("GCD & LCM")
        n1 = st.number_input("N1", value=1)
        n2 = st.number_input("N2", value=1)
        if st.button("Compute"):
            self.show_res(f"GCD: {gcd(int(n1), int(n2))}<br>LCM: {lcm(int(n1), int(n2))}")

    def ui_health(self):
        st.subheader("System Health")
        st.write("Calculus Engine: SymPy/SciPy")
        st.write("Status: Operational")

# Launch
ApexTools()
