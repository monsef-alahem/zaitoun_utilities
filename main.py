'''
author  :   monsef alahem
email   :   m.alahem09@gmail.com
version :   1.0
start   :   09-08-2019

'''
# import os
# os.environ['KIVY_AUDIO'] = 'sdl2'
import math
import os
# #sdl2, gstplayer, ffpyplayer, pygame, avplayer
# os.environ["KIVY_AUDIO"] = "sdl2"
# from kivy.core.window import Window
# Window.fullscreen = False

# from playsound import playsound
# playsound('test.mp3')

# import geocoder
# g = geocoder.ip('me')
# print(g.latlng)

import kivy
kivy.require("1.11.1")

#necesary for utf
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

# from kivy.graphics.transformation import Matrix
# from kivy.graphics.opengl import *
# from kivy.graphics import *
from kivy.animation import Animation
from kivy.properties import NumericProperty


from pyIslam.praytimes import PrayerConf, Prayer
from pyIslam.hijri import HijriDate
from pyIslam.qiblah import Qiblah
from pyIslam.mirath import Mirath
from pyIslam.zakat import Zakat
from datetime import date, time, datetime
# import threading

# import zakat, mirath, qiblah, hijri, praytimes

from kivy.app import App
from kivy.clock import Clock
from kivy.compat import string_types
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.metrics import sp, dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
# from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty
from kivy.uix.accordion import Accordion
# import geocoder

converted_date = []

mirath = Mirath()
zakat = Zakat()

# for keyboard writing
target_widget = None

eng = 0
ar = 1

latitude = '0'
longitude = '0'
timezone = '0'
fajr_isha_method = ' '
asr_fiqh = ' '

isha_ref = {
    'University of Islamic Sciences, Karachi' : 1,
    'Muslim World League' : 2,
    'Egyptian General Authority of Survey' : 3,
    'Umm al-Qura University, Makkah' : 4,
    'Islamic Society of North America' : 5
}


asr_ref = {
    'Shafii' : 1,
    'Hanafi' : 2
}



# print('\n---testing mirath---\n')

# test = Mirath()
# # test.add_relative('husband')
# # test.add_relative('wife')
# # test.add_relative('father')
# # test.add_relative('maternal_grandmother')
# # test.add_relative('mother')
# # test.add_relative('paternal_grandmother')
# # test.add_relative('son', 2)
# test.add_relative('father')

# # test.add_relative('grandfather')
# # test.add_relative('maternal_brother', 3)
# # test.add_relative('grandson')
# # test.add_relative('granddaughter')
# test.add_relative('son')
# test.add_relative('daughter', 3)
# test.calculte_mirath()
# test.display_shares()




lang = {
# '*Zaitoun utilities*': ['*Zaitoun utilities*',u''],
# 'date converter': ['date converter',u''],
# 'prayer time': [u'prayer time',u''],
# 'mirath calculator': [u'mirath calculator',u''],
# 'zakat calculator': [u'zakat calculator',u''],
# 'return': [u'return',u''],
# 'converted date': [u'converted date',u''],
# 'delete': [u'delete',u''],
# 'hijri': [u'hijri',u''],
# 'gregorian': [u'gregorian',u''],
# 'sobh': [u'sobh',u''],
# 'choroq': [u'choroq',u''],
# 'dohr': [u'dohr',u''],
# 'asr': [u'asr',u''],


# taa
# ufe90 replaced by ufe8f
# dha
# ufec8 replaced by ufec5
# ta
# ufec2 replaced by ufec1

'ok' : [u'ok', u'\ufed5\ufed3\ufe8d\ufeed\ufee3'],
'*Zaitoun utilities*' : [u'*Zaitoun utilities*', u'\u002a\ufee5\ufeed\ufe98\ufef3\ufeaf\ufedf\ufe8d\u0020\ufe95\ufe8d\ufeed\ufea9\ufe83\u002a'],
'date converter' : [u'date converter', u'\ufea6\ufef3\ufead\ufe8e\ufe98\ufedf\ufe8d\u0020\ufedd\ufeed\ufea4\ufee3'],
'prayer time' : [u'prayer time', u'\ufe93\ufefc\ufebc\ufedf\ufe8d\u0020\ufe95\ufe8e\ufed7\ufeed\ufe83'],
'mirath calculator' : [u'mirath calculator', u'\ufe99\ufe8d\ufead\ufef4\ufee4\ufedf\ufe8d\u0020\ufe8f\ufeb3\ufe8e\ufea3'],
'zakat calculator' : [u'zakat calculator', u'\ufe93\ufe8e\ufedb\ufeaf\ufedf\ufe8d\u0020\ufe8f\ufeb3\ufe8e\ufea3'],
'return' : [u'return', u'\ufec9\ufeed\ufe9f\ufead'],
'converted date' : [u'converted date', u'\ufedd\ufeed\ufea4\ufee4\ufedf\ufe8d\u0020\ufea6\ufef3\ufead\ufe8e\ufe98\ufedf\ufe8d'],
'delete' : [u'delete', u'\ufed1\ufea9\ufea3'],
'hijri' : [u'hijri', u'\ufef1\ufead\ufea0\ufeeb'],
'gregorian' : [u'gregorian', u'\ufef1\ufea9\ufefc\ufee3'],
'sobh' : [u'sobh', u'\ufea2\ufe92\ufebc\ufedf\ufe8d'],
'choroq' : [u'choroq', u'\ufed5\ufeed\ufead\ufeb8\ufedf\ufe8d'],
'dohr' : [u'dohr', u'\ufead\ufeec\ufec5\ufedf\ufe8d'],
'asr' : [u'asr', u'\ufead\ufebc\ufecc\ufedf\ufe8d'],

'maghrib' : [u'maghrib', u'\ufe8f\ufead\ufed0\ufee4\ufedf\ufe8d'],
'ishaa' : [u'ishaa', u'\ufe80\ufe8e\ufeb8\ufecc\ufedf\ufe8d'],
'calculate' : [u'calculate', u'\ufe8f\ufe8e\ufeb4\ufea3'],
'qibla' : [u'qibla', u'\ufe94\ufee0\ufe92\ufed8\ufedf\ufe8d'],
'timezone' : [u'timezone', u'\ufe94\ufef4\ufee8\ufee3\ufeaf\ufedf\ufe8d\u0020\ufe94\ufed8\ufec1\ufee8\ufee4\ufedf\ufe8d'],
'longitude' : [u'longitude', u'\ufebd\ufead\ufecc\ufedf\ufe8d\u0020\ufec1\ufea7'],
'latitude' : [u'latitude', u'\ufedd\ufeed\ufec1\ufedf\ufe8d\u0020\ufec1\ufea7'],
"University of Islamic Sciences, Karachi" : [u"University of Islamic Sciences, Karachi", u'\ufef2\ufe9f\ufe8d\ufead\ufedc\ufedf\ufe8d\u0020\u002c\ufe94\ufef4\ufee3\ufefc\ufeb3\ufef9\ufe8d\u0020\ufee1\ufeed\ufee0\ufecc\ufedf\ufe8d\u0020\ufe94\ufecc\ufee3\ufe8e\ufe9f'],
"Muslim World League" : [u"Muslim World League", u'\ufef2\ufee3\ufefc\ufeb3\ufef9\ufe8d\u0020\ufee1\ufedf\ufe8e\ufecc\ufedf\ufe8d\u0020\ufe94\ufec1\ufe91\ufe8d\ufead'],
"Egyptian General Authority of Survey" : [u'Egyptian General Authority of Survey', u'\ufe94\ufea3\ufe8e\ufeb4\ufee4\ufee0\ufedf\u0020\ufe94\ufee3\ufe8e\ufecc\ufedf\ufe8d\u0020\ufe94\ufef3\ufead\ufebc\ufee4\ufedf\ufe8d\u0020\ufe94\ufe8c\ufef4\ufeec\ufedf\ufe8d'],
"Umm al-Qura University, Makkah" : [u'Umm al-Qura University, Makkah', u'\ufe94\ufedc\ufee3\u0020\u002c\ufeef\ufead\ufed8\ufedf\ufe8d\u0020\ufee1\ufe83\u0020\ufe94\ufecc\ufee3\ufe8e\ufe9f'],
"Islamic Society of North America" : [u'Islamic Society of North America', u'\ufe94\ufef4\ufedf\ufe8e\ufee4\ufeb8\ufedf\ufe8d\u0020\ufe94\ufef4\ufedc\ufef3\ufead\ufee3\ufef7\ufe8d\u0020\ufe94\ufef4\ufee3\ufefc\ufeb3\ufef9\ufe8d\u0020\ufe94\ufedb\ufe8d\ufead\ufeb8\ufedf\ufe8d'],

'asr method' : [u'asr method', u'\ufead\ufebc\ufecc\ufedf\ufe8d\u0020\ufe8f\ufeeb\ufeab\ufee3'],
'ishaa method' : [u'ishaa method', u'\ufe80\ufe8e\ufeb8\ufecc\ufedf\ufe8d\ufeed\u0020\ufead\ufea0\ufed4\ufedf\ufe8d\u0020\ufe94\ufed8\ufef3\ufead\ufec1'],
# 'ishaa method' : [u'ishaa method', u'\ufe8d\u0020\ufe8f\ufeeb\ufeab\ufee3'],

'Hanafi' : [u'Hanafi', u'\ufef2\ufed4\ufee8\ufea3'],
'Shafii' : [u'Shafii', u'\ufef2\ufecc\ufed3\ufe8e\ufeb7'],

'husband' : [u'husband', u'\ufe9d\ufeed\ufeaf'],
'wife' : [u'wife', u'\ufe94\ufe9f\ufeed\ufeaf'],
'son' : [u'son', u'\ufea9\ufedf\ufeed'],
'daughter' : [u'daughter', u'\ufe95\ufee8\ufe91'],
'father' : [u'father', u'\ufe8f\ufe83'],
'mother' : [u'mother', u'\ufee1\ufe83'],
'grandson' : [u'grandson', u'\ufea9\ufedf\ufeed\ufedf\ufe8d\u0020\ufee5\ufe91\ufe87'],
'granddaughter' : [u'granddaughter', u'\ufea9\ufedf\ufeed\ufedf\ufe8d\u0020\ufe95\ufee8\ufe91'],
'grandfather' : [u'grandfather', u'\ufe8f\ufef7\u0020\ufea9\ufe9f'],
'paternal_grandmother' : [u'paternal_grandmother', u'\ufe8f\ufef7\u0020\ufe93\ufea9\ufe9f'],
'maternal_grandmother' : [u'maternal_grandmother', u'\ufee1\ufef7\u0020\ufe93\ufea9\ufe9f'],

'brother' : [u'brother', u'\ufea5\ufe83'],
'sister' : [u'sister', u'\ufe95\ufea7\ufe83'],
'paternal_brother' : [u'paternal_brother', u'\ufe8f\ufef7\u0020\ufea5\ufe83'],
'paternal_sister' : [u'paternal_sister', u'\ufe8f\ufef7\u0020\ufe95\ufea7\ufe83'],
'maternal_brother' : [u'maternal_brother', u'\ufee1\ufef7\u0020\ufea5\ufe83'],
'maternal_sister' : [u'maternal_sister', u'\ufee1\ufef7\u0020\ufe95\ufea7\ufe83'],
'nephew' : [u'nephew', u'\ufea5\ufef7\ufe8d\u0020\ufee5\ufe91\ufe87'],
'paternal_nephew' : [u'paternal_nephew', u'\ufea5\ufef7\ufe8d\u0020\ufee5\ufe91\ufe87\u0020\ufee5\ufe91\ufe87'],
'nephew_son' : [u'nephew_son', u'\ufe8f\ufef7\u0020\ufea5\ufef7\ufe8d\u0020\ufee5\ufe91\ufe87'],
'paternal_nephew_son' : [u'paternal_nephew_son', u'\ufe8f\ufef7\u0020\ufea5\ufef7\ufe8d\u0020\ufee5\ufe91\ufe87\u0020\ufee5\ufe91\ufe87'],
'paternal_uncle' : [u'paternal_uncle', u'\ufee1\ufecb'],
'cousin' : [u'cousin', u'\ufee1\ufecb\u0020\ufee5\ufe91\ufe87'],
'paternal_cousin' : [u'paternal_cousin', u'\ufe8f\ufef7\u0020\ufee1\ufecc\ufedf\ufe8d\u0020\ufee5\ufe91\ufe87'],
'cousin_son' : [u'cousin_son', u'\ufee1\ufecb\u0020\ufee5\ufe91\ufe87\u0020\ufee5\ufe91\ufe87'],
'paternal_cousin_son' : [u'paternal_cousin_son', u'\ufe8f\ufef7\u0020\ufee1\ufecc\ufedf\ufe8d\u0020\ufee5\ufe91\ufe87\u0020\ufee5\ufe91\ufe87'],
'cousin_grandson' : [u'cousin_grandson', u'\ufee1\ufecc\ufedf\ufe8d\u0020\ufee5\ufe91\ufe87\u0020\ufee5\ufe91\ufe87\u0020\ufee5\ufe91\ufe87'],
'paternal_cousin_grandson' : [u'paternal_cousin_grandson', u'\ufe8f\ufef7\u0020\ufee1\ufecc\ufedf\ufe8d\u0020\ufee5\ufe91\ufe87\u0020\ufee5\ufe91\ufe87\u0020\ufee5\ufe91\ufe87'],
'paternal_paternal_uncle' : [u'paternal_paternal_uncle', u'\ufe8f\ufef7\u0020\ufee1\ufecb'],

'add relative' : [u'add relative', u'\ufea9\ufead\ufed3\u0020\ufe94\ufed3\ufe8e\ufebf\ufe87'],
'clean' : [u'clean', u'\ufecd\ufe8d\ufead\ufed3\ufe87'],
'config' : [u'config', u'\ufea9\ufe8d\ufea9\ufecb\ufe87'],

'steps' : [u'steps', u'\ufe94\ufea0\ufef4\ufe98\ufee8\ufedf\ufe8d'],
'results' : [u'results', u'\ufe95\ufe8d\ufeed\ufec1\ufea8\ufedf\ufe8d'],

'touch here' : [u'touch here', u'\ufe8e\ufee8\ufeeb\u0020\ufec1\ufed0\ufec5\ufe8d'],

'money' : [u'money', u'\ufedd\ufe8e\ufee4\ufedf\ufe8d'],
'harvest' : [u'harvest', u'\ufedd\ufeed\ufebc\ufea4\ufee4\ufedf\ufe8d'],


'artificial irigation' : [u'artificial irigation', u'\ufef2\ufecc\ufef4\ufe92\ufec1\u0020\ufef1\ufead\ufedf\ufe8d'],
'natural irigation' : [u'natural irigation', u'\ufef2\ufe8b\ufe8e\ufed8\ufee0\ufe97\u0020\ufead\ufef4\ufecf\u0020\ufef1\ufead\ufedf\ufe8d'],
'hanafi nisab' : [u'hanafi nisab', u'\ufef2\ufed4\ufee8\ufea4\ufedf\ufe8d\u0020\ufe8f\ufe8e\ufebc\ufee8\ufedf\ufe8d'],
'others nisab' : [u'others nisab', u'\ufe94\ufee3\ufe8e\ufecc\ufedf\ufe8d\u0020\ufe8f\ufeb4\ufea3\u0020\ufe8f\ufe8e\ufebc\ufee8\ufedf\ufe8d']



}




def get_key(self, dict, myval):
    for key, val in dict.items():
        if val == myval:
            # print(key)
            return key


def get_key_tab(self, dict, myval, idx):
    for key, tab in dict.items():
        if tab[idx] == myval:
            # print(key)
            return key

        # for val in range(len(tab)):
        #     print(key)
        #     if val == myval:
        #         return key





class Date:
    _hd = 0
    _hm = 0
    _hy = 0

    _gd = 0
    _gm = 0
    _gy = 0

    _day_week = 5

    _julien_day = 1

    weekday = ["dimanche", "lundi", "mardi", "mercredi", "jeudi",
     "vendredi", "samedi"]
    hijri_month = ["moharam", "safar", "rabii I", "rabii II", "joumada I", "joumada II",
     "rajab", "chaaban", "ramadan", "chawal", "dou al qiida", "dou al hijaa"]
    gregorien_month = ["janvier", "fevrier", "mars", "avril", "mai",
     "juin", "juillet","aout","septembre","octobre","novembre","decembre"]

    #def __init__(self, **kwargs):
    def __init__(self, type, day, month, year):

        if type == 'h': 
            self._hd = day
            self._hm = month
            self._hy = year
            self.hijri_to_julien()
            self.julien_to_gregorien()

        if type == 'g':
            self._gd = day
            self._gm = month
            self._gy = year
            self.gregorien_to_julien()
            self.julien_to_hijri()
            
    def hijri_to_julien(self):
        YYH = self._hy
        MMH = self._hm
        DDH = self._hd
        KH1 = math.floor((YYH * 10631 + 58442583)/30)
        KH2 = math.floor((MMH * 325 - 320)/11)
        KH3 = DDH - 1
        self._julien_day = KH1 + KH2 + KH3
        KHS1 = (self._julien_day + 1.5)
        KHS2 = (KHS1/7)
        KHS3 = KHS2 - math.floor(KHS2)
        self._day_week = round(KHS3*7 + 0.000000000317) - 1
        self._hy = YYH
        self._hm = MMH
        self._hd = DDH

    def julien_to_gregorien(self):
        Z = math.floor(self._julien_day+0.5)
        F = self._julien_day+0.5 - Z
        if Z < 2299161:
            A = Z
        else:
            I = math.floor((Z - 1867216.25)/36524.25)
            A = Z + 1 + I - math.floor(I/4)
        
        B = A + 1524
        C = math.floor((B - 122.1)/365.25)
        D = math.floor(365.25 * C)
        T = math.floor((B - D)/ 30.6001)
        RJ = B - D - math.floor(30.6001 * T) + F
        JJ = math.floor(RJ)
        if T < 13.5:
            MM = T - 1
        else:
            if T > 13.5:
                MM = T - 13 
        if MM > 2.5:
            AA = C - 4716 
        else:
            if MM < 2.5: 
                AA = C - 4715

        self._gd = JJ
        self._gm = MM
        self._gy = AA

    def gregorien_to_julien(self):
        YY = self._gy
        MM = self._gm
        DD = self._gd

        GGG = 1
        if YY < 1582:
            GGG = 0
        if YY <= 1582 and MM < 10:
            GGG = 0
        if YY <= 1582 and MM == 10 and DD < 5:
            GGG = 0
        self._julien_day = -1 * math.floor(7 * (math.floor((MM + 9) / 12) + YY) / 4)
        S = 1
        if (MM - 9)<0:
            S=-1
        A = abs(MM - 9)
        J1 = math.floor(YY + S * math.floor(A / 7))
        J1 = -1 * math.floor((math.floor(J1 / 100) + 1) * 3 / 4)
        self._julien_day = self._julien_day + math.floor(275 * MM / 9) + DD + (GGG * J1)
        self._julien_day = self._julien_day + 1721027 + 2 * GGG + 367 * YY - 0.5
        K1 = (self._julien_day + 1.5)
        K2 = (K1/7)
        K3 = K2 - math.floor(K2)
        self._day_week = round(K3*7 + 0.000000000317)
        self._gy = YY
        self._gm = MM
        self._gd = DD

    def julien_to_hijri(self):
        Z = (self._julien_day + 0.5)
        AH = math.floor((Z * 30 - 58442554)/10631)
        R2 = Z - math.floor((AH * 10631 + 58442583)/30)
        M = math.floor((R2 * 11 + 330)/325)
        R1 = R2 - math.floor((M * 325 - 320)/11)
        J = R1 +1
        self._hy = AH
        self._hm = M
        self._hd = J
    
    def check_hijri_date(self,day,month):
        if month > 12 or month <= 0:
            return False
        if day > 30 or day <= 0:
            return False
        return True

    def check_gregorien_date(self,day,month):
        months = [31,28,31,30,31,30,31,31,30,31,30,31]
        if month > 12 or month <= 0:
            return False
        if day > 0 and day <= months[int(month)-1] and month <= 12 and month > 0:
            return True
        return False

    def tell_day(self):
        if not self.check_gregorien_date(self._gd,self._gm):
            return 'invalid date'
        if not self.check_gregorien_date(self._hd,self._hm):
            return 'invalid date'
        return str(self.weekday[int(self._day_week)])\
        + ' '\
        + str(int(self._hd))\
        + ' '\
        + str(self.hijri_month[int(self._hm)-1])\
        + ' '\
        + str(int(self._hy))\
        + ' / '\
        + str(int(self._gd))\
        + ' '\
        + str(self.gregorien_month[int(self._gm)-1])\
        + ' '\
        + str(int(self._gy))\


#build app with kv language
cvrt = '''
#: import asr_ref __main__.asr_ref
#: import isha_ref __main__.isha_ref
#: import lang __main__.lang

#: import ar __main__.ar
#: import eng __main__.eng


<Zaitoun>:
    
    #menu
    FloatLayout:
        id: menu
        # text: 'menu'
        # position and size to the parent, root in this case
        size_hint: (1, 1)
        pos_hint: {'x':0, 'y':.0}
        orientation: 'vertical'
        #opacity: 1 if root.ismenu else 0

        # canvas:
        #     Rectangle:
        #         pos: self.pos
        #         size: self.size
        #         source: 'zaitoun.png'
    
        # BoxLayout:
        #     id: logo
        #     pos_hint: {'x':.45, 'y':.78}
        #     size_hint: (.15, .15)
        #     Image:
        #         source: 'converter.png'



        # Button:
        #     id: close_menu
        #     text: 'X'
        #     size_hint: (.0, .07)
        #     pos_hint: {'x':.85, 'y':.93}
        #     on_press: root.hide_menu()

        Label:
            id: title
            text: lang['*Zaitoun utilities*'][ar]
            font_name: 'simpbdo.ttf'
            # text: "*Zaitoun utilies*" #utf code mean menu in arabic
            size_hint: (.66, .2)
            pos_hint: {'x':.17, 'y':.85}
            font_size: 40
            color: 1, 1, 0, 1

        Button:
            id: goto_date
            text: lang['date converter'][ar]
            font_name: 'simpbdo.ttf'
            size_hint: (.4, .1)
            pos_hint: {'x':.3, 'y':.66}
            on_press: root.goto_layout(root.date)
            # on_press: root.lauch_thread()
            # on_press: root.soundpl()
        Button:
            id: goto_prayer
            text: lang['prayer time'][ar]
            font_name: 'simpbdo.ttf'
            size_hint: (.4, .1)
            pos_hint: {'x':.3, 'y':.54}
            on_press: root.goto_layout(praytime)
            # on_press: root.lauch_thread2()
        Button:
            id: goto_mirath
            text: lang['mirath calculator'][ar]
            font_name: 'simpbdo.ttf'
            size_hint: (.4, .1)
            pos_hint: {'x':.3, 'y':.42}
            on_press: root.goto_layout(mirath)
        Button:
            id: goto_zakat
            text: lang['zakat calculator'][ar]
            font_name: 'simpbdo.ttf'
            size_hint: (.4, .1)
            pos_hint: {'x':.3, 'y':.3}
            on_press: root.goto_layout(zakat)
                
        Button:
            id: langage_btn
            text: 'eng'
            disabled: True
            background_color: 0,2,1,1
            size_hint: (.2, .1)
            pos_hint: {'x':.4, 'y':.08}
            on_press: root.change_langage()

        # Button:
        #     #id: type_btn
        #     text: 'return'
        #     background_color: 0,2,1,1
        #     size_hint: (.2, .1)
        #     pos_hint: {'x':.2, 'y':.08}
        #     on_press: root.goto_layout(date)
                

        # BoxLayout:
        #     # position and size to the parent, menu in this case
        #     size_hint: (.9, .08)
        #     pos_hint: {'x':.05, 'y':.6}

        #     ScreenLabel:
        #         id: result
        #         size_hint: (1, 1)
        #         text: 'DD-MM-YYYY ex : 09-08-2019'

            # ZaitounLabel:
            #     id: lbl_viw_siz
            #     text: 'void'
            #     markup: True
            #     # size_hint: (.25, .06)
            #     # pos: (0,440)








# date
    FloatLayout:
        id: date
        size_hint: (1, 1)
        pos_hint: {'x':0, 'y':.0}
        orientation: 'vertical'
        # opacity: 1 if root.ishist else 0

        ScrollView:
            id: date_list
            orientation: 'vertical'
            size_hint: (1, .5)
            pos_hint: {'x':0, 'y':.5}
            pos: (0,0)
            BoxLayout:
                id: date_box
                orientation: 'vertical'
                size_hint_x: 1
                size_hint_y: .12 * len(date_box.children)
                orientation: 'vertical'
                #on_touch_down: root.hide_kb()

        Button:
            id: ret_date_btn
            text: lang['return'][ar]
            font_name: 'simpbdo.ttf'
            #background_color: 0,2,1,1
            size_hint: (.2, .1)
            pos_hint: {'x':.7, 'y':.08}
            on_press: root.goto_layout(menu)

        Button:
            id: add_date
            text: lang['calculate'][ar]
            font_name: 'simpbdo.ttf'
            #background_color: 0,2,1,1
            size_hint: (.2, .1)
            pos_hint: {'x':.7, 'y':.35}
            on_press: root.convert(date_input)

        Label:
            id: result
            text: lang['converted date'][ar]
            font_name: 'simpbdo.ttf'
            size_hint: (.2, .1)
            pos_hint: {'x':.1, 'y':.35}
            #background_color: 0,2,1,1

        Button:
            id: date_input
            text: lang['touch here'][ar]
            font_name: 'simpbdo.ttf'
            size_hint: (.2, .1)
            pos_hint: {'x':.4, 'y':.35}
            # background_color: 3,3,3,1
            on_press: root.attach_kb(date_input)

        Button:
            id: delete_btn
            text: lang['delete'][ar]
            font_name: 'simpbdo.ttf'
            #background_color: 0,2,1,1
            size_hint: (.2, .1)
            pos_hint: {'x':.1, 'y':.08}
            on_press: root.activate_delete()

        Button:
            id: type_btn
            text: 'hijri'
            background_color: 0,2,1,1
            size_hint: (.2, .1)
            pos_hint: {'x':.4, 'y':.08}
            on_press: root.change_type()










# praytime
    FloatLayout:
        size_hint: (1, 1)
        pos_hint: {'x':0, 'y':.0}
        id: praytime


        GridLayout:
            size_hint: (.6, .40)
            pos_hint: {'x':.2, 'y':.35}
            rows: 6


            BoxLayout:
                canvas:
                    Color:
                        rgba: 0,0,0,1
                    # Rectangle:
                    #     #source: 'mylogo.png'
                    #     pos: self.pos
                    #     size: self.size
                Button:
                    id: sobh2
                    # background_color: 3,3,3,1
                    text: lang['sobh'][ar]
                    font_name: 'simpbdo.ttf'
                Label:
                    id: sobh
                    text: ''

            BoxLayout:
                canvas:
                    Color:
                        rgba: 0,0,0,1
                    # Rectangle:
                    #     #source: 'mylogo.png'
                    #     pos: self.pos
                    #     size: self.size
                Button:
                    id: choroq2
                    text: lang['choroq'][ar]
                    font_name: 'simpbdo.ttf'
                Label:
                    id: choroq
                    text: ''

            BoxLayout:
                canvas:
                    Color:
                        rgba: 0,0,0,1
                    # Rectangle:
                    #     #source: 'mylogo.png'
                    #     pos: self.pos
                    #     size: self.size
                Button:
                    id: dohr2
                    text: lang['dohr'][ar]
                    font_name: 'simpbdo.ttf'
                Label:
                    id: dohr
                    text: ''

            BoxLayout:
                canvas:
                    Color:
                        rgba: 0,0,0,1
                    # Rectangle:
                    #     #source: 'mylogo.png'
                    #     pos: self.pos
                    #     size: self.size
                Button:
                    id: asr2
                    text: lang['asr'][ar]
                    font_name: 'simpbdo.ttf'
                Label:
                    id: asr
                    text: ''

            BoxLayout:
                canvas:
                    Color:
                        rgba: 0,0,0,1
                    # Rectangle:
                    #     #source: 'mylogo.png'
                    #     pos: self.pos
                    #     size: self.size
                Button:
                    id: maghrib2
                    text: lang['maghrib'][ar]
                    font_name: 'simpbdo.ttf'
                Label:
                    id: maghrib
                    text: ''

            BoxLayout:
                canvas:
                    Color:
                        rgba: 0,0,0,1
                    # Rectangle:
                    #     #source: 'mylogo.png'
                    #     pos: self.pos
                    #     size: self.size
                Button:
                    id: ishaa2
                    text: lang['ishaa'][ar]
                    font_name: 'simpbdo.ttf'
                Label:
                    id: ishaa
                    text: ''

        Button:
            id: config
            text: lang['config'][ar]
            font_name: 'simpbdo.ttf'
            size_hint: (.2, .09)
            pos_hint: {'x':.79, 'y':.80}
            # background_color: 3,3,3,1
            on_press: root.goto_layout(praytime_config)

        Button:
            id: pray_config_ret
            text: lang['return'][ar]
            font_name: 'simpbdo.ttf'
            size_hint: (.2, .09)
            pos_hint: {'x':.79, 'y':.10}
            # background_color: 3,3,3,1
            on_press: root.goto_layout(menu)
        Button:
            id: pray_calcul
            text: lang['calculate'][ar]
            font_name: 'simpbdo.ttf'
            size_hint: (.2, .09)
            pos_hint: {'x':.19, 'y':.10}
            # background_color: 3,3,3,1
            on_press: root.calculate_praytime()
            # on_release: app.calculate_qiblah()

        Label:
            id: today_date
            # font_name: 'simpbdo.ttf'
            text: ''
            halign: "center"
            size_hint: (.6, .09)
            pos_hint: {'x':.2, 'y':.90}
            canvas:
                Color:
                    rgba: 0,0,0,1

        ScreenLabel:
            id: qibla
            text:  ' : ' + lang['qibla'][ar]
            font_name: 'simpbdo.ttf'
            size_hint: (.2, .09)
            pos_hint: {'x':.79, 'y':.20}

        FloatLayout:
            id: compass
            size: 100, 100
            pos_hint: {'x':.0, 'y':.0}
            size_hint: (.2, .3)

            Image:
                # id: rose
                source: 'none.png'
                # size: 100, 100
                pos: 0, 0
                canvas:
                    # Rotate:
                    #     angle: root.needle_angle
                    #     origin: self.center
                    Rectangle:
                        source: 'none.png'
                        # pos: 0.1, 0.1
                        # pos: 0.2*root.size[0]-25, 0.7*root.size[1]-25
                    Color: 
                        rgba: 0,0,1,0
            Image:
                id: needle
                source: 'rose.png'
                allow_stretch: True
                # size_hint: (.2, .1)
                size: compass.size
                # size: 100, 100
                pos: 0, 0
                canvas:
                    Rotate:
                        angle: root.needle_angle
                        origin: needle.center
                    Rectangle:
                        source: 'needle.png'
                        size: compass.size
                        # pos: 0.2*root.size[0]-25, 0.7*root.size[1]-25
                    Color: 
                        rgba: 0,0,1,0



















# configuration praytime
    FloatLayout:
        id: praytime_config
        size_hint: (1, 1)
        pos_hint: {'x':0, 'y':.0}

        BoxLayout:
            size_hint: (.8, .09)
            pos_hint: {'x':.1, 'y':.90}
            canvas:
                Color:
                    rgba: 0,0,0,1
            Label:
                id: timezone2
                text: lang['timezone'][ar]
                font_name: 'simpbdo.ttf'
            Button:
                id: timezone
                # background_color: 3,3,3,1
                text: '1'
                on_press: root.attach_kb(timezone)
        
        BoxLayout:
            size_hint: (.8, .09)
            pos_hint: {'x':.1, 'y':.80}
            canvas:
                Color:
                    rgba: 0,0,0,1
            Label:
                id: latitude2
                text: lang['latitude'][ar]
                font_name: 'simpbdo.ttf'
            Button:
                id: latitude
                # background_color: 3,3,3,1
                on_press: root.attach_kb(latitude)
                text: '33.546'

        BoxLayout:
            size_hint: (.8, .09)
            pos_hint: {'x':.1, 'y':.70}
            canvas:
                Color:
                    rgba: 0,0,0,1
            Label:
                id: longitude2
                text: lang['longitude'][ar]
                font_name: 'simpbdo.ttf'
            Button:
                id: longitude
                text: '-7.444'
                # background_color: 3,3,3,1
                on_press: root.attach_kb(longitude)

            
        BoxLayout:
            size_hint: (.8, .09)
            pos_hint: {'x':.1, 'y':.60}
            canvas:
                Color:
                    rgba: 0,0,0,1
            Label:
                id: isha_ref2
                text: lang['ishaa method'][ar]
                font_name: 'simpbdo.ttf'
            MySpinner:
                id: isha_ref
                text: lang['Egyptian General Authority of Survey'][ar]
                values: (lang['University of Islamic Sciences, Karachi'][ar],\
                lang['Muslim World League'][ar],\
                lang['Egyptian General Authority of Survey'][ar],\
                lang['Umm al-Qura University, Makkah'][ar],\
                lang['Islamic Society of North America'][ar])
                font_name: 'simpbdo.ttf'
                # background_color: 3,3,3,1

        BoxLayout:
            size_hint: (.8, .09)
            pos_hint: {'x':.1, 'y':.50}
            canvas:
                Color:
                    rgba: 0,0,0,1
            Label:
                id: asr_madhab2
                text: lang['asr method'][ar]
                font_name: 'simpbdo.ttf'
            MySpinner:
                id: asr_madhab
                text: lang['Hanafi'][ar]
                values: (lang['Shafii'][ar], lang['Hanafi'][ar])
                font_name: 'simpbdo.ttf'
                # background_color: 3,3,3,1

        Button:
            id: pray_ret
            text: lang['return'][ar]
            font_name: 'simpbdo.ttf'
            size_hint: (.2, .09)
            pos_hint: {'x':.79, 'y':.10}
            # background_color: 3,3,3,1
            on_press: root.goto_layout(praytime)






















# mirath
    FloatLayout:
        id: mirath
        size_hint: (1, 1)
        pos_hint: {'x':0, 'y':.0}
        orientation: 'vertical'
        # opacity: 1 if root.ishist else 0


        Accordion:
            size_hint: (1, .7)
            pos_hint: {'x':0, 'y':.3}
            orientation: 'vertical'

            AccordionItem:
                title: 'Panel 1'

                ScrollView:
                    id: mirath_list
                    orientation: 'vertical'
                    pos: (0,0)
                    BoxLayout:
                        id: mirath_box
                        orientation: 'vertical'
                        size_hint_x: 1
                        size_hint_y: .12 * len(mirath_box.children)
                        orientation: 'vertical'
                        #on_touch_down: root.hide_kb()

            AccordionItem:
                title: 'Panel 2'

                ScrollView:
                    id: mirath_log_sv
                    orientation: 'vertical'
                    pos: (0,0)
                    BoxLayout:
                        id: mirath_log_box
                        size_hint_y: 2
                        Button:
                            id: mirath_log
                            # text: "log\
                            # sdg"
                            # halign: "center"
                            # # halign: "center"
                            # valign: "top"
                            # # valign: "middle"

        # Button:
        #     id: add_mirath
        #     text: lang['add relative'][ar]
        #     font_name: 'simpbdo.ttf'
        #     text: 'add relative'
        #     #background_color: 0,2,1,1
        #     size_hint: (.2, .1)
        #     pos_hint: {'x':.7, 'y':.4}
        #     on_press: root.convert(date_input)

        Label:
            id: m_result
            text: ''
            # text: lang[''][ar]
            # font_name: 'simpbdo.ttf'
            size_hint: (.2, .1)
            pos_hint: {'x':.1, 'y':.4}
            #background_color: 0,2,1,1

        Button:
            id: mirath_input
            text: lang['calculate'][ar]
            font_name: 'simpbdo.ttf'
            size_hint: (.2, .08)
            pos_hint: {'x':.4, 'y':.1}
            # background_color: 3,3,3,1
            on_press: root.calculte_mirath()

        BoxLayout:
            size_hint: (.8, .08)
            pos_hint: {'x':.1, 'y':.20}
            canvas:
                Color:
                    rgba: 0,0,0,1
            # Label:
            #     text: 'relative'
            MySpinner:
                id: relative
                font_name: 'simpbdo.ttf'
                text: lang['husband'][ar]
                values: (lang['husband'][ar],\
                lang['wife'][ar],\
                lang['son'][ar],\
                lang['daughter'][ar],\
                lang['grandson'][ar],\
                lang['granddaughter'][ar],\
                lang['father'][ar],\
                lang['mother'][ar],\
                lang['grandfather'][ar],\
                lang['paternal_grandmother'][ar],\
                lang['maternal_grandmother'][ar],\
                lang['brother'][ar],\
                lang['sister'][ar],\
                lang['paternal_brother'][ar],\
                lang['paternal_sister'][ar],\
                lang['maternal_brother'][ar],\
                lang['maternal_sister'][ar],\
                lang['nephew'][ar],\
                lang['paternal_nephew'][ar],\
                lang['nephew_son'][ar],\
                lang['paternal_nephew_son'][ar],\
                lang['paternal_uncle'][ar],\
                lang['paternal_paternal_uncle'][ar],\
                lang['cousin'][ar],\
                lang['cousin_son'][ar],\
                lang['paternal_cousin'][ar],\
                lang['paternal_cousin_son'][ar],\
                lang['cousin_grandson'][ar],\
                lang['paternal_cousin_grandson'][ar]\
                )

                # background_color: 3,3,3,1
                font_name: 'simpbdo.ttf'
            Spinner:
                id: number
                text: '1'
                values: ('1','2','3','4','5')
                # background_color: 3,3,3,1
            Button:
                id: add_relative
                text: lang['add relative'][ar]
                font_name: 'simpbdo.ttf'
                on_press: root.add_relative()

 

        Button:
            id: mirath_cln
            text: lang['clean'][ar]
            font_name: 'simpbdo.ttf'
            #background_color: 0,2,1,1
            size_hint: (.2, .08)
            pos_hint: {'x':.1, 'y':.04}
            on_press: root.clean()

        Button:
            id: mirath_del
            text: lang['delete'][ar]
            font_name: 'simpbdo.ttf'
            disabled: True
            #background_color: 0,2,1,1
            size_hint: (.2, .08)
            pos_hint: {'x':.4, 'y':.04}
            on_press: root.activate_delete()

        Button:
            id: mirath_ret
            text: lang['return'][ar]
            font_name: 'simpbdo.ttf'
            #background_color: 0,2,1,1
            size_hint: (.2, .08)
            pos_hint: {'x':.7, 'y':.04}
            on_press: root.goto_layout(menu)



















#zakat
    FloatLayout:
        id: zakat
        size_hint: (1, 1)
        pos_hint: {'x':0, 'y':.0}
        orientation: 'vertical'


        ScreenLabel:
            id: z_result
            text: '0 $'
            size_hint: (.2, .1)
            pos_hint: {'x':.4, 'y':.8}
            background_color: 0,2,1,1

        Button:
            id: zakat_input
            text: lang['touch here'][ar]
            font_name: 'simpbdo.ttf'
            size_hint: (.2, .1)
            pos_hint: {'x':.4, 'y':.7}
            on_press: root.attach_kb(zakat_input)

        Button:
            id: zakat_validate
            text: lang['calculate'][ar]
            font_name: 'simpbdo.ttf'
            size_hint: (.2, .08)
            pos_hint: {'x':.4, 'y':.6}
            # background_color: 3,3,3,1
            on_press: root.calculte_zakat()






        Button:
            id: zakat_type
            text: lang['money'][ar]
            font_name: 'simpbdo.ttf'
            size_hint: (.16, .08)
            pos_hint: {'x':.17, 'y':.3}
            # background_color: 3,3,3,1
            on_press: root.change_zakat_type()

        Button:
            id: irigation_type
            text: lang['natural irigation'][ar]
            font_name: 'simpbdo.ttf'
            disabled: True
            size_hint: (.16, .08)
            pos_hint: {'x':.42, 'y':.3}
            # background_color: 3,3,3,1
            on_press: root.change_irigation_type()

        Button:
            id: zakat_madhab
            text: lang['hanafi nisab'][ar]
            font_name: 'simpbdo.ttf'
            disabled: True
            size_hint: (.16, .08)
            pos_hint: {'x':.67, 'y':.3}
            # background_color: 3,3,3,1
            on_press: root.change_zakat_madhab()



        Button:
            id: zakat_ret
            text: lang['return'][ar]
            font_name: 'simpbdo.ttf'
            #background_color: 0,2,1,1
            size_hint: (.2, .1)
            pos_hint: {'x':.7, 'y':.08}
            on_press: root.goto_layout(menu)




















    FloatLayout:
        id: keyboard
        canvas:
            Color:
                rgba: 0,0,0,1
            Rectangle:
                pos: self.pos
                size: self.size
        ScreenLabel:
            id: kb_val
            size_hint: (.6, 0.09)
            pos_hint: {'x':.2, 'y':.6}
            text: ''
        GridLayout:
            id: kb
            size_hint: (.6, .40)
            pos_hint: {'x':.2, 'y':.2}
            rows: 6

            Button:
                text: u'1'
                # text: str(asr_ref['Hanafi'])
                on_press: root.enter_number(1)
            Button:
                text: u'2'
                on_press: root.enter_number(2)
            Button:
                text: u'3'
                on_press: root.enter_number(3)

            Button:
                text: u'4'
                on_press: root.enter_number(4)
            Button:
                text: u'5'
                on_press: root.enter_number(5)
            Button:
                text: u'6'
                on_press: root.enter_number(6)

            Button:
                text: u'7'
                on_press: root.enter_number(7)
            Button:
                text: u'8'
                on_press: root.enter_number(8)
            Button:
                text: u'9'
                on_press: root.enter_number(9)

            Button:
                text: u'<-'
                #on_press: kb_val.text = ''
                on_press: kb_val.text = kb_val.text[:-1]
            Button:
                text: u'0'
                on_press: root.enter_number(0)
            Button:
                id: ok
                font_name: 'simpbdo.ttf'
                text: lang['ok'][ar]

                on_press: root.validate(kb_val.text)
                # on_press: root.convert(kb_val)

            # ZaitounLabel:
            #     opacity:0
            Button:
                text: u'-'
                on_press: root.enter_number('-')

            Button:
                id: clean_kb
                text: lang['clean'][ar]
                font_name: 'simpbdo.ttf'
                # text: u'clean'
                on_press: kb_val.text = ''
                #on_press: kb_val.text = kb_val.text[:-1]

            # ZaitounLabel:
            #     opacity:0
            Button:
                text: u'.'
                on_press: root.enter_number('.')














# # config menu

#     #date page
#     FloatLayout:
#         id: date
#         size_hint: (1, 1)
#         pos_hint: {'x':0, 'y':.0}
#         orientation: 'vertical'

#         ScrollView:
#             id: date_list
#             pos: (0,0)
#             BoxLayout:
#                 id: date_box
#                 size_hint_x: 1
#                 size_hint_y: 0
#                 orientation: 'vertical'
#                 #on_touch_down: root.hide_kb()
#         Button:
#             id: ret_date_btn
#             text: 'return'
#             #background_color: 0,2,1,1
#             size_hint: (.2, .1)
#             pos_hint: {'x':.7, 'y':.08}
#             on_press: root.goto_layout(menu)
#         Button:
#             id: delete_btn
#             text: 'delete'
#             #background_color: 0,2,1,1
#             size_hint: (.2, .1)
#             pos_hint: {'x':.1, 'y':.08}
#             on_press: root.activate_delete()
#             # on_press: root.show_popup(delete_btn)
#             # on_press: root.enter_number(kb_val, 3)
#             # on_press: root.activate_delete()
#   # config menu

#     #date page
#     FloatLayout:
#         id: date
#         size_hint: (1, 1)
#         pos_hint: {'x':0, 'y':.0}
#         orientation: 'vertical'

#         ScrollView:
#             id: date_list
#             pos: (0,0)
#             BoxLayout:
#                 id: date_box
#                 size_hint_x: 1
#                 size_hint_y: 0
#                 orientation: 'vertical'
#                 #on_touch_down: root.hide_kb()
#         Button:
#             id: ret_date_btn
#             text: 'return'
#             #background_color: 0,2,1,1
#             size_hint: (.2, .1)
#             pos_hint: {'x':.7, 'y':.08}
#             on_press: root.goto_layout(menu)
#         Button:
#             id: delete_btn
#             text: 'delete'
#             #background_color: 0,2,1,1
#             size_hint: (.2, .1)
#             pos_hint: {'x':.1, 'y':.08}
#             on_press: root.activate_delete()
#             # on_press: root.show_popup(delete_btn)
#             # on_press: root.enter_number(kb_val, 3)
#             # on_press: root.activate_delete()
#   # config menu





    # #mirath page
    # FloatLayout:
    #     id: mirath
    #     size_hint: (1, 1)
    #     pos_hint: {'x':0, 'y':.0}
    #     orientation: 'vertical'

        # ScrollView:
        #     id: date_list
        #     pos: (0,0)
        #     BoxLayout:
        #         id: date_box
        #         size_hint_x: 1
        #         size_hint_y: 0
        #         orientation: 'vertical'
        #         #on_touch_down: root.hide_kb()
        # Button:
        #     id: ret_date_btn
        #     text: 'return'
        #     #background_color: 0,2,1,1
        #     size_hint: (.2, .1)
        #     pos_hint: {'x':.7, 'y':.08}
        #     on_press: root.goto_layout(menu)
        # Button:
        #     id: delete_btn
        #     text: 'delete'
        #     #background_color: 0,2,1,1
        #     size_hint: (.2, .1)
        #     pos_hint: {'x':.1, 'y':.08}
        #     on_press: root.activate_delete()
        #     # on_press: root.show_popup(delete_btn)
        #     # on_press: root.enter_number(kb_val, 3)
        #     # on_press: root.activate_delete()
    



'''

# kbrd = '''
# # custom keyboard
# <FloatLayout>
#     GridLayout:
#         id: kb
#         size_hint: (.6, .40)
#         pos_hint: {'x':.2, 'y':.2}
#         rows: 6

#         Button:
#             text: u'1'
#             on_press: root.enter_number(page_val, 1)
#         Button:
#             text: u'2'
#             on_press: root.enter_number(page_val, 2)
#         Button:
#             id: btn3
#             text: u'3'
#             # on_press: root.enter_number(page_val, 3)
#             on_press: root.show_popup(btn3)

#         Button:
#             text: u'4'
#             on_press: root.enter_number(page_val, 4)
#         Button:
#             text: u'5'
#             on_press: root.enter_number(page_val, 5)
#         Button:
#             text: u'6'
#             on_press: root.enter_number(page_val, 6)

#         Button:
#             text: u'7'
#             on_press: root.enter_number(page_val, 7)
#         Button:
#             text: u'8'
#             on_press: root.enter_number(page_val, 8)
#         Button:
#             text: u'9'
#             on_press: root.enter_number(page_val, 9)

#         Button:
#             text: u'<-'
#             #on_press: page_val.text = ''
#             on_press: page_val.text = page_val.text[:-1]
#         Button:
#             text: u'0'
#             on_press: root.enter_number(page_val, 0)
#         Button:
#             id: goto_page_btn
#             #font_name: 'simpbdo.ttf'
#             #text: u'ok'#means done in arabic
#             text: 'ok'
#             on_press: root.valide()

#         Button:
#             text: u'clean'
#             on_press: page_val.text = ''
#             #on_press: page_val.text = page_val.text[:-1]
#         ScreenLabel:
#             id: page_val
#             size_hint: (1, 1)
#             text: ''
#         ZaitounLabel:
#             opacity:0

#     '''




# Builder.load_string(kbrd, filename ="kbrd.kv")
Builder.load_string(cvrt, filename ="cvrt.kv")

# Builder.unload_file("cvrt.kv")
# Builder.unload_file("kbrd.kv")


# class MyButton(Button):
#     font_name = 'simpbdo.ttf'
#     size = 20, 20

class MySpinner(Spinner):
    def _update_dropdown(self, *largs):
        dp = self._dropdown
        cls = self.option_cls
        values = self.values
        text_autoupdate = self.text_autoupdate
        if isinstance(cls, string_types):
            cls = Factory.get(cls)
        dp.clear_widgets()
        for value in values:
            item = cls(text=value)
            item.height = self.height if self.sync_height else item.height
            item.bind(on_release=lambda option: dp.select(option.text))
            item.font_name = 'simpbdo.ttf'
            dp.add_widget(item)
        if text_autoupdate:
            if values:
                if not self.text or self.text not in values:
                    self.text = values[0]
            else:
                self.text = ''
    # option_cls = ObjectProperty(MyButton) # setting this property inside kv doesn't seem to work





#custom label with solid background
class ZaitounLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(.5, .5, .5, 1)
            Rectangle(pos=self.pos, size=self.size)

#same here with black color
class ScreenLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(pos=self.pos, size=self.size)

class Zaitoun(FloatLayout):

    ismenu = 1
    iskb = 1
    isfirsttime = 1
    current_layout = None
    # sound = SoundLoader.load('test.mp3')
    # current_thread = None
    # sound2 = SoundLoader.load('test.ogg')
    isdelete = 0
    needle_angle = NumericProperty(0)

    global ar
    global eng
    curent_langage = ar

    date = FloatLayout()
    pray_conf = FloatLayout()



    day = 1
    month = 1
    year = 1

    # 'h' for hijri and 'g' for gregorian
    date_type = 'h'

    # 'm' for money and 'h' for harvest
    zakat_type = 'm'

    # 'n' for natural and 'a' for artificial
    irigation_type = 'n'

    # 's' for hanafi and 'o' for other
    zakat_madhab = 'h'


    # global ype
    
    #ti = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Zaitoun, self).__init__(**kwargs)
        self.pray_conf = self.ids.praytime_config
        self.date = self.ids.date

        
    def update(self, dt):

        if self.isfirsttime:
            #self.hide_kb()
            
            # self.add_widget()
            # self.remove_widget(self.ids.kb)
            self.current_layout = self.ids.menu
            # p = Keyboard(self)
            # p.open()
            # p.dismiss()

            global latitude
            latitude = self.ids.latitude.text
            global longitude
            longitude = self.ids.longitude.text
            global timezone
            timezone = self.ids.timezone.text
            global fajr_isha_method
            fajr_isha_method = self.ids.isha_ref.text
            global asr_fiqh
            asr_fiqh = self.ids.asr_madhab.text


            self.date = self.ids.date
            self.pray_conf = self.ids.praytime_config
            self.clear_widgets()
            self.add_widget(self.ids.menu)


            # self.goto_layout(self.ids.praytime_config)
            # self.goto_layout(self.ids.menu)
            
            # if self.sound:
            #     print("Sound found at %s" % self.sound.source)
            #     print("Sound is %.3f seconds" % self.sound.length)
            #     self.sound.play()

            for i in range(10):
                lbl = Label(text= '')
                # lbl = Label(text= str(i))
                self.ids.mirath_box.add_widget(lbl)

            # print(get_key(asr_ref, 1))
            # print(get_key_tab(self,lang, '\ufedd\ufeed\ufec1\ufedf\ufe8d\u0020\ufec2\ufea7', ar))
            # self.ids.date.clear_widgets



        # for i in range(15):
        #     lbl = Label(text= str(i))
        #     self.ids.date_box.add_widget(lbl)
            # if self.sound2:
            #     print("Sound found at %s" % self.sound2.source)
            #     print("Sound is %.3f seconds" % self.sound2.length)
            #     self.sound2.play()
            self.isfirsttime = 0

        # print( self.date is self.ids.date)

        # self.ids.date_box.size_hint_y = .12 * len(self.ids.date_box.children)
        # self.ids.mirath_box.size_hint_y = .12 * len(self.ids.mirath_box.children)

        # print(lang['word'][ar])
        # print(isha_ref['University of Islamic Sciences, Karachi'])





    #functions for buttons


    def attach_kb(self, target):
        self.add_widget(self.ids.keyboard)
        global target_widget
        target_widget = target
        # self.add_widget(self.ids.keyboard, len(self.children))

    def detach_kb(self):
        self.remove_widget(self.ids.keyboard)

    def show_kb(self):
        if not self.iskb:
            self.ids.kb.opacity = 1
            self.ids.kb.size_hint_x = .6
            self.iskb = 1

    def hide_kb(self):
        if self.iskb:
            self.ids.kb.opacity = 0
            self.ids.kb.size_hint_x = .0
            self.iskb = 0

    def goto_layout(self, layout):
        # self.clear_widgets()
        self.remove_widget(self.current_layout)
        self.current_layout = layout
        self.add_widget(self.current_layout)
        # for i in range(len(layout.children)):
        #     print(layout.children[i].id)

        global latitude
        latitude = self.ids.latitude.text
        global longitude
        longitude = self.ids.longitude.text
        global timezone
        timezone = self.ids.timezone.text
        global fajr_isha_method
        fajr_isha_method = self.ids.isha_ref.text
        global asr_fiqh
        asr_fiqh = self.ids.asr_madhab.text




    def enter_number(self, page_val, number):
        page_val.text += (str)(number)
        # if len(page_val.text) == 2 or len(page_val.text) == 5:
        #     page_val.text += (str)('-')
        # if (int)(page_val.text) > 604:
        #     page_val.text = u'604'
        # if page_val.text == '0':
        #     page_val.text = u''

    def convert(self, date_input):

        if self.ids.date_input.text == lang['touch here'][ar]:
            return

        result = self.ids.result
        result.text = ''

        type_btn = self.ids.type_btn
        date_type = self.date_type

        day, month, year = date_input.text.split('-', 2)
        date = Date(date_type,int(day),int(month),int(year))

        # date_input.text = '23-06-2019'
        result.text = (str)(date.tell_day()) 



    # size = len(self.ids.date_box.children)
    # i = size
    # btn = Button(text= str(i), id= 'd'+str(i))
        # btn.bind(on_press= self.auto_destruct)
    # self.ids.date_box.add_widget(btn, size)
    # tmp = 'd'+str(size)
        # self.ids.d0.bind(on_press= self.auto_destruct)

        if result.text != "invalid date" :
            global converted_date
            size = len(converted_date)
            size2 = len(self.ids.date_box.children)
            converted_date.append(result.text)
            
            btn = Button(text= converted_date[size], id= str(size))
            # btn = Button(text= str(size), id= str(size))
            btn.bind(on_press= self.auto_destruct)
            self.ids.date_box.add_widget(btn, size2)

        self.ids.date_box.size_hint_y = .12 * size2


    def change_type(self):

        # global cvrt
        # print(cvrt)
        # Builder.unload_file("kbrd.kv")
        # self.clear_widgets()
        # cv = FloatLayout() 
        # cv.add_widget(Builder.load_string(cvrt))
        # self.add_widget(cv)
        # self.add_widget(Button())


        type_btn = self.ids.type_btn
        if self.date_type == 'h':
            self.date_type = 'g'
            type_btn.background_color = 0,1,2,1
            type_btn.text = "gregorien"
        else:
            self.date_type = 'h'
            type_btn.background_color = 0,2,1,1
            type_btn.text = "hijri"



    # def auto_destruct(self, id):
    #     if self.isdelete :
    #         # converted_date.pop(int(instance.id))
    #         self.ids.hist_box.remove_widget(instance)
    #         print(instance.id + ' deleted')

    def auto_destruct(self, instance):
        if self.isdelete :
            # converted_date.pop(int(instance.id))
            self.ids.date_box.remove_widget(instance)
            global converted_date
            converted_date.pop(int(instance.id))
            print(instance.id + ' deleted')

            #replace orders
            l = len(converted_date)
            l2 = len(self.ids.date_box.children)
            for i in range(l):
                print(str(i) + ' deleted')
                self.ids.date_box.children[l2-l+i].id = str(i)
                # self.ids.date_box.children[l2-l+i].text = str(i)
            self.ids.date_box.size_hint_y = .12 * l2


    def activate_delete(self):
        if self.isdelete:
            self.isdelete = 0
            self.ids.delete_btn.background_color = 1,1,1,1
        else :
            self.isdelete = 1
            self.ids.delete_btn.background_color = 3,0,0,1

    # def lauch_thread(self):
    #     threading.Thread(target = self.soundpl).start()
    
    # def lauch_thread2(self):
    #     threading.Thread(target = self.soundpl2).start()

    # def soundpl(self):
    #     if self.sound:
    #         print("Sound found at %s" % self.sound.source)
    #         print("Sound is %.3f seconds" % self.sound.length)
    #         self.sound.play()
    #     playsound('test.ogg')
    #     self.sound.play()

    # def soundpl2(self):
    #     if self.sound:
    #         print("Sound found at %s" % self.sound.source)
    #         print("Sound is %.3f seconds" % self.sound.length)
    #         self.sound.play()
    #     playsound('test.mp3')
    #     self.sound.play()


    def calculate_praytime(self):
        # playsound('test.ogg', False)
            # self.lauch_thread()
            # self.sound.play()
        # latitude = 33.5922
        # longitude = -7.6184

    # g = geocoder.ip('me')
    # latitude = g.latlng[0]
    # longitude = g.latlng[1]


        # print(g.latlng)

        lg = self.curent_langage


        global latitude
        latitude = self.ids.latitude.text
        global longitude
        longitude = self.ids.longitude.text
        global timezone
        timezone = self.ids.timezone.text
        global fajr_isha_method
        fajr_isha_method = self.ids.isha_ref.text
        global asr_fiqh
        asr_fiqh = self.ids.asr_madhab.text





        latitude = float(self.ids.latitude.text)
        longitude = float(self.ids.longitude.text)
        timezone = float(self.ids.timezone.text)


        fajr_isha_method = isha_ref[get_key_tab(self, lang, self.ids.isha_ref.text, lg)]
        asr_fiqh = asr_ref[get_key_tab(self, lang, self.ids.asr_madhab.text, lg)]
        # asr_fiqh = 1


        pconf = PrayerConf(longitude, latitude, timezone, fajr_isha_method, asr_fiqh)
        pt = Prayer(pconf, date.today())

        #method 1
        dat = date.today()
        tim = datetime.now()
        mydate = Date('g', dat.day, dat.month, dat.year)

        minute = str(tim.minute)

        if tim.minute < 10 :
            minute = "0" + minute

        self.ids.today_date.text = mydate.tell_day() + '\n' + str(tim.hour) + ':' + minute

        #method 2
        # hijri = HijriDate.today()
        # self.ids.today_date.text = hijri.format(2)
        #str(hijri.to_gregorian())



        f = self.ids.sobh
        s = self.ids.choroq
        d = self.ids.dohr
        a = self.ids.asr
        m = self.ids.maghrib
        i = self.ids.ishaa

        # f.text = str(latitude)
        # s.text = str(longitude)
        f.text = str(pt.fajr_time())
        s.text = str(pt.sherook_time())
        d.text = str(pt.dohr_time())
        a.text = str(pt.asr_time())
        m.text = str(pt.maghreb_time())
        i.text = str(pt.ishaa_time())

        # self.needle_angle = float(Qiblah(pconf).direction()) + 90.
        t_angle = float(Qiblah(pconf).direction()) * -1

        # Animation(needle_angle= 90).start(self)
        
        # Animation(needle_angle= self.wdg.needle_angle).start(self)

        #self.ids.needle.canvas = 90.

        Animation(needle_angle= t_angle, duration= .5).start(self)


        print(self.needle_angle)
        self.ids.qibla.text = str("{0:.2f}".format(-t_angle)) + ' : ' + lang['qibla'][ar]
        # "{0:.2f}".format(self.needle_angle)


        # def calculate_qiblah(self):

        # PushMatrix()
        # self.ids.needle.rot = Rotate(1, 0, 1, 0)
        # PopMatrix()







    def add_relative(self):
        #handle mirath class
        relative = self.ids.relative.text
        number = self.ids.number.text
        mirath.add_relative(get_key_tab(self, lang, relative, ar), int(number))

        #handle mirath widget
        box = BoxLayout()
        btn = Button(text= number)
        box.add_widget(btn)
        lbl = Label(text= relative, font_name= 'simpbdo.ttf')
        box.add_widget(lbl)
        btn2 = Button()
        box.add_widget(btn2)
        
        l = len(self.ids.mirath_box.children)
        self.ids.mirath_box.add_widget(box, l)
        self.ids.mirath_box.size_hint_y = .12 * len(self.ids.mirath_box.children)


    def calculte_mirath(self):
        mirath.calculte_mirath()

        l = len(mirath.result_list)
        l2 = len(self.ids.mirath_box.children)
        for i in range(l):
            self.ids.mirath_box.children[l2-l+i].children[0].text = str(mirath.result_list[i])

        mirath.display_shares()
        self.ids.mirath_log.text = mirath.log

        lines = 1
        for i in range(len(self.ids.mirath_log.text)):
            if self.ids.mirath_log.text[i] == '\n':
                lines += 1

        self.ids.mirath_log_box.size_hint_y = lines * .1

        if self.ids.mirath_log_box.size_hint_y < 1.1:
            self.ids.mirath_log_box.size_hint_y = 1.1

        # self.ids.mirath_log_sv.size_hint_y = self.ids.mirath_log.size[1]
        # self.ids.mirath_log.valign = 'top'
        # self.ids.mirath_log.halign = 'left'

    def clean(self):
        l = len(mirath.relative_list)
        l2 = len(self.ids.mirath_box.children)
        for i in range(l):
            #don't do this
            # self.ids.mirath_box.remove_widget(self.ids.mirath_box.children[l2-l+i])
            self.ids.mirath_box.remove_widget(self.ids.mirath_box.children[l2-l])
            # print(i)

        mirath.relative_list.clear()
        mirath.count_list.clear()
        mirath.result_list.clear()
        mirath.log = ''
        self.ids.mirath_log.text = mirath.log
        self.ids.mirath_box.size_hint_y = .12 * len(self.ids.mirath_box.children)


            
        # self.ids.mirath_box.clear_widgets()
        # for i in range(10):
        #     lbl = Label(text= str(i))
        #     self.ids.mirath_box.add_widget(lbl)


    def calculte_zakat(self):



        #security
        if self.ids.zakat_input.text == lang['touch here'][ar]:
            return
                # if self.ids.zakat_input.text == get_key_tab(self, lang, u'touch here', lg):


        if self.zakat_type == 'm':
            self.ids.z_result.text = str(zakat.calculate_zakat(int(self.ids.zakat_input.text))) + ' $'
        elif self.zakat_type == 'h' and self.irigation_type == 'n':
            if self.zakat_madhab == 'h':
                self.ids.z_result.text = str(zakat.calculate_zakat_harvest(int(self.ids.zakat_input.text), 'natural', 'hanafi')) + ' kg'
            elif self.zakat_madhab == 'o':
                self.ids.z_result.text = str(zakat.calculate_zakat_harvest(int(self.ids.zakat_input.text), 'natural', 'other')) + ' kg'

        elif self.zakat_type == 'h' and self.irigation_type == 'a':
            if self.zakat_madhab == 'h':
                self.ids.z_result.text = str(zakat.calculate_zakat_harvest(int(self.ids.zakat_input.text), 'artificial', 'hanafi')) + ' kg'
            elif self.zakat_madhab == 'o':
                self.ids.z_result.text = str(zakat.calculate_zakat_harvest(int(self.ids.zakat_input.text), 'artificial', 'other')) + ' kg'


        # + ' Kg'

    def change_zakat_type(self):
        if self.zakat_type == 'm':
            self.zakat_type = 'h'
            self.ids.zakat_type.text = lang['harvest'][ar]
            self.ids.irigation_type.disabled = False
            self.ids.zakat_madhab.disabled = False
        else:
            self.zakat_type = 'm'
            self.ids.zakat_type.text = lang['money'][ar]
            self.ids.irigation_type.disabled = True
            self.ids.zakat_madhab.disabled = True

    def change_irigation_type(self):
        if self.irigation_type == 'n':
            self.irigation_type = 'a'
            self.ids.irigation_type.text = lang['artificial irigation'][ar]
        else:
            self.irigation_type = 'n'
            self.ids.irigation_type.text = lang['natural irigation'][ar]

    def change_zakat_madhab(self):
        if self.zakat_madhab == 'h':
            self.zakat_madhab = 'o'
            self.ids.zakat_madhab.text = lang['others nisab'][ar]
        else:
            self.zakat_madhab = 'h'
            self.ids.zakat_madhab.text = lang['hanafi nisab'][ar]

    def change_langage(self):

        global ar
        global eng

        langage_btn = self.ids.langage_btn
        if self.curent_langage == ar:
            self.curent_langage = eng
            langage_btn.background_color = 0,1,2,1
            langage_btn.text = "eng"
        elif self.curent_langage == eng:
            self.curent_langage = ar
            langage_btn.background_color = 0,2,1,1
            langage_btn.text = "ar"

        lg = self.curent_langage


        # self.ids.clean_kb.text = lang['clean'][lg]
        # self.ids.ok.text = lang['ok'][lg]
        self.ids.title.text = lang['*Zaitoun utilities*'][lg]
        self.ids.goto_date.text = lang['date converter'][lg]

        self.ids.goto_date.text = lang['date converter'][lg]
        self.ids.goto_prayer.text = lang['prayer time'][lg]
        self.ids.goto_mirath.text = lang['mirath calculator'][lg]
        self.ids.goto_zakat.text = lang['zakat calculator'][lg]

        self.ids.ret_date_btn.text = lang['return'][lg]
        self.ids.add_date.text = lang['calculate'][lg]
        self.ids.result.text = lang['converted date'][lg]
        self.ids.delete_btn.text = lang['delete'][lg]

        self.ids.sobh2.text = lang['sobh'][lg]
        self.ids.choroq2.text = lang['choroq'][lg]
        self.ids.dohr2.text = lang['dohr'][lg]
        self.ids.asr2.text = lang['asr'][lg]
        self.ids.maghrib2.text = lang['maghrib'][lg]
        self.ids.ishaa2.text = lang['ishaa'][lg]

        self.ids.config.text = lang['config'][lg]
        self.ids.pray_config_ret.text = lang['return'][lg]
        self.ids.pray_calcul.text = lang['calculate'][lg]
        self.ids.qibla.text = lang['qibla'][lg]
        self.ids.timezone2.text = lang['timezone'][lg]
        self.ids.latitude2.text = lang['latitude'][lg]
        self.ids.longitude2.text = lang['longitude'][lg]

        self.ids.isha_ref2.text = lang['ishaa method'][lg]
        self.ids.isha_ref.text = lang['Egyptian General Authority of Survey'][lg]
        self.ids.isha_ref.values = (lang['University of Islamic Sciences, Karachi'][lg],\
            lang['Muslim World League'][lg],\
            lang['Egyptian General Authority of Survey'][lg],\
            lang['Umm al-Qura University, Makkah'][lg],\
            lang['Islamic Society of North America'][lg])

        self.ids.asr_madhab2.text = lang['asr method'][lg]
        self.ids.asr_madhab.text = lang['Hanafi'][lg]
        # self.ids.asr_madhab.values = (lang['Shafii'][lg], lang['Hanafi'][lg])

        self.ids.pray_ret.text = lang['return'][lg]

        self.ids.mirath_ret.text = lang['return'][lg]
        self.ids.add_mirath.text = lang['add relative'][lg]
        self.ids.mirath_input.text = lang['calculate'][lg]

        # self.ids.relative.values = (lang['husband'][lg],\
        #     lang['wife'][lg],\
        #     lang['son'][lg],\
        #     lang['daughter'][lg],\
        #     lang['father'][lg],\
        #     lang['mother'][lg],\
        #     lang['grandson'][lg],\
        #     lang['granddaughter'][lg],\
        #     lang['grandfather'][lg],\
        #     lang['paternal_grandmother'][lg],\
        #     lang['maternal_grandmother'][lg],\
        #     lang['brother'][lg],\
        #     lang['sister'][lg],\
        #     lang['paternal_brother'][lg],\
        #     lang['paternal_sister'][lg],\
        #     lang['maternal_brother'][lg],\
        #     lang['maternal_sister'][lg],\
        #     lang['nephew'][lg],\
        #     lang['paternal_nephew'][lg],\
        #     lang['nephew_son'][lg],\
        #     lang['paternal_nephew_son'][lg],\
        #     lang['paternal_uncle'][lg],\
        #     lang['paternal_cousin'][lg],\
        #     lang['paternal_cousin_son'][lg],\
        #     lang['paternal_uncle'][lg],\
        #     lang['paternal_cousin'][lg],\
        #     lang['paternal_cousin_son'][lg],\
        #     lang['cousin_grandson'][lg],\
        #     lang['paternal_cousin_grandson'][lg],\
        #     lang['paternal_paternal_uncle'][lg])
        
        self.ids.relative.text = lang['husband'][lg]

        self.ids.add_relative.text = lang['add relative'][lg]
        self.ids.mirath_cln.text = lang['clean'][lg]




    def enter_number(self, number):
        self.ids.kb_val.text += (str)(number)
        if  self.current_layout == self.ids.date:
            if len(self.ids.kb_val.text) == 2 or len(self.ids.kb_val.text) == 5:
                self.ids.kb_val.text += (str)('-')


    def validate(self, value):
        global target_widget
        target_widget.text = value
        self.detach_kb()






class ZaitounApp(App):

    #window object of the app
    global Window
    #principal widget of the app
    global wdg
    needle_angle = NumericProperty(0)
    # stop = threading.Event()
    _anim = None


    # global asr_ref
    # asr_reff = asr_ref

    def build(self):
        Window.set_title('Zaitoun')
        self.title = 'Zaitoun'
        self.icon = 'Zaitoun.png'
        self.wdg = Zaitoun(size= Window.size)
        main_wdg = self.wdg
        lg = self.wdg.curent_langage



        #restore last session auto-save
        try:
            f = open("date_log.dat")
            count = int(f.readline())
            for i in range(count):
                line = f.readline()
                #remove newline
                #size = len(converted_date[i])
                if line[int(len(line))-1] == '\n' :
                    line = line[:-1]
                converted_date.append(line)
                print(converted_date[i])
                #btn = Button(text= 'btn'+str(i), id= 'btn'+str(i), on_press= lambda a:self.wdg.auto_destruct())
                #btn = Button(text= converted_date[i], id='btn'+str(i))
                # btn = Button(text= str(i), id = str(i))
                btn = Button(text= converted_date[i], id = str(i))
                btn.bind(on_press= self.wdg.auto_destruct)
                #btn = Button(text= converted_date[i], id= 'btn'+str(i))
                main_wdg.ids.date_box.add_widget(btn, len(main_wdg.ids.date_box.children))
            for i in range(10):
                img = Label(text= '')
                main_wdg.ids.date_box.add_widget(img, 0)

            # main_wdg.ids.hist_box.size_hint_y= .1 * (i + 1)
            #btn0 = self.wdg.ids.btn0
            f.close()
        except:
            pass


        try:
            f = open("pray_conf.dat")
            line = f.readline()
            main_wdg.ids.latitude.text = line[:-1]
            line = f.readline()
            main_wdg.ids.longitude.text = line[:-1]
            line = f.readline()
            main_wdg.ids.timezone.text = line[:-1]
            line = f.readline()
            main_wdg.ids.isha_ref.text = lang[line[:-1]][lg]
            line = f.readline()
            main_wdg.ids.asr_madhab.text = lang[line[:-1]][lg]

            # self.wdg.ids.latitude.text = f.readline()
            # self.wdg.ids.longitude.text = f.readline()
            # self.wdg.ids.timezone.text = f.readline()
            # self.wdg.ids.isha_ref.text = f.readline()
        
            f.close()
        except:
            pass




        
    # initializing graphic objects that can't be on kv language

        Clock.schedule_interval(main_wdg.update, 1.0 / 30.0)
        # Clock.schedule_interval(self.update, 1.0 / 30.0)
        return main_wdg



    # def update():
    #     self.needle_angle = 134


    #when user exit the app auto-save his session
    def on_stop(self):
        lg = self.wdg.curent_langage


        # f = open("pray_conf.dat", "w")
        f = open("date_log.dat", "w")
        f.write(str(len(converted_date)))  
        for i in range(len(converted_date)):
            f.write("\n")
            f.write(converted_date[i])
        f.close()

        f = open("pray_conf.dat", "w")

        global latitude
        global longitude
        global timezone
        global fajr_isha_method
        fajr_isha_method = get_key_tab(self, lang, fajr_isha_method, lg)
        global asr_fiqh
        asr_fiqh = get_key_tab(self, lang, asr_fiqh, lg)
        
        # latitude = self.wdg.pray_conf.ids.latitude.text
        # longitude = self.wdg.ids.longitude.text
        # timezone = self.wdg.ids.timezone.text
        # fajr_isha_method = get_key_tab(self, lang, self.wdg.ids.isha_ref.text, lg)
        
        # fajr_isha_method = isha_ref[get_key_tab(self, lang, self.wdg.ids.isha_ref.text, lg)]

        f.write(latitude)
        f.write("\n")
        f.write(longitude)
        f.write("\n")
        f.write(timezone)
        f.write("\n")
        f.write(fajr_isha_method)
        f.write("\n")
        f.write(asr_fiqh)
        f.write("\n")
        # f.write("\n")
        f.close()
        # self.root.stop.set()


if __name__ == '__main__':
    ZaitounApp().run()



# import requests
# url = 'https://www.googleapis.com/qpxExpress/v1/trips/search?key=mykeyhere'
# payload = open("request.json")
# headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
# r = requests.post(url, data=payload, headers=headers)




























# from kivy.app import App
# from kivy.uix.widget import Widget
# from kivy.lang import Builder
# from kivy.animation import Animation
# from kivy.properties import NumericProperty

# import math 

# kv = '''
# <Dial>:
#     canvas:
#         Rotate:
#             angle: root.angle
#             origin: self.center
#         Color:
#             rgb: 1, 0, 0
#         Ellipse:    
#             size: min(self.size), min(self.size)
#             pos: 0.5*self.size[0] - 0.5*min(self.size), 0.5*self.size[1] - 0.5*min(self.size)
#         Color:
#             rgb: 0, 0, 0
#         Ellipse:    
#             size: 50, 50
#             pos: 0.5*root.size[0]-25, 0.9*root.size[1]-25
# '''
# Builder.load_string(kv)

# class Dial(Widget):
#     angle = NumericProperty(0)

#     def on_touch_down(self, touch):
#         y = (touch.y - self.center[1])
#         x = (touch.x - self.center[0])
#         calc = math.degrees(math.atan2(y, x))
#         self.prev_angle = calc if calc > 0 else 360+calc
#         self.tmp = self.angle

#     def on_touch_move(self, touch):
#         y = (touch.y - self.center[1])
#         x = (touch.x - self.center[0])
#         calc = math.degrees(math.atan2(y, x))
#         new_angle = calc if calc > 0 else 360+calc

#         self.angle = self.tmp + (new_angle-self.prev_angle)%360

#     def on_touch_up(self, touch):
#         Animation(angle=0).start(self)

# class DialApp(App):
#     def build(self):
#         return Dial()

# if __name__ == "__main__":
#     DialApp().run()

















# from kivy.app import App
# from kivy.uix.widget import Widget
# from kivy.lang import Builder
# from kivy.animation import Animation
# from kivy.properties import NumericProperty

# import math 

# kv = '''
# <Dial>:
    
#     Image:
#         id: needle
#         canvas:
#             Rotate:
#                 angle: root.angle
#                 origin: self.center
#             Color:
#                 rgb: 0, 1, 0
#             Ellipse:    
#                 size: 50, 50
#                 pos: 0.2*root.size[0]-25, 0.7*root.size[1]-25
#             Rectangle:
#                 source: 'needle.png'
# '''
# Builder.load_string(kv)

# class Dial(Widget):
#     angle = NumericProperty(90)


#     def on_touch_up(self, touch):
#         Animation(angle=0).start(self)

# class DialApp(App):
#     def build(self):
#         return Dial()

# if __name__ == "__main__":
#     DialApp().run()








# import threading   
# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.properties import NumericProperty
# from kivy.lang import Builder

# Builder.load_string(
# '''
# <Thread>:
#     Button:
#         text: "use thread"
#         on_release: root.lauch_thread()
#     Button:
#         text: "reset"
#         on_release: root.reset()
#     Label:
#         id: lbl
#         text: "Numbers"

# ''')

# class Thread(BoxLayout):
#     counter = NumericProperty(0)

#     def thread_function(self):
#         while True:
#             self.counter += 1
#             self.ids.lbl.text = "{}".format(self.counter)
#     def reset(self):
#         self.counter = 0
#         self.ids.lbl.text = "{}".format(self.counter)
#     def lauch_thread(self):
#         threading.Thread(target = self.thread_function).start()


# class MyApp(App):
#     stop = threading.Event()
#     def build(self):
#         # self.load_kv('thread.kv')
#         return Thread()

#     def on_stop(self):
#         self.root.stop.set()

# if __name__ == "__main__":
#     app = MyApp()
#     app.run()