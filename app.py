import streamlit as st
import math
import random
import string
from sympy import symbols, simplify, isprime, ntheory, gcd, lcm

# --- CONFIG STREAMLIT ---
st.set_page_config(layout="wide", page_title="ApexTools Pro")

class ApexTools:
    def __init__(self):
        if 'matrix_mode' not in st.session_state: st.session_state['matrix_mode'] = False
        if 'click_count' not in st.session_state: st.session_state['click_count'] = 0

        self.apply_styles()
        self.render_header()
        
        self.menu_options = [
            'Home', '--- SYSTEM ---', 'Tutorial', 'System Health',
            '--- MATH CORE ---', 'Pro Calculator', 'GCD & LCM', 'Linear Solver',
            '--- NUMBER THEORY ---', 'Check Square Number', 'Check Prime Number',
            'Prime Factorization', 'Find All Divisors',
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
        st.markdown('<marquee class="marquee-bar">Random Engine: READY | Expressions supported | Invisible secrets active... </marquee>', unsafe_allow_html=True)

    def show_res(self, text):
        st.markdown(f'<div class="res-box"><b>Console_Output:></b><br>{text}</div>', unsafe_allow_html=True)

    def check_global_eggs(self, v):
        low_v = str(v).lower().strip()
        if low_v == "hack":
            st.session_state['matrix_mode'] = not st.session_state['matrix_mode']
            st.rerun()
            return True
        elif low_v == "coffee":
            self.show_res("☕ System energy at 100%.")
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
        st.info("Select a tool from the sidebar to begin.")

    # --- ROUTER ---
    def router(self, v):
        if v.startswith('---'): return
        if v == 'Home': self.ui_home()
        elif v == 'Pro Calculator': self.ui_math_tool("Calculator", "Enter expression:", "2^50 + 1", self.logic_calc)
        elif v == 'Check Prime Number': self.ui_math_tool("Prime Check", "Enter number:", "97", self.logic_prime)
        elif v == 'Check Square Number': self.ui_math_tool("Square Check", "Enter number:", "1024", self.logic_square)
        
        # RANDOM TOOLS
        elif v == 'Secure Password Gen': self.ui_random_tool("Password Generator", "Enter length:", "12", self.logic_pass)
        elif v == 'Random Color HEX': self.ui_color_tool()
        elif v == 'Dice Roller (d6/d20)': self.ui_dice_tool()
        elif v == 'Random List Picker': self.ui_random_tool("List Picker", "Enter items (comma separated):", "Apple, Orange, Banana", self.logic_picker)
        elif v == 'Integer RNG (Min/Max)': self.ui_rng_tool()
        
        elif v == 'System Health': self.ui_health()
        else: st.info(f"The module '{v}' is under maintenance or coming soon.")

    # --- UI WRAPPERS ---
    def ui_math_tool(self, name, label, placeholder, callback):
        st.subheader(name)
        inp = st.text_input(label, placeholder=placeholder, key=f"inp_{name}")
        if st.button(f"Compute {name}", key=f"btn_{name}"):
            callback(inp)

    def ui_random_tool(self, name, label, placeholder, callback):
        st.subheader(name)
        inp = st.text_input(label, placeholder=placeholder, key=f"inp_{name}")
        if st.button(f"Generate", key=f"btn_{name}"):
            callback(inp)

    def ui_color_tool(self):
        st.subheader("Random Color HEX")
        st.write("Click below to generate a random web color code.")
        if st.button("Generate Color"):
            color = "#%06x" % random.randint(0, 0xFFFFFF)
            self.show_res(f"Generated HEX: <span style='color:{color}; font-weight:bold;'>{color}</span>")

    def ui_dice_tool(self):
        st.subheader("Dice Roller")
        dice_type = st.selectbox("Select Dice Type:", ["d6 (Standard)", "d20 (D20 System)"])
        if st.button("Roll Dice"):
            res = random.randint(1, 6) if "d6" in dice_type else random.randint(1, 20)
            self.show_res(f"Dice Result ({dice_type.split()[0]}): 🎲 **{res}**")

    def ui_rng_tool(self):
        st.subheader("Integer RNG")
        c1, c2 = st.columns(2)
        with c1: min_v = st.number_input("Minimum:", value=1)
        with c2: max_v = st.number_input("Maximum:", value=100)
        if st.button("Generate Random Number"):
            if min_v <= max_v:
                res = random.randint(int(min_v), int(max_v))
                self.show_res(f"RNG Result: **{res}** (Range: {min_v}-{max_v})")
            else:
                self.show_res("Error: Minimum cannot be greater than Maximum.")

    # --- LOGIC ---
    def logic_calc(self, v):
        if self.check_global_eggs(v): return
        try: self.show_res(f"Result: {simplify(v.replace('^','**'))}")
        except: self.show_res("Error in expression.")

    def logic_prime(self, v):
        if self.check_global_eggs(v): return
        try:
            n = int(simplify(v.replace('^','**')))
            if n == 666: self.show_res("⚠️ Infernal number. Not Prime."); return
            self.show_res(f"Is Prime: {isprime(n)}")
        except: self.show_res("Input error.")

    def logic_square(self, v):
        try:
            n = int(simplify(v.replace('^','**')))
            res = n >= 0 and math.isqrt(n)**2 == n
            self.show_res(f"Value: {n}<br>Perfect Square: {res}")
        except: self.show_res("Input error.")

    def logic_pass(self, v):
        try:
            length = int(v)
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            res = "".join(random.choice(chars) for _ in range(length))
            self.show_res(f"Secure Password: <code style='color:blue;'>{res}</code>")
        except: self.show_res("Error: Please enter a valid number for length.")

    def logic_picker(self, v):
        if not v.strip(): self.show_res("Error: List is empty."); return
        items = [i.strip() for i in v.split(',') if i.strip()]
        res = random.choice(items)
        self.show_res(f"Items processed: {len(items)}<br>Picked Choice: 🎯 **{res}**")

    def ui_health(self):
        st.subheader("System Health")
        st.write("Core Status: Stable")
        if st.session_state['matrix_mode']: st.success("Matrix Override: ACTIVE")

# Launch
ApexTools()
