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
        # State bí mật
        if 'click_count' not in st.session_state: st.session_state['click_count'] = 0
        if 'matrix_mode' not in st.session_state: st.session_state['matrix_mode'] = False

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
        # Matrix Mode logic
        bg = "#000000" if st.session_state['matrix_mode'] else "#ffffff"
        fg = "#00ff00" if st.session_state['matrix_mode'] else "#000"
        border = "1px solid #00ff00" if st.session_state['matrix_mode'] else "2px inset #808080"
        
        st.markdown(f"""
        <style>
            .stApp {{ background-color: {bg}; color: {fg}; }}
            .apex-header {{ 
                background: linear-gradient(90deg, #000040, #000080); 
                color: #fff; padding: 10px; font-weight: bold; border: 2px inset #fff; 
                display: flex; justify-content: space-between; 
            }}
            .res-box {{ 
                background: {bg}; border: {border}; padding: 15px; 
                color: {fg}; font-family: 'Consolas', monospace; 
                font-size: 18px; margin-top: 20px; 
            }}
            .marquee-bar {{ background: #000; color: #0f0; font-family: 'Courier New'; font-size: 13px; border: 1px solid #fff; padding: 3px; }}
            .update-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            .update-table th, .update-table td {{ border: 1px solid #808080; padding: 10px; text-align: left; }}
            
            /* NÚT COMPUTE HIỆN HỮU */
            .stButton > button {{
                width: 100%;
                background-color: #f0f0f0;
                color: black;
                border: 2px outset #808080;
            }}

            /* CHỈ GIẤU NÚT CÓ KEY LÀ EGG */
            div[data-testid="stBaseButton-secondary"] {{
                background: transparent !important;
                border: none !important;
                color: transparent !important;
                height: 1px !important;
                width: 1px !important;
                padding: 0 !important;
            }}
        </style>
        """, unsafe_allow_html=True)

    def render_header(self):
        st.markdown('<div class="apex-header"><span>ApexTools Pro</span><span>CORE: ONLINE</span></div>', unsafe_allow_html=True)
        st.markdown('<marquee class="marquee-bar">System Ready | Engine: SymPy | UI Stable | Core Protocols Online...</marquee>', unsafe_allow_html=True)

    def show_res(self, text):
        st.markdown(f'<div class="res-box"><b>ApexTools Log:</b><br>{text}</div>', unsafe_allow_html=True)

    def clean_input(self, text):
        return str(text).replace('^', '**')

    def ui_generic(self, name, label, placeholder, callback):
        st.subheader(name)
        inp = st.text_input(label, placeholder=placeholder, key=f"inp_{name}")
        
        if inp.lower() == "matrix": 
            st.session_state['matrix_mode'] = True
            st.rerun()
        if inp.lower() == "exit":
            st.session_state['matrix_mode'] = False
            st.rerun()

        if st.button(f"Compute {name}", key=f"btn_{name}"):
            callback(inp)

    def router(self, v):
        if v.startswith('---'): return
        if v == 'Home': self.ui_home()
        elif v == 'Update Log': self.ui_update_log()
        elif v == 'Tutorial': self.ui_tutorial()
        elif v == 'System Health': self.ui_health()
        
        elif v == 'Pro Calculator': self.ui_generic("Calculator", "Expression:", "2^50 + 1", self.logic_calc)
        elif v == 'GCD & LCM': self.ui_gcd_lcm()
        elif v == 'Linear Solver': self.ui_generic("Linear Solver", "Equation (f(x)=0):", "2*x - 10", self.logic_solve)
        elif v == 'Quadratic Solver': self.ui_generic("Quadratic Solver", "Equation:", "x^2 - 5*x + 6", self.logic_solve)
        elif v == 'Expand Expression': self.ui_generic("Expand", "Input:", "(x+1)^3", self.logic_expand)
        elif v == 'Factorize Polynomial': self.ui_generic("Factorize", "Input:", "x^2 - 1", self.logic_factor)
        
        elif v == 'Check Square Number': self.ui_generic("Square Check", "Value:", "2^10", self.logic_square)
        elif v == 'Check Prime Number': self.ui_generic("Prime Check", "Value:", "97", self.logic_prime)
        elif v == 'Prime Factorization': self.ui_generic("Prime Factorization", "Value:", "120", self.logic_p_factors)
        elif v == 'Find All Divisors': self.ui_generic("Divisor Finder", "Value:", "100", self.logic_divisors)
        
        elif v == 'Derivative (df/dx)': self.ui_generic("Derivative", "f(x):", "x^3", self.logic_der)
        elif v == 'Integral (∫dx)': self.ui_generic("Integral", "f(x):", "sin(x)", self.logic_int)
        elif v == 'Limits (x -> c)': self.ui_limit_ui()

        elif v == 'Random List Picker': self.ui_generic("List Picker", "Items:", "A, B, C", self.logic_picker)
        elif v == 'Secure Password Gen': self.ui_generic("Password Gen", "Length:", "12", self.logic_pass)
        elif v == 'Random Color HEX': self.ui_color_tool()
        elif v == 'Dice Roller (d6/d20)': self.ui_dice_tool()
        elif v == 'Integer RNG (Min/Max)': self.ui_rng_tool()
        
        elif v in ['Length', 'Mass', 'Time', 'Power', 'Force', 'Voltage', 'Temperature']:
            self.ui_generic(v, "Value to convert:", "100", self.logic_calc)

    def logic_calc(self, v):
        try: self.show_res(f"Result: {simplify(self.clean_input(v))}")
        except: self.show_res("Invalid Syntax.")

    def logic_square(self, v):
        try:
            n = int(simplify(self.clean_input(v)))
            res = n >= 0 and math.isqrt(n)**2 == n
            self.show_res(f"Value: {n}<br>Square Number: {res}")
        except: self.show_res("Integer required.")

    def logic_prime(self, v):
        try: self.show_res(f"Is Prime: {isprime(int(simplify(self.clean_input(v))))}")
        except: self.show_res("Error.")

    def logic_p_factors(self, v):
        try:
            n = int(simplify(self.clean_input(v)))
            f = ntheory.factorint(n)
            res = " * ".join([f"{p}^{e}" if e>1 else str(p) for p,e in f.items()])
            self.show_res(f"Result: {res}")
        except: self.show_res("Error.")

    def logic_divisors(self, v):
        try: self.show_res(f"Divisors: {ntheory.divisors(int(simplify(self.clean_input(v))))}")
        except: self.show_res("Error.")

    def logic_solve(self, v):
        try: self.show_res(f"Roots: {solve(self.clean_input(v), x)}")
        except: self.show_res("Could not solve.")

    def logic_expand(self, v):
        try: self.show_res(f"Expanded: {expand(self.clean_input(v))}")
        except: self.show_res("Error.")

    def logic_factor(self, v):
        try: self.show_res(f"Factored: {factor(self.clean_input(v))}")
        except: self.show_res("Error.")

    def logic_der(self, v):
        try: self.show_res(f"df/dx: {diff(self.clean_input(v), x)}")
        except: self.show_res("Error.")

    def logic_int(self, v):
        try: self.show_res(f"∫f(x)dx: {integrate(self.clean_input(v), x)} + C")
        except: self.show_res("Error.")

    def ui_limit_ui(self):
        st.subheader("Limits")
        e = st.text_input("f(x):", "sin(x)/x")
        c = st.text_input("x approaches:", "0")
        if st.button("Compute Limit"):
            try: self.show_res(f"Limit: {limit(self.clean_input(e), x, c)}")
            except: self.show_res("Error.")

    def ui_gcd_lcm(self):
        st.subheader("GCD & LCM")
        n1 = st.number_input("N1:", value=1)
        n2 = st.number_input("N2:", value=1)
        if st.button("Compute"):
            self.show_res(f"GCD: {gcd(int(n1), int(n2))}<br>LCM: {lcm(int(n1), int(n2))}")

    def logic_pass(self, v):
        try:
            res = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(int(v)))
            self.show_res(f"Generated: <code>{res}</code>")
        except: self.show_res("Error.")

    def logic_picker(self, v):
        try: self.show_res(f"Picked: {random.choice([i.strip() for i in v.split(',')])}")
        except: self.show_res("Error.")

    def ui_color_tool(self):
        st.subheader("Color")
        if st.button("Compute Color"):
            c = "#%06x" % random.randint(0, 0xFFFFFF)
            self.show_res(f"Color: <span style='color:{c}'>{c}</span>")

    def ui_dice_tool(self):
        st.subheader("Dice")
        t = st.selectbox("Type:", ["d6", "d20"])
        if st.button("Roll Dice"):
            self.show_res(f"Result: {random.randint(1, 6 if t=='d6' else 20)}")

    def ui_rng_tool(self):
        st.subheader("RNG")
        mi = st.number_input("Min:", value=1)
        ma = st.number_input("Max:", value=100)
        if st.button("Generate Number"):
            self.show_res(f"Result: {random.randint(int(mi), int(ma))}")

    def ui_home(self):
        st.title("🏠 Home")
        c1, c2 = st.columns([0.22, 0.78])
        with c1: st.write("Welcome back, Commander.")
        with c2:
            # SỬ DỤNG TYPE SECONDARY ĐỂ GIẤU
            if st.button(" ", key="egg_trigger", type="secondary"):
                st.session_state['click_count'] += 1
                if st.session_state['click_count'] >= 5:
                    st.balloons()
                    self.show_res("🎁 <b>STATUS UPGRADED:</b> Legendary User Detected.")
                else: st.toast(f"Security probe... {st.session_state['click_count']}/5")
        
        st.info("Station is operational. Select a core module from the sidebar.")

    def ui_update_log(self):
        st.subheader("📜 System Update Log")
        st.markdown("""
        <table class="update-table">
            <tr><th>Date</th><th>Module</th><th>Changes</th></tr>
            <tr><td>2026-03-28</td><td><b>Bug Fix</b></td><td><b>CRITICAL:</b> Restored all missing 'Compute' buttons.</td></tr>
            <tr><td>2026-03-28</td><td><b>Core</b></td><td>Enhanced CSS for button visibility and state management.</td></tr>
            <tr><td>2026-03-27</td><td><b>Interface</b></td><td>Optimized for high-resolution displays.</td></tr>
        </table>
        """, unsafe_allow_html=True)

    def ui_tutorial(self): st.info("Use '^' for exponents (e.g., x^2). Always use '*' for multiplication.")
    def ui_health(self): st.success("System Health: 100% | Engine: Online")

# Boot
ApexTools()
