import streamlit as st
import math
import random
import string
import time
from sympy import symbols, diff, integrate, solve, simplify, isprime, ntheory, limit, expand, factor, oo, gcd, lcm

# --- CONFIG STREAMLIT ---
st.set_page_config(layout="wide", page_title="ApexTools Pro")

# --- SYMBOLIC ENGINE ---
x, y, z = symbols('x y z')

class ApexTools:
    def __init__(self):
        # State quản lý các Easter Eggs
        if 'matrix_mode' not in st.session_state: st.session_state['matrix_mode'] = False
        if 'click_count' not in st.session_state: st.session_state['click_count'] = 0

        self.apply_styles()
        self.render_header()
        
        self.menu_options = [
            'Home', '--- SYSTEM ---', 'Tutorial', 'System Health',
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
        # Chế độ Matrix hoặc Trắng Xám cổ điển
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
                display: flex; justify-content: space-between; font-family: 'Segoe UI', sans-serif;
            }}
            .res-box {{ 
                background: {"#000" if is_matrix else "#fdfdfd"}; 
                border: 2px inset {border_color}; padding: 15px; 
                color: {text_color}; font-family: 'Consolas', monospace; 
                font-size: 18px; margin-top: 20px; 
            }}
            .marquee-bar {{ background: #000; color: #0f0; font-family: 'Courier New'; font-size: 13px; border: 1px solid #fff; padding: 3px; }}
            
            /* Nút Secret tàng hình hoàn toàn */
            .stButton>button[kind="secondary"] {{
                background: transparent !important;
                color: transparent !important;
                border: none !important;
                width: 10px !important;
                height: 10px !important;
                padding: 0 !important;
                min-width: 0 !important;
                margin-left: -10px !important;
            }}
            .stButton>button[kind="secondary"]:hover {{
                cursor: default !important;
            }}
        </style>
        """
        st.markdown(self.css, unsafe_allow_html=True)

    def render_header(self):
        st.markdown('<div class="apex-header"><span>ApexTools Pro</span><span>CORE: ONLINE</span></div>', unsafe_allow_html=True)
        st.markdown('<marquee class="marquee-bar">Expression support: ACTIVE | "hack" to override | Perfect numbers detection: ON... </marquee>', unsafe_allow_html=True)

    def show_res(self, text):
        st.markdown(f'<div class="res-box"><b>Console_Output:></b><br>{text}</div>', unsafe_allow_html=True)

    def check_global_eggs(self, v):
        low_v = str(v).lower().strip()
        if low_v == "hack":
            st.session_state['matrix_mode'] = not st.session_state['matrix_mode']
            st.rerun()
            return True
        elif low_v == "coffee":
            self.show_res("☕ Energy restored.")
            return True
        return False

    def ui_home(self):
        st.title("🏠 Home")
        # Chia cột để đặt nút Secret ngay sau dấu chấm
        c1, c2 = st.columns([0.23, 0.77])
        with c1:
            st.write("Welcome back, Commander.")
        with c2:
            if st.button(" ", key="hidden_secret_btn"):
                st.session_state['click_count'] += 1
                if st.session_state['click_count'] >= 5:
                    st.balloons()
                    self.show_res("🎁 <b>ACCESS GRANTED:</b> System Core unlocked.<br>Status: LEGENDARY.")
                else:
                    st.toast(f"Probe: {st.session_state['click_count']}/5")

        st.info("Select a tool from the sidebar to begin. Support for expressions like '2^50+1' is active.")

    def ui_generic(self, name, placeholder, callback):
        st.subheader(name)
        inp = st.text_input("Enter expression:", placeholder=placeholder, key=f"inp_{name}")
        if st.button(f"Compute", key=f"btn_{name}"):
            callback(inp)

    # --- MATH LOGIC ---
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

    def router(self, v):
        if v.startswith('---'): return
        if v == 'Home': self.ui_home()
        elif v == 'Check Prime Number': self.ui_generic("Prime Check", "97", self.logic_prime)
        elif v == 'Check Square Number': self.ui_generic("Square Check", "2^10", self.logic_square)
        elif v == 'Pro Calculator': self.ui_generic("Calculator", "2^50 + 1", self.logic_calc)
        elif v == 'System Health': self.ui_health()
        else:
            st.info(f"The module '{v}' is ready for input.")
            self.ui_generic(v, "...", self.logic_calc)

    def ui_health(self):
        st.subheader("System Health")
        st.write("Math Engine: Stable")
        if st.session_state['matrix_mode']: st.success("Matrix Mode: ON")

# Launch
ApexTools()
