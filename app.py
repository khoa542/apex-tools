import streamlit as st
import math
import random
import string
from collections import Counter
from sympy import symbols, diff, integrate, solve, simplify, isprime, ntheory, limit, expand, factor, oo, gcd, lcm, Integer

# --- CONFIG STREAMLIT (WIDE MODE) ---
st.set_page_config(layout="wide", page_title="ApexTools Pro")

# --- SYMBOLIC ENGINE ---
x, y, z = symbols('x y z')

class ApexTools:
    def __init__(self):
        self.css = """
        <style>
            .apex-wrapper { background-color: #c0c0c0; border: 4px outset #fff; padding: 10px; width: 100%; font-family: 'Tahoma', sans-serif; }
            .apex-header { background: linear-gradient(90deg, #000040, #000080); color: #fff; padding: 10px; font-weight: bold; font-size: 20px; border: 2px inset #fff; display: flex; justify-content: space-between; }
            .res-box { background: #f0f0f0; border: 2px inset #808080; padding: 15px; color: #000; font-family: 'Consolas', monospace; font-size: 18px; margin-top: 20px; word-wrap: break-word; }
            .marquee-bar { background: #000; color: #0f0; font-family: 'Courier New'; font-size: 13px; border: 1px solid #fff; padding: 3px; }
            .status-tag { color: #00ff00; border: 1px solid #0f0; padding: 2px 8px; font-size: 11px; background: #002200; }
            .tutorial-table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px; }
            .tutorial-table td, .tutorial-table th { border: 1px solid #808080; padding: 8px; text-align: left; }
            .tutorial-table th { background-color: #e0e0e0; }
            .welcome-screen { text-align: center; padding: 50px; border: 2px dashed #000080; background: #f9f9f9; }
        </style>
        """
        st.markdown(self.css, unsafe_allow_html=True)
        st.markdown('<div class="apex-header"><span>ApexTools Pro</span><span class="status-tag">CORE_STATUS: STABLE</span></div>', unsafe_allow_html=True)
        st.markdown('<marquee class="marquee-bar">ApexTools v2.2 - ENGINE UPDATED: Expression Support for Number Theory... READY... </marquee>', unsafe_allow_html=True)

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

    def show_res(self, text):
        st.markdown(f'<div class="res-box"><b>ApexTools Log:</b><br>{text}</div>', unsafe_allow_html=True)

    def clean_input(self, text):
        return str(text).replace('^', '**')

    def router(self, v):
        if v.startswith('---'): 
            st.warning("Please select a valid tool option.")
            return 

        if v == 'Home': self.ui_home()
        elif v == 'Tutorial': self.ui_manual()
        elif v == 'System Health': self.ui_health()
        elif v == 'Pro Calculator': self.ui_generic("Calculator", "5 + 2^3", self.logic_calc)
        elif v == 'GCD & LCM': self.ui_gcd_lcm()
        elif v == 'Linear Solver': self.ui_generic("Linear Solver", "2*x - 10", self.logic_solve)
        elif v == 'Quadratic Solver': self.ui_generic("Quadratic Solver", "x^2 - 5*x + 6", self.logic_solve)
        elif v == 'Expand Expression': self.ui_generic("Expand", "(x+1)^2", self.logic_expand)
        elif v == 'Factorize Polynomial': self.ui_generic("Factorize", "x^2 - 1", self.logic_factorize)
        elif v == 'Check Square Number': self.ui_generic("Square Check", "2^50 + 1", self.logic_square)
        elif v == 'Check Prime Number': self.ui_generic("Prime Check", "2^31 - 1", self.logic_prime)
        elif v == 'Prime Factorization': self.ui_generic("Prime Factorization", "2^10", self.logic_p_factors)
        elif v == 'Find All Divisors': self.ui_generic("Divisor Finder", "100", self.logic_divisors)
        elif v == 'Derivative (df/dx)': self.ui_generic("Derivative", "x^3", self.logic_der)
        elif v == 'Integral (∫dx)': self.ui_generic("Integral", "sin(x)", self.logic_int)
        elif v == 'Limits (x -> c)': self.ui_limit()
        elif v == 'Length': self.ui_conv("Length", ['Meters', 'Kilometers', 'Inches', 'Feet', 'Miles'])
        elif v == 'Mass': self.ui_conv("Mass", ['Grams', 'Kilograms', 'Pounds', 'Ounces', 'Metric Tons'])
        elif v == 'Time': self.ui_conv("Time", ['Seconds', 'Minutes', 'Hours', 'Days', 'Years'])
        elif v == 'Power': self.ui_conv("Power", ['Watts', 'Kilowatts', 'Horsepower'])
        elif v == 'Force': self.ui_conv("Force", ['Newtons', 'Dynes', 'Pound-force'])
        elif v == 'Voltage': self.ui_conv("Voltage", ['Volts', 'Millivolts', 'Kilovolts'])
        elif v == 'Temperature': self.ui_temp()
        elif v == 'Secure Password Gen': self.ui_generic("Password Gen", "Length (e.g. 12)", self.logic_pass)
        elif v == 'Random Color HEX': self.ui_color()
        elif v == 'Dice Roller (d6/d20)': self.ui_dice()
        elif v == 'Random List Picker': self.ui_generic("List Picker", "Item1, Item2, Item3", self.logic_picker)
        elif v == 'Integer RNG (Min/Max)': self.ui_rng_int()

    def ui_home(self):
        st.markdown("""
            <div class="welcome-screen">
                <h1 style="color:#000080;">ApexTools Multi-Utility</h1>
                <p style="font-size:16px;">Welcome to the All-in-One symbolic computation engine.</p>
                <hr>
                <p>Support for expressions like <b>2^50 + 1</b> is now enabled for Number Theory tools.</p>
            </div>
        """, unsafe_allow_html=True)

    def ui_generic(self, name, placeholder, callback):
        st.subheader(name)
        inp = st.text_input("Input:", placeholder=placeholder, key=name)
        if st.button(f"Compute {name}"):
            callback(inp)

    # --- UPDATED LOGIC FOR EXPRESSIONS ---
    def logic_square(self, v): 
        try:
            # Dùng simplify để tính toán biểu thức (VD: 2^50 + 1)
            val = simplify(self.clean_input(v))
            if val.is_Integer:
                n = int(val)
                res = n >= 0 and math.isqrt(n)**2 == n
                self.show_res(f"Expression Value: {n}<br><b>Is Perfect Square: {res}</b>")
            else:
                self.show_res("Error: Expression did not result in a single integer.")
        except Exception as e:
            self.show_res(f"Error processing expression: {e}")

    def logic_prime(self, v): 
        try:
            val = simplify(self.clean_input(v))
            if val.is_Integer:
                n = int(val)
                self.show_res(f"Expression Value: {n}<br><b>Is Prime: {isprime(n)}</b>")
            else:
                self.show_res("Error: Result is not an integer.")
        except Exception as e:
            self.show_res(f"Error: {e}")

    def logic_p_factors(self, v):
        try:
            val = simplify(self.clean_input(v))
            if val.is_Integer:
                num = int(val)
                if num < 2: self.show_res(f"Input {num} must be >= 2"); return
                factors_dict = ntheory.factorint(num)
                res_str = " * ".join([f"{p}^{exp}" if exp > 1 else str(p) for p, exp in sorted(factors_dict.items())])
                self.show_res(f"Value: {num}<br><b>{num} = {res_str}</b>")
            else:
                self.show_res("Error: Result is not an integer.")
        except Exception as e: self.show_res(f"Invalid Input: {e}")

    # --- REMAINING LOGIC (Giữ nguyên) ---
    def logic_calc(self, v): 
        try: self.show_res(f"Result: {simplify(self.clean_input(v))}")
        except: self.show_res("Error: Invalid Expression")
        
    def logic_gcd_lcm(self, a, b): self.show_res(f"GCD: {gcd(a, b)}<br>LCM: {lcm(a, b)}")
    def logic_solve(self, v): self.show_res(f"Solution: {solve(self.clean_input(v), x)}")
    def logic_expand(self, v): self.show_res(f"Expanded: {expand(self.clean_input(v))}")
    def logic_factorize(self, v): self.show_res(f"Factored: {factor(self.clean_input(v))}")

    def ui_manual(self): 
        st.markdown("""
            <h3>ApexTools Quick Start</h3>
            <table class="tutorial-table">
                <tr><th>Operation</th><th>Symbol</th><th>Example</th></tr>
                <tr><td><b>Exponents</b></td><td>^ or **</td><td>2^50 hoặc x^2</td></tr>
                <tr><td><b>Square Root</b></td><td>sqrt()</td><td>sqrt(16)</td></tr>
            </table>
        """, unsafe_allow_html=True)

    def ui_health(self): 
        st.markdown("<h3 style='color:green;'>ApexTools System Status</h3><p>Operational. Symbolic Engine updated to support expression evaluation.</p>", unsafe_allow_html=True)

    def ui_gcd_lcm(self):
        st.subheader("GCD & LCM")
        n1 = st.number_input("Num 1:", value=1)
        n2 = st.number_input("Num 2:", value=1)
        if st.button("Compute GCD & LCM"):
            self.logic_gcd_lcm(n1, n2)

    def ui_limit(self):
        st.subheader("Limits")
        expr = st.text_input("Function:", placeholder="1/x")
        val = st.text_input("Approaches:", placeholder="oo or 0")
        if st.button("Compute Limit"):
            self.logic_limit(expr, val)

    def ui_conv(self, title, units):
        st.subheader(f"{title} Converter")
        val = st.number_input("Value:", value=1.0)
        from_u = st.selectbox("From:", units, key=f"{title}_from")
        to_u = st.selectbox("To:", units, key=f"{title}_to")
        if st.button(f"Convert {title}"):
            self.logic_units(val, from_u, to_u)

    def ui_temp(self):
        st.subheader("Temperature")
        val = st.number_input("Temp:", value=0.0)
        f_u = st.selectbox("From:", ['Celsius', 'Fahrenheit', 'Kelvin'], key="temp_from")
        t_u = st.selectbox("To:", ['Celsius', 'Fahrenheit', 'Kelvin'], key="temp_to")
        if st.button("Convert Temperature"):
            self.logic_temp(val, f_u, t_u)

    def ui_color(self):
        st.subheader("Color Generator")
        if st.button("Generate Hex Color"):
            self.logic_color()

    def ui_dice(self):
        st.subheader("Dice Roller")
        drop = st.selectbox("Dice:", ['d6', 'd20'])
        if st.button("Roll"):
            self.logic_dice(drop)

    def ui_rng_int(self):
        st.subheader("Integer RNG")
        mi = st.number_input("Min:", value=1)
        ma = st.number_input("Max:", value=100)
        if st.button("Generate"):
            self.show_res(f"Result: {random.randint(int(mi), int(ma))}")

    def logic_divisors(self, v): 
        try:
            val = simplify(self.clean_input(v))
            self.show_res(f"Divisors: {ntheory.divisors(int(val))}")
        except: self.show_res("Invalid Input.")

    def logic_der(self, v): self.show_res(f"Derivative: {diff(self.clean_input(v), x)}")
    def logic_int(self, v): self.show_res(f"Integral: {integrate(self.clean_input(v), x)} + C")
    def logic_limit(self, e, v): 
        try: target = oo if v == 'oo' else simplify(v)
        except: target = 0
        self.show_res(f"Limit: {limit(self.clean_input(e), x, target)}")

    def logic_units(self, val, f, t):
        db = {'Meters':1,'Kilometers':1000,'Inches':0.0254,'Feet':0.3048,'Miles':1609.34,'Grams':1,'Kilograms':1000,'Pounds':453.59,'Ounces':28.35,'Metric Tons':1e6,'Seconds':1,'Minutes':60,'Hours':3600,'Days':86400,'Years':31536000,'Watts':1,'Kilowatts':1000,'Horsepower':745.7,'Newtons':1,'Dynes':1e-5,'Pound-force':4.448,'Volts':1,'Millivolts':0.001,'Kilovolts':1000}
        self.show_res(f"Result: {val*(db[f]/db[t]):.6g} {t}")

    def logic_temp(self, v, f, t):
        if f == t: r = v
        elif f == 'Celsius': r = v+273.15 if t == 'Kelvin' else v*1.8+32
        elif f == 'Fahrenheit': r = (v-32)/1.8+273.15 if t == 'Kelvin' else (v-32)/1.8
        else: r = v-273.15 if t == 'Celsius' else (v-273.15)*1.8+32
        self.show_res(f"Result: {r:.2f} {t}")

    def logic_pass(self, v): self.show_res("".join(random.choice(string.ascii_letters+string.digits) for _ in range(int(v))))
    def logic_color(self): c = "#%06x"%random.randint(0,0xFFFFFF); self.show_res(f"HEX Code: <b style='color:{c}'>{c}</b>")
    def logic_dice(self, v): self.show_res(f"Rolled: {random.randint(1, 6 if v=='d6' else 20)}")
    def logic_picker(self, v): self.show_res(f"Picked: {random.choice([i.strip() for i in v.split(',')])}")

# Launch
ApexTools()
