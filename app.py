import streamlit as st
import math
import random
import string
import time
from collections import Counter
from sympy import symbols, diff, integrate, solve, simplify, isprime, ntheory, limit, expand, factor, oo, gcd, lcm, Integer

# --- CONFIG STREAMLIT ---
st.set_page_config(layout="wide", page_title="ApexTools Pro v3.1")

# --- SYMBOLIC ENGINE ---
x, y, z = symbols('x y z')

class ApexTools:
    def __init__(self):
        # Khởi tạo state cho các Easter Egg mới
        if 'dark_mode_egg' not in st.session_state: st.session_state['dark_mode_egg'] = False
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

        self.selection = st.sidebar.radio("APEX MENU", self.menu_options)
        self.router(self.selection)

    def apply_styles(self):
        # Easter Egg 6: Matrix Mode (Giao diện đen xanh lá toàn tập)
        bg_color = "#000" if st.session_state['matrix_mode'] else "#c0c0c0"
        text_color = "#0f0" if st.session_state['matrix_mode'] else "#000"
        header_grad = "linear-gradient(90deg, #003300, #006600)" if st.session_state['matrix_mode'] else "linear-gradient(90deg, #000040, #000080)"
        
        self.css = f"""
        <style>
            .stApp {{ background-color: {bg_color}; color: {text_color}; }}
            .apex-header {{ background: {header_grad}; color: #fff; padding: 10px; font-weight: bold; font-size: 20px; border: 2px inset #fff; display: flex; justify-content: space-between; }}
            .res-box {{ background: {"#001100" if st.session_state['matrix_mode'] else "#f0f0f0"}; border: 2px inset {"#0f0" if st.session_state['matrix_mode'] else "#808080"}; padding: 15px; color: {text_color}; font-family: 'Consolas', monospace; font-size: 18px; margin-top: 20px; word-wrap: break-word; }}
            .marquee-bar {{ background: #000; color: #0f0; font-family: 'Courier New'; font-size: 13px; border: 1px solid #fff; padding: 3px; }}
            .egg-found {{ color: #ff00ff; animation: blinker 1s linear infinite; font-weight: bold; }}
            @keyframes blinker {{ 50% {{ opacity: 0; }} }}
        </style>
        """
        st.markdown(self.css, unsafe_allow_html=True)

    def render_header(self):
        st.markdown('<div class="apex-header"><span>ApexTools Pro v3.1</span><span style="font-size:10px">EST. 2024</span></div>', unsafe_allow_html=True)
        st.markdown('<marquee class="marquee-bar">NEW: Matrix Mode discovered? | Try "666" in Prime Check... | "hack" to change UI... | Perfect numbers are rare... </marquee>', unsafe_allow_html=True)

    def show_res(self, text):
        st.markdown(f'<div class="res-box"><b>System_Log:></b><br>{text}</div>', unsafe_allow_html=True)

    def clean_input(self, text):
        return str(text).replace('^', '**')

    def check_global_eggs(self, v):
        low_v = str(v).lower().strip()
        
        # Easter Egg 7: "hack" - Kích hoạt Matrix Mode
        if low_v == "hack":
            st.session_state['matrix_mode'] = not st.session_state['matrix_mode']
            self.show_res("<span class='egg-found'>[SYSTEM OVERRIDE]</span><br>Matrix mode toggled. Reality is often disappointing.")
            time.sleep(0.5)
            st.rerun()
            return True
            
        # Easter Egg 8: "coffee" - Nạp năng lượng
        elif low_v == "coffee":
            self.show_res("☕ *Slurp*... Energy refilled. ApexTools is now 0.0001% faster.")
            return True

        # Easter Egg 1, 2, 3 cũ (xyzzy, pi, make it rain)
        elif low_v == "xyzzy": st.balloons(); self.show_res("🎁 Classic magic words."); return True
        elif low_v == "pi": self.show_res(f"Pi = {math.pi}"); return True
        elif low_v == "make it rain": st.snow(); self.show_res("🎁 Cold cash!"); return True
            
        return False

    def router(self, v):
        if v.startswith('---'): return 
        if v == 'Home': self.ui_home()
        elif v == 'Tutorial': self.ui_manual()
        elif v == 'System Health': self.ui_health()
        elif v == 'Pro Calculator': self.ui_generic("Calculator", "5 + 2^3", self.logic_calc)
        elif v == 'GCD & LCM': self.ui_gcd_lcm()
        elif v == 'Check Square Number': self.ui_generic("Square Check", "2^50", self.logic_square)
        elif v == 'Check Prime Number': self.ui_generic("Prime Check", "97", self.logic_prime)
        elif v == 'Find All Divisors': self.ui_generic("Divisor Finder", "24", self.logic_divisors)
        # ... (Các hàm khác giữ nguyên từ bản trước)
        else:
            st.info(f"Tool '{v}' is active. Enter value below.")
            self.ui_generic(v, "...", self.logic_calc)

    def ui_home(self):
        st.title("🏠 Central Command")
        st.write("Welcome back, Commander.")
        # Easter Egg 9: Click vào logo ẩn
        if st.button("秘密 (Secret)", key="secret_btn"):
            st.session_state['click_count'] += 1
            if st.session_state['click_count'] >= 5:
                self.show_res("<span class='egg-found'>🎁 PERSISTENCE PAID OFF!</span><br>You clicked enough. Take this: <b>01100110 01110101 01101110</b>")
                st.balloons()
            else:
                st.write(f"Keep clicking... ({st.session_state['click_count']}/5)")

    def ui_generic(self, name, placeholder, callback):
        st.subheader(name)
        inp = st.text_input("Input:", placeholder=placeholder, key=f"inp_{name}")
        if st.button(f"Compute", key=f"btn_{name}"):
            callback(inp)

    # --- UPDATED LOGIC WITH NEW EGGS ---
    def logic_prime(self, v):
        if self.check_global_eggs(v): return
        try:
            n = int(simplify(self.clean_input(v)))
            # Easter Egg 10: 666 - The Beast
            if n == 666:
                self.show_res("<span style='color:red;'>⚠️ ERROR: INFERNAL NUMBER DETECTED</span><br>666 is not prime. It is the number of the beast. *Thunder sounds*")
                return
            self.show_res(f"Is Prime: {isprime(n)}")
        except: self.show_res("Invalid Input.")

    def logic_divisors(self, v):
        try:
            n = int(simplify(self.clean_input(v)))
            # Easter Egg 11: Perfect Numbers (Số hoàn hảo)
            perfect_numbers = [6, 28, 496, 8128]
            divs = ntheory.divisors(n)
            if n in perfect_numbers:
                self.show_res(f"🎁 <span class='egg-found'>PERFECT NUMBER DETECTED!</span><br>Divisors: {divs}<br>Sum of proper divisors = {n}. Rare and beautiful.")
                st.balloons()
            else:
                self.show_res(f"Divisors: {divs}")
        except: self.show_res("Invalid Input.")

    def logic_calc(self, v):
        if self.check_global_eggs(v): return
        try: self.show_res(f"Result: {simplify(self.clean_input(v))}")
        except: self.show_res("Calculation Error.")

    def ui_health(self):
        # Easter Egg 12: System Health Check ẩn
        st.markdown("### System Diagnostics")
        cols = st.columns(3)
        cols[0].metric("CPU", "2.4 GHz", "Stable")
        cols[1].metric("Memory", "128MB / 512MB", "-2%")
        cols[2].metric("Math Engine", "READY", "100%")
        
        if st.checkbox("Show hidden logs"):
            st.code("DEBUG: User is looking for eggs...\nDEBUG: Easter_Egg_Manager: OK\nDEBUG: Coffee_Level: LOW")

    # (Các UI khác giữ nguyên để tiết kiệm không gian code)
    def ui_manual(self): st.write("Check the marquee for hints!")
    def logic_square(self, v): self.show_res(f"Square: {math.isqrt(int(simplify(self.clean_input(v))))**2 == int(simplify(self.clean_input(v)))}")
    def ui_gcd_lcm(self):
        n1 = st.number_input("N1", value=1, key="g1")
        n2 = st.number_input("N2", value=1, key="g2")
        if st.button("Run"): self.show_res(f"GCD: {gcd(n1, n2)}")

# Run
ApexTools()
