# TextInput 3 character limit:
#       https://groups.google.com/g/kivy-users/c/xTcDcm2eKEE


from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import time
import threading
import socket
from math import sqrt
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.properties import BooleanProperty

green = [0.5, 255, 0.5, 0.95]
red = [255, 0.5, 0.5, 0.95]

is_connected = False    # Check if it's connected.


class LimitInput(TextInput):
    valid_characters = "0123456789.,"

    def insert_text(self, substring, from_undo=False):
        if substring in self.valid_characters:
            s = ''.join(substring)
            return super().insert_text(s, from_undo=from_undo)
        else:
            pass

    def keyboard_on_key_up(self, keycode, text):
        if self.readonly and text[1] == "backspace":
            self.readonly = False
            self.do_backspace()


class Calc:
    @staticmethod
    def total_current(i_1, i_2, i_3, i_4, i_5, i_6):
        return i_1 + i_2 + i_3 + i_4 + i_5 + i_6

    @staticmethod
    def i_lineer_percentage(v, i_lineer, kva, pf):
        return (v*i_lineer) * 100 / (kva*pf*1000)

    @staticmethod
    def i_nonlineer_percentage(v, i_nonlineer, kva, pf):
        return (v*i_nonlineer*0.7) * 100 / (kva*pf*1000)

    @staticmethod
    def kw_2(v, i_lineer, i_nonlineer):
        return v*(i_lineer + 0.7 * i_nonlineer)

    @staticmethod
    def power_factor2(kw_2, kva_2):
        return kw_2 / kva_2

    @staticmethod
    def kva_2(v, i_lineer, i_nonlineer):
        # print(f"v={v}, i_lineer={i_lineer}, i_nonlineer={i_nonlineer}")
        return sqrt((v * (i_lineer + (0.7 * i_nonlineer))) ** 2 + (v * 0.3 * 2.41 * i_nonlineer) ** 2)

    @staticmethod
    def kw_prc(kw_2, kva, pf):  # kW percentage (%kW)
        return kw_2 / (kva * pf * 1000)

    @staticmethod
    def kva_prc(kva_2, kva):    # kVA percentage (%kVA)
        return kva_2 / (kva * 1000)

    @staticmethod
    def percentage(v, kva, pf, i):

        i_lineer_total = Calc.total_current(i[0], i[1], i[2], i[3], i[4], i[5])
        i_nonlineer_total = Calc.total_current(i[6], i[7], i[8], i[9], i[10], 0)

        kw_2 = Calc.kw_2(v, i_lineer_total, i_nonlineer_total)
        kva_2 = Calc.kva_2(v, i_lineer_total, i_nonlineer_total)

        power_factor2 = Calc.power_factor2(kw_2, kva_2)

        kw_prc = Calc.kw_prc(kw_2, kva, pf)     # kW percentage (%kW)
        kva_prc = Calc.kva_prc(kva_2, kva)      # kVA percentage (%kVA)

        i1_prc = 0
        i2_prc = 0
        i3_prc = 0
        i4_prc = 0
        i5_prc = 0
        i6_prc = 0
        i7_prc = 0
        i8_prc = 0
        i9_prc = 0
        i10_prc = 0
        i11_prc = 0

        if kw_prc >= kva_prc:
            i1_prc = Calc.i_lineer_percentage(v, i[0], kva, pf)
            i2_prc = Calc.i_lineer_percentage(v, i[1], kva, pf)
            i3_prc = Calc.i_lineer_percentage(v, i[2], kva, pf)
            i4_prc = Calc.i_lineer_percentage(v, i[3], kva, pf)
            i5_prc = Calc.i_lineer_percentage(v, i[4], kva, pf)
            i6_prc = Calc.i_lineer_percentage(v, i[5], kva, pf)

            i7_prc = Calc.i_nonlineer_percentage(v, i[6], kva, pf)
            i8_prc = Calc.i_nonlineer_percentage(v, i[7], kva, pf)
            i9_prc = Calc.i_nonlineer_percentage(v, i[8], kva, pf)
            i10_prc = Calc.i_nonlineer_percentage(v, i[9], kva, pf)
            i11_prc = Calc.i_nonlineer_percentage(v, i[10], kva, pf)

        elif kva_prc > kw_prc:
            i1_prc = Calc.i_lineer_percentage(v, i[0], kva, power_factor2)
            i2_prc = Calc.i_lineer_percentage(v, i[1], kva, power_factor2)
            i3_prc = Calc.i_lineer_percentage(v, i[2], kva, power_factor2)
            i4_prc = Calc.i_lineer_percentage(v, i[3], kva, power_factor2)
            i5_prc = Calc.i_lineer_percentage(v, i[4], kva, power_factor2)
            i6_prc = Calc.i_lineer_percentage(v, i[5], kva, power_factor2)

            i7_prc = Calc.i_nonlineer_percentage(v, i[6], kva, power_factor2)
            i8_prc = Calc.i_nonlineer_percentage(v, i[7], kva, power_factor2)
            i9_prc = Calc.i_nonlineer_percentage(v, i[8], kva, power_factor2)
            i10_prc = Calc.i_nonlineer_percentage(v, i[9], kva, power_factor2)
            i11_prc = Calc.i_nonlineer_percentage(v, i[10], kva, power_factor2)
            pass

        return [kw_2, kva_2, power_factor2, kw_prc, kva_prc, round(i1_prc, 2), round(i2_prc, 2), round(i3_prc, 2),
                round(i4_prc, 2), round(i5_prc, 2), round(i6_prc, 2), round(i7_prc, 2), round(i8_prc, 2),
                round(i9_prc, 2), round(i10_prc, 2), round(i11_prc, 2)]


class ControlPage(Screen):
    r_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    s_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    t_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    r_calc_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    s_calc_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    t_calc_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    prc_calculation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    total_r_prc = 0
    total_s_prc = 0
    total_t_prc = 0

    thread_pause = BooleanProperty(False)
    is_connected = False    # Check if it's connected.
    app_start_setup = True  # Setting threads for once.
    is_trying_to_connect = False

    def reset(self):
        self.tcp_thread_start()

    def percentage_init(self):

        try:
            if float(self.pf.text.replace(',', '.')) == 0:
                return
            initial_calculation = Calc.percentage(float(self.v.text), float(self.kva.text),
                                                  float(self.pf.text.replace(',', '.')),
                                                  [1.5, 3, 6, 9, 18, 32, 0, 0, 0, 0, 0])
            # Edit spesific line
            a = open("ip.txt", "r").read().split('\n')  # Read .txt file
            a[1] = self.v.text  # Write to a spesific line
            a[2] = self.kva.text  # Write to a spesific line
            a[3] = self.pf.text  # Write to a spesific line
            a = "\n".join(a)
            f = open("ip.txt", "w")
            f.write(a)  # Save the file
            f.close()
            if initial_calculation[3] >= initial_calculation[4]:
                self.r_1.text = f' 1,5A\n%{initial_calculation[5]}'
                self.r_2.text = f' 3A\n%{initial_calculation[6]}'
                self.r_3.text = f' 6A\n%{initial_calculation[7]}'
                self.r_4.text = f' 9A\n%{initial_calculation[8]}'
                self.r_5.text = f' 18A\n%{initial_calculation[9]}'
                self.r_6.text = f' 32A\n%{initial_calculation[10]}'

                self.s_1.text = f' 1,5A\n%{initial_calculation[5]}'
                self.s_2.text = f' 3A\n%{initial_calculation[6]}'
                self.s_3.text = f' 6A\n%{initial_calculation[7]}'
                self.s_4.text = f' 9A\n%{initial_calculation[8]}'
                self.s_5.text = f' 18A\n%{initial_calculation[9]}'
                self.s_6.text = f' 32A\n%{initial_calculation[10]}'

                self.t_1.text = f' 1,5A\n%{initial_calculation[5]}'
                self.t_2.text = f' 3A\n%{initial_calculation[6]}'
                self.t_3.text = f' 6A\n%{initial_calculation[7]}'
                self.t_4.text = f' 9A\n%{initial_calculation[8]}'
                self.t_5.text = f' 18A\n%{initial_calculation[9]}'
                self.t_6.text = f' 32A\n%{initial_calculation[10]}'

            if self.r_loads[0:5] != [0, 0, 0, 0, 0]:
                r_prc_enter = Calc.percentage(float(self.v.text), float(self.kva.text),
                                              float(self.pf.text.replace(',', '.')), self.r_calc_loads)
                total_r_prc = 0
                if r_prc_enter[4] > r_prc_enter[3]:
                    # print("flagflag19", r_prc_enter)
                    # print(r_prc_enter[5], r_prc_enter[6], r_prc_enter[15])
                    self.r_1.text = f" 1,5A\n%{r_prc_enter[5]}" if r_prc_enter[5] != 0 else "1,5A"
                    self.r_2.text = f" 3A\n%{r_prc_enter[6]}" if r_prc_enter[6] != 0 else "3A"
                    self.r_3.text = f" 6A\n%{r_prc_enter[7]}" if r_prc_enter[7] != 0 else "6A"
                    self.r_4.text = f" 9A\n%{r_prc_enter[8]}" if r_prc_enter[8] != 0 else "9A"
                    self.r_5.text = f" 18A\n%{r_prc_enter[9]}" if r_prc_enter[9] != 0 else "18A"
                    self.r_6.text = f" 32A\n%{r_prc_enter[10]}" if r_prc_enter[10] != 0 else "32A"
                    self.r_7.text = f" 4A\n%{r_prc_enter[11]}" if r_prc_enter[11] != 0 else "4A"
                    self.r_8.text = f" 8A\n%{r_prc_enter[12]}" if r_prc_enter[12] != 0 else "8A"
                    self.r_9.text = f" 15A\n%{r_prc_enter[13]}" if r_prc_enter[13] != 0 else "15A"
                    self.r_10.text = f" 22A\n%{r_prc_enter[14]}" if r_prc_enter[14] != 0 else "22A"
                    self.r_11.text = f" 42A\n%{r_prc_enter[15]}" if r_prc_enter[15] != 0 else "42A"
                for k in range(5, 16):
                    total_r_prc = total_r_prc + r_prc_enter[k]
                self.r_prc.text = f"%{round(total_r_prc, 2)}"

            if self.s_loads[0:5] != [0, 0, 0, 0, 0]:
                s_prc_enter = Calc.percentage(float(self.v.text), float(self.kva.text),
                                              float(self.pf.text.replace(',', '.')), self.s_calc_loads)
                total_s_prc = 0
                # print(s_prc_enter)
                if s_prc_enter[4] > s_prc_enter[3]:
                    # print("testtt")
                    self.s_1.text = f" 1,5A\n%{s_prc_enter[5]}" if s_prc_enter[5] != 0 else "1,5A"
                    self.s_2.text = f" 3A\n%{s_prc_enter[6]}" if s_prc_enter[6] != 0 else "3A"
                    self.s_3.text = f" 6A\n%{s_prc_enter[7]}" if s_prc_enter[7] != 0 else "6A"
                    self.s_4.text = f" 9A\n%{s_prc_enter[8]}" if s_prc_enter[8] != 0 else "9A"
                    self.s_5.text = f" 18A\n%{s_prc_enter[9]}" if s_prc_enter[9] != 0 else "18A"
                    self.s_6.text = f" 32A\n%{s_prc_enter[10]}" if s_prc_enter[10] != 0 else "32A"
                    self.s_7.text = f" 4A\n%{s_prc_enter[11]}" if s_prc_enter[11] != 0 else "4A"
                    self.s_8.text = f" 8A\n%{s_prc_enter[12]}" if s_prc_enter[12] != 0 else "8A"
                    self.s_9.text = f" 15A\n%{s_prc_enter[13]}" if s_prc_enter[13] != 0 else "15A"
                    self.s_10.text = f" 22A\n%{s_prc_enter[14]}" if s_prc_enter[14] != 0 else "22A"
                    self.s_11.text = f" 42A\n%{s_prc_enter[15]}" if s_prc_enter[15] != 0 else "42A"
                for k in range(5, 16):
                    total_s_prc = total_s_prc + s_prc_enter[k]
                self.s_prc.text = f"%{round(total_s_prc, 2)}"

            if self.t_loads[0:5] != [0, 0, 0, 0, 0]:
                # print("t_loads =", self.t_loads)
                # print("t_calc_loads =", self.t_calc_loads)
                t_prc_enter = Calc.percentage(float(self.v.text), float(self.kva.text),
                                              float(self.pf.text.replace(',', '.')), self.t_calc_loads)
                total_t_prc = 0
                if t_prc_enter[4] > t_prc_enter[3]:
                    self.t_1.text = f" 1,5A\n%{t_prc_enter[5]}" if t_prc_enter[5] != 0 else "1,5A"
                    self.t_2.text = f" 3A\n%{t_prc_enter[6]}" if t_prc_enter[6] != 0 else "3A"
                    self.t_3.text = f" 6A\n%{t_prc_enter[7]}" if t_prc_enter[7] != 0 else "6A"
                    self.t_4.text = f" 9A\n%{t_prc_enter[8]}" if t_prc_enter[8] != 0 else "9A"
                    self.t_5.text = f" 18A\n%{t_prc_enter[9]}" if t_prc_enter[9] != 0 else "18A"
                    self.t_6.text = f" 32A\n%{t_prc_enter[10]}" if t_prc_enter[10] != 0 else "32A"
                    self.t_7.text = f" 4A\n%{t_prc_enter[11]}" if t_prc_enter[11] != 0 else "4A"
                    self.t_8.text = f" 8A\n%{t_prc_enter[12]}" if t_prc_enter[12] != 0 else "8A"
                    self.t_9.text = f" 15A\n%{t_prc_enter[13]}" if t_prc_enter[13] != 0 else "15A"
                    self.t_10.text = f" 22A\n%{t_prc_enter[14]}" if t_prc_enter[14] != 0 else "22A"
                    self.t_11.text = f" 42A\n%{t_prc_enter[15]}" if t_prc_enter[15] != 0 else "42A"
                for k in range(5, 16):
                    total_t_prc = total_t_prc + t_prc_enter[k]
                self.t_prc.text = f"%{round(total_t_prc, 2)}"
        except ValueError as e:
            self.v.text = ''
            self.kva.text = ''
            self.pf.text = ''
            print("Wrong Input", e)

    def calculation(self, loads, phase):
        try:
            if phase == "r":
                if loads != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    if self.v.text != '' and self.kva.text != '' and self.pf.text != '':
                        self.prc_calculation = Calc.percentage(float(self.v.text), float(self.kva.text),
                                                               float(self.pf.text.replace(',', '.')), loads)
                elif loads == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    self.prc_calculation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                total_r_prc = 0
                for k in range(5, 16):
                    total_r_prc = total_r_prc + self.prc_calculation[k]
                if self.prc_calculation[4] > self.prc_calculation[3]:
                    self.r_1.text = f" 1,5A\n%{self.prc_calculation[5]}" if self.prc_calculation[
                                                                           5] != 0 else "1,5A"
                    self.r_2.text = f" 3A\n%{self.prc_calculation[6]}" if self.prc_calculation[
                                                                         6] != 0 else "3A"
                    self.r_3.text = f" 6A\n%{self.prc_calculation[7]}" if self.prc_calculation[
                                                                         7] != 0 else "6A"
                    self.r_4.text = f" 9A\n%{self.prc_calculation[8]}" if self.prc_calculation[
                                                                         8] != 0 else "9A"
                    self.r_5.text = f" 18A\n%{self.prc_calculation[9]}" if self.prc_calculation[
                                                                          9] != 0 else "18A"
                    self.r_6.text = f" 32A\n%{self.prc_calculation[10]}" if self.prc_calculation[
                                                                           10] != 0 else "32A"
                    self.r_7.text = f" 4A\n%{self.prc_calculation[11]}" if self.prc_calculation[
                                                                          11] != 0 else "4A"
                    self.r_8.text = f" 8A\n%{self.prc_calculation[12]}" if self.prc_calculation[
                                                                          12] != 0 else "8A"
                    self.r_9.text = f" 15A\n%{self.prc_calculation[13]}" if self.prc_calculation[
                                                                           13] != 0 else "15A"
                    self.r_10.text = f" 22A\n%{self.prc_calculation[14]}" if self.prc_calculation[
                                                                            14] != 0 else "22A"
                    self.r_11.text = f" 42A\n%{self.prc_calculation[15]}" if self.prc_calculation[
                                                                            15] != 0 else "42A"
                elif self.prc_calculation[3] >= self.prc_calculation[4]:
                    self.percentage_init()
                    self.r_1.text = self.r_1.text if self.prc_calculation[11] == 0 else "1,5A"
                    self.r_2.text = self.r_2.text if self.prc_calculation[12] == 0 else "3A"
                    self.r_3.text = self.r_3.text if self.prc_calculation[13] == 0 else "6A"
                    self.r_4.text = self.r_4.text if self.prc_calculation[14] == 0 else "9A"
                    self.r_5.text = self.r_5.text if self.prc_calculation[15] == 0 else "18A"

                    self.r_7.text = self.r_7.text if self.prc_calculation[
                                                                          11] != 0 else "4A"
                    self.r_8.text = f" 8A\n%{self.prc_calculation[12]}" if self.prc_calculation[
                                                                          12] != 0 else "8A"
                    self.r_9.text = f" 15A\n%{self.prc_calculation[13]}" if self.prc_calculation[
                                                                           13] != 0 else "15A"
                    self.r_10.text = f" 22A\n%{self.prc_calculation[14]}" if self.prc_calculation[
                                                                            14] != 0 else "22A"
                    self.r_11.text = f" 42A\n%{self.prc_calculation[15]}" if self.prc_calculation[
                                                                            15] != 0 else "42A"
                self.r_prc.text = f"%{round(total_r_prc, 2)}"

            elif phase == "s":
                if loads != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    if self.v.text != '' and self.kva.text != '' and self.pf.text != '':
                        self.prc_calculation = Calc.percentage(float(self.v.text), float(self.kva.text),
                                                               float(self.pf.text.replace(',', '.')), loads)
                elif loads == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    self.prc_calculation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                total_s_prc = 0
                for k in range(5, 16):
                    total_s_prc = total_s_prc + self.prc_calculation[k]
                if self.prc_calculation[4] > self.prc_calculation[3]:
                    self.s_1.text = f" 1,5A\n%{self.prc_calculation[5]}" if self.prc_calculation[
                                                                           5] != 0 else "1,5A"
                    self.s_2.text = f" 3A\n%{self.prc_calculation[6]}" if self.prc_calculation[
                                                                         6] != 0 else "3A"
                    self.s_3.text = f" 6A\n%{self.prc_calculation[7]}" if self.prc_calculation[
                                                                         7] != 0 else "6A"
                    self.s_4.text = f" 9A\n%{self.prc_calculation[8]}" if self.prc_calculation[
                                                                         8] != 0 else "9A"
                    self.s_5.text = f" 18A\n%{self.prc_calculation[9]}" if self.prc_calculation[
                                                                          9] != 0 else "18A"
                    self.s_6.text = f" 32A\n%{self.prc_calculation[10]}" if self.prc_calculation[
                                                                           10] != 0 else "32A"
                    self.s_7.text = f" 4A\n%{self.prc_calculation[11]}" if self.prc_calculation[
                                                                          11] != 0 else "4A"
                    self.s_8.text = f" 8A\n%{self.prc_calculation[12]}" if self.prc_calculation[
                                                                          12] != 0 else "8A"
                    self.s_9.text = f" 15A\n%{self.prc_calculation[13]}" if self.prc_calculation[
                                                                           13] != 0 else "15A"
                    self.s_10.text = f" 22A\n%{self.prc_calculation[14]}" if self.prc_calculation[
                                                                            14] != 0 else "22A"
                    self.s_11.text = f" 42A\n%{self.prc_calculation[15]}" if self.prc_calculation[
                                                                            15] != 0 else "42A"
                elif self.prc_calculation[3] >= self.prc_calculation[4]:
                    self.percentage_init()
                    self.s_1.text = self.s_1.text if self.prc_calculation[11] == 0 else "1,5A"
                    self.s_2.text = self.s_2.text if self.prc_calculation[12] == 0 else "3A"
                    self.s_3.text = self.s_3.text if self.prc_calculation[13] == 0 else "6A"
                    self.s_4.text = self.s_4.text if self.prc_calculation[14] == 0 else "9A"
                    self.s_5.text = self.s_5.text if self.prc_calculation[15] == 0 else "18A"

                    self.s_7.text = f" 4A\n%{self.prc_calculation[11]}" if self.prc_calculation[
                                                                          11] != 0 else "4A"
                    self.s_8.text = f" 8A\n%{self.prc_calculation[12]}" if self.prc_calculation[
                                                                          12] != 0 else "8A"
                    self.s_9.text = f" 15A\n%{self.prc_calculation[13]}" if self.prc_calculation[
                                                                           13] != 0 else "15A"
                    self.s_10.text = f" 22A\n%{self.prc_calculation[14]}" if self.prc_calculation[
                                                                            14] != 0 else "22A"
                    self.s_11.text = f" 42A\n%{self.prc_calculation[15]}" if self.prc_calculation[
                                                                            15] != 0 else "42A"
                self.s_prc.text = f"%{round(total_s_prc, 2)}"

            elif phase == "t":
                if loads != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    if self.v.text != '' and self.kva.text != '' and self.pf.text != '':
                        self.prc_calculation = Calc.percentage(float(self.v.text), float(self.kva.text),
                                                               float(self.pf.text.replace(',', '.')), loads)
                elif loads == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    self.prc_calculation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                total_t_prc = 0
                for k in range(5, 16):
                    total_t_prc = total_t_prc + self.prc_calculation[k]
                if self.prc_calculation[4] > self.prc_calculation[3]:
                    self.t_1.text = f" 1,5A\n%{self.prc_calculation[5]}" if self.prc_calculation[
                                                                           5] != 0 else "1,5A"
                    self.t_2.text = f" 3A\n%{self.prc_calculation[6]}" if self.prc_calculation[
                                                                         6] != 0 else "3A"
                    self.t_3.text = f" 6A\n%{self.prc_calculation[7]}" if self.prc_calculation[
                                                                         7] != 0 else "6A"
                    self.t_4.text = f" 9A\n%{self.prc_calculation[8]}" if self.prc_calculation[
                                                                         8] != 0 else "9A"
                    self.t_5.text = f" 18A\n%{self.prc_calculation[9]}" if self.prc_calculation[
                                                                          9] != 0 else "18A"
                    self.t_6.text = f" 32A\n%{self.prc_calculation[10]}" if self.prc_calculation[
                                                                           10] != 0 else "32A"
                    self.t_7.text = f" 4A\n%{self.prc_calculation[11]}" if self.prc_calculation[
                                                                          11] != 0 else "4A"
                    self.t_8.text = f" 8A\n%{self.prc_calculation[12]}" if self.prc_calculation[
                                                                          12] != 0 else "8A"
                    self.t_9.text = f" 15A\n%{self.prc_calculation[13]}" if self.prc_calculation[
                                                                           13] != 0 else "15A"
                    self.t_10.text = f" 22A\n%{self.prc_calculation[14]}" if self.prc_calculation[
                                                                            14] != 0 else "22A"
                    self.t_11.text = f" 42A\n%{self.prc_calculation[15]}" if self.prc_calculation[
                                                                            15] != 0 else "42A"
                elif self.prc_calculation[3] >= self.prc_calculation[4]:
                    self.percentage_init()
                    self.t_1.text = self.t_1.text if self.prc_calculation[11] == 0 else "1,5A"
                    self.t_2.text = self.t_2.text if self.prc_calculation[12] == 0 else "3A"
                    self.t_3.text = self.t_3.text if self.prc_calculation[13] == 0 else "6A"
                    self.t_4.text = self.t_4.text if self.prc_calculation[14] == 0 else "9A"
                    self.t_5.text = self.t_5.text if self.prc_calculation[15] == 0 else "18A"

                    self.t_7.text = f" 4A\n%{self.prc_calculation[11]}" if self.prc_calculation[
                                                                          11] != 0 else "4A"
                    self.t_8.text = f" 8A\n%{self.prc_calculation[12]}" if self.prc_calculation[
                                                                          12] != 0 else "8A"
                    self.t_9.text = f" 15A\n%{self.prc_calculation[13]}" if self.prc_calculation[
                                                                           13] != 0 else "15A"
                    self.t_10.text = f" 22A\n%{self.prc_calculation[14]}" if self.prc_calculation[
                                                                            14] != 0 else "22A"
                    self.t_11.text = f" 42A\n%{self.prc_calculation[15]}" if self.prc_calculation[
                                                                            15] != 0 else "42A"
                self.t_prc.text = f"%{round(total_t_prc, 2)}"
        except ValueError as e:
            self.v.text = ''
            self.kva.text = ''
            self.pf.text = ''
            print("Wrong Input", e)
            pass

    def on_enter(self, *args):
        if self.thread_pause is True and self.is_trying_to_connect is True:
            print("y")
            #Clock.schedule_once(self.tcp_thread_start, 0.01)  # Try to connect again.
            self.is_trying_to_connect = False
            self.thread_pause = False
        if self.app_start_setup is True:     # Setting threads for once.
            self.app_start_setup = False
            Clock.schedule_once(self.getip, 0.01)  # At the start, get IP from txt file
            #Clock.schedule_once(self.tcp_thread_start, 0.01)  # Start tcp thread
            #Clock.schedule_interval(self.connection_check, 0.5)  # Check connection if its still on going.

    def getip(self, dt):
        # Edit spesific line
        a = open("ip.txt", "r").read().split('\n')  # Read .txt file
        self.v.text = a[1]
        self.kva.text = a[2]
        self.pf.text = a[3]
        self.box.text = open("ip.txt", "r").read().split('\n')[0]

    def tick(self, dt):
        self.status.source = "tick.png"
        self.status2.source = "tick.png"

    def cross(self, dt):
        self.status.source = "cross.png"
        self.status2.source = "cross.png"

    def tcp_thread_start(self, *args):
        y = threading.Thread(target=self.tcp_thread, daemon=True)  # Setup thread
        y.start()  # Starts thread

    def tcp_thread(self):
        global s
        print("test1\n")
        func = [self.r_onof, self.s_onof, self.t_onof,
                self.r_1, self.r_2, self.r_3, self.r_4, self.r_5, self.r_6, self.r_7, self.r_8, self.r_9,
                self.r_10, self.r_11,
                self.s_1, self.s_2, self.s_3, self.s_4, self.s_5, self.s_6, self.s_7, self.s_8, self.s_9,
                self.s_10, self.s_11,
                self.t_1, self.t_2, self.t_3, self.t_4, self.t_5, self.t_6, self.t_7, self.t_8, self.t_9,
                self.t_10, self.t_11, self.masteronof]

        var = [b'281010', b'291010', b'521010', b'531010', b'761010', b'771010', b'301010', b'311010', b'321010',
               b'331010', b'341010', b'351010', b'361010', b'371010', b'381010', b'391010', b'401010', b'411010',
               b'421010', b'431010', b'441010', b'451010', b'461010', b'471010', b'481010', b'491010', b'501010',
               b'511010', b'541010', b'551010', b'561010', b'571010', b'581010', b'591010', b'601010', b'611010',
               b'621010', b'631010', b'641010', b'651010', b'661010', b'671010', b'681010', b'691010', b'701010',
               b'711010', b'721010', b'731010', b'741010', b'751010', b'781010', b'791010', b'801010', b'811010',
               b'821010', b'831010', b'841010', b'851010', b'861010', b'871010', b'881010', b'891010', b'901010',
               b'911010', b'921010', b'931010', b'941010', b'951010', b'961010', b'971010', b'981010', b'991010']

        varr = ["q", "Q", "f", "F", "n", "N", "w", "W", "e", "E", "r", "R", "t", "T", "y", "Y", "u", "U", "o", "O",
                "p", "P", "a", "A", "s", "S", "d", "D", "g", "G", "h", "H", "j", "J", "k", "K", "l", "L", "i", "I",
                "z", "Z", "x", "X", "c", "C", "v", "V", "b", "B", "m", "M", "1", "!", "2", "'", "3", "^", "4", "+",
                "5", "%", "6", "&", "7", "/", "8", "(", "9", ")", "0", "=", "{", "}"]

        currents = [1.5, 3, 6, 9, 18, 32, 4, 8, 15, 22, 42]

        try:
            print("test2")
            host = self.box.text  # Get IP from TextInput.
            port = 10001
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print("test3")
                s.connect((host, port))  # Try to connect
                print("test4")
                # If connected:
                self.is_trying_to_connect = False
                Clock.schedule_once(self.tick)  # Make Connection status ON (Green tick)

                # Edit spesific line
                a = open("ip.txt", "r").read().split('\n')  # Read .txt file
                a[0] = self.box.text  # Write to first line
                a = "\n".join(a)
                f = open("ip.txt", "w")
                f.write(a)  # Save the file
                f.close()
                while True:
                    print("test5")
                    data = s.recv(2)  # Receive data
                    print("test6")
                    datastr = data.decode("utf-8")
                    print(datastr)

                    a = []
                    for x in range(3, 36):      # Button states
                        a.append(func[x].background_color)

                    for x in range(0, 74):
                        if varr[x] in datastr:  # Button state
                            if (x % 2) == 0:
                                func[int(x/2)].background_color = green  # Button State - ON
                            elif (x % 2) == 1:
                                func[int((x-1)/2)].background_color = red  # Button State - OFF

                    for x in range(3, 36):      # Changed Button States
                        if func[x].background_color != a[x-3]:      # If button state is changed,
                            if func[x].background_color == green:       # Button is ON

                                if 3 <= x <= 13:        # R Phase
                                    self.r_loads[x-3] = currents[x-3]
                                    self.r_calc_loads = self.r_loads.copy()

                                    for i in range(0, 11):
                                        if 0 <= i <= 4:
                                            if self.r_loads[i] == 0:
                                                self.r_calc_loads[i+6] = 0

                                        if 6 <= i <= 10:
                                            if self.r_loads[i-6] == 0:
                                                self.r_calc_loads[i] = 0

                                            if self.r_loads[i] != 0:
                                                self.r_calc_loads[i-6] = 0
                                    self.calculation(self.r_calc_loads, "r")

                                if 14 <= x <= 24:       # S Phase
                                    self.s_loads[x - 14] = currents[x - 14]
                                    self.s_calc_loads = self.s_loads.copy()

                                    for i in range(0, 11):
                                        if 0 <= i <= 4:
                                            if self.s_loads[i] == 0:
                                                self.s_calc_loads[i + 6] = 0

                                        if 6 <= i <= 10:
                                            if self.s_loads[i - 6] == 0:
                                                self.s_calc_loads[i] = 0

                                            if self.s_loads[i] != 0:
                                                self.s_calc_loads[i - 6] = 0
                                    self.calculation(self.s_calc_loads, "s")

                                if 25 <= x <= 35:       # T Phase
                                    self.t_loads[x - 25] = currents[x - 25]
                                    self.t_calc_loads = self.t_loads.copy()

                                    for i in range(0, 11):
                                        if 0 <= i <= 4:
                                            if self.t_loads[i] == 0:
                                                self.t_calc_loads[i + 6] = 0

                                        if 6 <= i <= 10:
                                            if self.t_loads[i - 6] == 0:
                                                self.t_calc_loads[i] = 0

                                            if self.t_loads[i] != 0:
                                                self.t_calc_loads[i - 6] = 0
                                    self.calculation(self.t_calc_loads, "t")

                            if func[x].background_color == red:         # Button is OFF
                                if 3 <= x <= 13:  # R Phase
                                    self.r_loads[x - 3] = 0
                                    self.r_calc_loads = self.r_loads.copy()

                                    for i in range(0, 11):
                                        if 0 <= i <= 4:
                                            if self.r_loads[i] == 0:
                                                self.r_calc_loads[i + 6] = 0

                                        if 6 <= i <= 10:
                                            if self.r_loads[i - 6] == 0:
                                                self.r_calc_loads[i] = 0

                                            if self.r_loads[i] != 0:
                                                self.r_calc_loads[i - 6] = 0
                                    self.calculation(self.r_calc_loads, "r")

                                if 14 <= x <= 24:  # S Phase
                                    self.s_loads[x - 14] = 0
                                    self.s_calc_loads = self.s_loads.copy()

                                    for i in range(0, 11):
                                        if 0 <= i <= 4:
                                            if self.s_loads[i] == 0:
                                                self.s_calc_loads[i + 6] = 0

                                        if 6 <= i <= 10:
                                            if self.s_loads[i - 6] == 0:
                                                self.s_calc_loads[i] = 0

                                            if self.s_loads[i] != 0:
                                                self.s_calc_loads[i - 6] = 0
                                    self.calculation(self.s_calc_loads, "s")

                                if 25 <= x <= 35:  # T Phase
                                    self.t_loads[x - 25] = 0
                                    self.t_calc_loads = self.t_loads.copy()

                                    for i in range(0, 11):
                                        if 0 <= i <= 4:
                                            if self.t_loads[i] == 0:
                                                self.t_calc_loads[i + 6] = 0

                                        if 6 <= i <= 10:
                                            if self.t_loads[i - 6] == 0:
                                                self.t_calc_loads[i] = 0

                                            if self.t_loads[i] != 0:
                                                self.t_calc_loads[i - 6] = 0
                                    self.calculation(self.t_calc_loads, "t")

                    if self.is_connected is False:  # If connection lost:
                        print("Connection lost.")
                        break
            Clock.schedule_once(self.cross)  # Make Connection status OFF (Red cross)
            Clock.schedule_once(self.tcp_thread_start, 0.01)  # Try to connect again.

        except Exception as e:  # If it couldn't connect
            self.is_connected = False
            self.is_trying_to_connect = True
            print(self.thread_pause)
            if self.thread_pause is False:
                Clock.schedule_once(self.tcp_thread_start, 0.01)  # Try to connect again.
            Clock.schedule_once(self.cross)  # Make Connection status OFF (Red cross)
            print("crash", e)

    def send(self, x):
        try:
            s.sendall(bytes(x, 'ascii'))    # Send button's status.

        except Exception as e:      # If connection has lost:
            self.is_connected = False
            self.status2.source = "cross.png"   # Make Connection status OFF (Red cross)
            print("fail,", e)

    def master_onof(self, x):
        try:
            if x is False:  # If Master button is OFF
                s.sendall(bytes("q", 'ascii'))      # Make all on/off buttons ON.
                s.sendall(bytes("f", 'ascii'))      # Make all on/off buttons ON.
                s.sendall(bytes("n", 'ascii'))      # Make all on/off buttons ON.
            elif x is True:  # If Master button is ON
                s.sendall(bytes("Q", 'ascii'))      # Make all on/off buttons OFF.
                s.sendall(bytes("F", 'ascii'))      # Make all on/off buttons OFF.
                s.sendall(bytes("N", 'ascii'))      # Make all on/off buttons OFF.
        except Exception as e:      # If connection has lost:
            self.is_connected = False
            self.status2.source = "cross.png"   # Make Connection status OFF (Red cross)
            print("fail,", e)

    def connection_check(self, dt):
        global s
        print("test7")
        try:
            if self.is_connected:
                s.sendall(b'\x11')     # Sending a byte to check if connection is lost.
                print("test8")
                self.is_connected = True     # Connection is on going.
                time.sleep(0.05)
            elif not self.is_connected:
                print("passed check")
                pass

        except:
            self.is_connected = False    # Connection is lost.
            print(f"Connection is lost, is_connected = {self.is_connected}")


class OptionPage(Screen):

    def save(self):

        # Edit spesific line
        a = open("ip.txt", "r").read().split('\n')  # Read .txt file
        a[0] = self.box.text  # Write to first line
        a = "\n".join(a)
        f = open("ip.txt", "w")
        f.write(a)  # Save the file
        f.close()
    pass


class MyApp(App):
    Window.minimum_height = 720
    Window.minimum_width = 1280
    Window.size = (1280, 720)
    pass


if __name__ == '__main__':
    MyApp().run()
