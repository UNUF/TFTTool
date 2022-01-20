"""
TFTTool by Max Zuidberg

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import sys
import struct
import json
import string
import argparse
from pathlib import Path
from NextionChecksum import Checksum

# Disable traceback for Nuitka compiling
if not __debug__:
    sys.tracebacklimit = 0

class pdict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return json.dumps(self, indent=4)

def hexStr(raw:bytes):
    return " ".join("{:02X}".format(c) for c in raw)

class Usercode:
    class CodeBlock:
        _operandTypesEncode = {
            "local:":  0x01,
            "global:": 0x05,
            "system:": 0x04,
            "":        0x03, #actual value
        }

        # Most encodings differ for each model series.
        _listOperatorsEncode = {
            # T0/Basic
            0: {
                "jmp":      0x2054,
                "cjmp":     0x400,
                "pic":      0x401,
                "cle":      0x402,
                "ref":      0x403,
                "cir":      0x404,
                "vis":      0x405,
                "cls":      0x406,
                "get":      0x407,
                "cov":      0x408,
                "tsw":      0x409,
                "xpic":     0x40a,
                "page":     0x40b,
                "line":     0x40c,
                "fill":     0x40d,
                "pa_q":     0x40e,
                "picq":     0x40f,
                "fstr":     0x410,
                "nstr":     0x411,
                "xstr":     0x412,
                "zstr":     0x413,
                "cirs":     0x414,
                "addt":     0x415,
                "init":     0x416,
                "rfpt":     0x417,
                "wfpt":     0x418,
                "rest":     0x419,
                "draw":     0x41a,
                "covx":     0x41b,
                "click":    0x800,
                "comok":    0x801,
                "btlen":    0x802,
                "spstr":    0x803,
                "print":    0x804,
                "ucopy":    0x805,
                "code_c":   0x806,
                "draw3d":   0x807,
                "qrcode":   0x808,
                "sendme":   0x809,
                "draw_h":   0x80a,
                "printh":   0x80b,
                "strlen":   0x80c,
                "showqq":   0x80d,
                "substr":   0x80e,
                "prints":   0x80f,
                "pa_txt":   0x810,
                "udelete":  0x811,
                "strsize":  0x812,
                "crcputh":  0x813,
                "touch_j":  0x814,
                "crcputs":  0x815,
                "randset":  0x816,
                "crcrest":  0x817,
                "crcputu":  0x818,
                "lcd_dev":  0x819,
                "lhmi_cle": 0x81a,
                "whmi_cle": 0x81b,
                "setbrush": 0x81c,
                "ref_stop": 0x81d,
                "com_stop": 0x81e,
                "ref_star": 0x81f,
                "com_star": 0x820,
                "doevents": 0x821,
                "timerset": 0x822,
                "getpassw": 0x823,
                "lcd_refx": 0x824,
                "setbaudz": 0x825,
            },
            # K0/Enhanced
            1: {
                "jmp":      0x2054,
                "cjmp":     0x400,
                "pic":      0x401,
                "cle":      0x402,
                "ref":      0x403,
                "cir":      0x404,
                "vis":      0x405,
                "cls":      0x406,
                "get":      0x407,
                "cov":      0x408,
                "tsw":      0x409,
                "xpic":     0x40a,
                "page":     0x40b,
                "line":     0x40c,
                "fill":     0x40d,
                "repo":     0x40e,
                "wepo":     0x40f,
                "pa_q":     0x410,
                "picq":     0x411,
                "fstr":     0x412,
                "nstr":     0x413,
                "xstr":     0x414,
                "zstr":     0x415,
                "cirs":     0x416,
                "addt":     0x417,
                "init":     0x418,
                "rept":     0x419,
                "wept":     0x41a,
                "rfpt":     0x41b,
                "wfpt":     0x41c,
                "rest":     0x41d,
                "draw":     0x41e,
                "covx":     0x41f,
                "click":    0x800,
                "comok":    0x801,
                "btlen":    0x802,
                "spstr":    0x803,
                "print":    0x804,
                "ucopy":    0x805,
                "code_c":   0x806,
                "draw3d":   0x807,
                "qrcode":   0x808,
                "sendme":   0x809,
                "draw_h":   0x80a,
                "printh":   0x80b,
                "strlen":   0x80c,
                "cfgpio":   0x80d,
                "showqq":   0x80e,
                "substr":   0x80f,
                "prints":   0x810,
                "pa_txt":   0x811,
                "udelete":  0x812,
                "strsize":  0x813,
                "crcputh":  0x814,
                "touch_j":  0x815,
                "crcputs":  0x816,
                "randset":  0x817,
                "crcrest":  0x818,
                "crcputu":  0x819,
                "lcd_dev":  0x81a,
                "lhmi_cle": 0x81b,
                "whmi_cle": 0x81c,
                "setbrush": 0x81d,
                "ref_stop": 0x81e,
                "com_stop": 0x81f,
                "ref_star": 0x820,
                "com_star": 0x821,
                "doevents": 0x822,
                "timerset": 0x823,
                "getpassw": 0x824,
                "lcd_refx": 0x825,
                "setbaudz": 0x826,
            },
            # X3/-
            2: {
                "jmp":      0x2054,
                "cjmp":     0x400,
                "pic":      0x401,
                "cle":      0x402,
                "ref":      0x403,
                "cir":      0x404,
                "vis":      0x405,
                "cls":      0x406,
                "get":      0x407,
                "cov":      0x408,
                "tsw":      0x409,
                "xpic":     0x40a,
                "page":     0x40b,
                "line":     0x40c,
                "move":     0x40d,
                "fill":     0x40e,
                "repo":     0x40f,
                "wepo":     0x410,
                "pa_q":     0x411,
                "picq":     0x412,
                "nstr":     0x413,
                "xstr":     0x414,
                "zstr":     0x415,
                "cirs":     0x416,
                "addt":     0x417,
                "init":     0x418,
                "rept":     0x419,
                "wept":     0x41a,
                "rfpt":     0x41b,
                "wfpt":     0x41c,
                "rest":     0x41d,
                "draw":     0x41e,
                "covx":     0x41f,
                "play":     0x420,
                "click":    0x800,
                "comok":    0x801,
                "btlen":    0x802,
                "redir":    0x803,
                "spstr":    0x804,
                "print":    0x805,
                "ucopy":    0x806,
                "code_c":   0x807,
                "draw3d":   0x808,
                "qrcode":   0x809,
                "rdfile":   0x80a,
                "refile":   0x80b,
                "twfile":   0x80c,
                "sendme":   0x80d,
                "draw_h":   0x80e,
                "printh":   0x80f,
                "strlen":   0x810,
                "cfgpio":   0x811,
                "showqq":   0x812,
                "deldir":   0x813,
                "newdir":   0x814,
                "substr":   0x815,
                "prints":   0x816,
                "pa_txt":   0x817,
                "delfile":  0x818,
                "newfile":  0x819,
                "udelete":  0x81a,
                "strsize":  0x81b,
                "crcputh":  0x81c,
                "touch_j":  0x81d,
                "finddir":  0x81e,
                "crcputs":  0x81f,
                "randset":  0x820,
                "crcrest":  0x821,
                "crcputu":  0x822,
                "lcd_dev":  0x823,
                "lhmi_cle": 0x824,
                "whmi_cle": 0x825,
                "findfile": 0x826,
                "setbrush": 0x827,
                "ref_stop": 0x828,
                "com_stop": 0x829,
                "ref_star": 0x82a,
                "com_star": 0x82b,
                "setlayer": 0x82c,
                "doevents": 0x82d,
                "timerset": 0x82e,
                "getpassw": 0x82f,
                "lcd_refx": 0x830,
                "setbaudz": 0x831,
            },
           # X5/Intelligent
           3: {
               "jmp":       0x2054,
                "cjmp":     0x400,
                "pic":      0x401,
                "cle":      0x402,
                "ref":      0x403,
                "cir":      0x404,
                "vis":      0x405,
                "cls":      0x406,
                "get":      0x407,
                "cov":      0x408,
                "tsw":      0x409,
                "xpic":     0x40a,
                "page":     0x40b,
                "line":     0x40c,
                "move":     0x40d,
                "fill":     0x40e,
                "repo":     0x40f,
                "wepo":     0x410,
                "pa_q":     0x411,
                "picq":     0x412,
                "nstr":     0x413,
                "xstr":     0x414,
                "zstr":     0x415,
                "cirs":     0x416,
                "addt":     0x417,
                "init":     0x418,
                "rept":     0x419,
                "wept":     0x41a,
                "rfpt":     0x41b,
                "wfpt":     0x41c,
                "rest":     0x41d,
                "draw":     0x41e,
                "covx":     0x41f,
                "play":     0x420,
                "click":    0x800,
                "comok":    0x801,
                "btlen":    0x802,
                "redir":    0x803,
                "spstr":    0x804,
                "print":    0x805,
                "ucopy":    0x806,
                "code_c":   0x807,
                "draw3d":   0x808,
                "qrcode":   0x809,
                "rdfile":   0x80a,
                "refile":   0x80b,
                "twfile":   0x80c,
                "sendme":   0x80d,
                "draw_h":   0x80e,
                "printh":   0x80f,
                "strlen":   0x810,
                "cfgpio":   0x811,
                "showqq":   0x812,
                "deldir":   0x813,
                "newdir":   0x814,
                "substr":   0x815,
                "prints":   0x816,
                "pa_txt":   0x817,
                "delfile":  0x818,
                "newfile":  0x819,
                "udelete":  0x81a,
                "strsize":  0x81b,
                "crcputh":  0x81c,
                "touch_j":  0x81d,
                "finddir":  0x81e,
                "crcputs":  0x81f,
                "randset":  0x820,
                "crcrest":  0x821,
                "crcputu":  0x822,
                "lcd_dev":  0x823,
                "lhmi_cle": 0x824,
                "whmi_cle": 0x825,
                "findfile": 0x826,
                "setbrush": 0x827,
                "ref_stop": 0x828,
                "com_stop": 0x829,
                "ref_star": 0x82a,
                "com_star": 0x82b,
                "setlayer": 0x82c,
                "doevents": 0x82d,
                "timerset": 0x82e,
                "getpassw": 0x82f,
                "lcd_refx": 0x830,
                "setbaudz": 0x831,
           },
            # T1/Discovery
            100: {
                "jmp":      0x2054,
                "cjmp":     0x400,
                "pic":      0x401,
                "cle":      0x402,
                "ref":      0x403,
                "cir":      0x404,
                "vis":      0x405,
                "cls":      0x406,
                "get":      0x407,
                "cov":      0x408,
                "tsw":      0x409,
                "xpic":     0x40a,
                "page":     0x40b,
                "line":     0x40c,
                "fill":     0x40d,
                "pa_q":     0x40e,
                "picq":     0x40f,
                "fstr":     0x410,
                "nstr":     0x411,
                "xstr":     0x412,
                "zstr":     0x413,
                "cirs":     0x414,
                "addt":     0x415,
                "init":     0x416,
                "rfpt":     0x417,
                "wfpt":     0x418,
                "rest":     0x419,
                "draw":     0x420,
                "covx":     0x421,
                "click":    0x800,
                "comok":    0x801,
                "btlen":    0x802,
                "spstr":    0x803,
                "print":    0x804,
                "ucopy":    0x805,
                "code_c":   0x806,
                "draw3d":   0x807,
                "qrcode":   0x808,
                "sendme":   0x809,
                "draw_h":   0x80a,
                "printh":   0x80b,
                "strlen":   0x80c,
                "showqq":   0x80d,
                "substr":   0x80e,
                "prints":   0x80f,
                "pa_txt":   0x810,
                "udelete":  0x811,
                "strsize":  0x812,
                "crcputh":  0x813,
                "touch_j":  0x814,
                "crcputs":  0x815,
                "randset":  0x816,
                "crcrest":  0x817,
                "crcputu":  0x818,
                "lcd_dev":  0x819,
                "lhmi_cle": 0x81a,
                "whmi_cle": 0x81b,
                "setbrush": 0x81c,
                "ref_stop": 0x81d,
                "com_stop": 0x81e,
                "ref_star": 0x81f,
                "com_star": 0x820,
                "doevents": 0x821,
                "timerset": 0x822,
                "getpassw": 0x823,
                "lcd_refx": 0x824,
                "setbaudz": 0x825,
            },
        }
        _unaryOperators  = ["++", "--"]
        _binaryOperators = ["+", "-", "*", "/", "<<", ">>", "&", "|"]
        _binaryOperators.extend([c + "=" for c in _binaryOperators])
        _binaryOperators.append("=")

        _systemVariablesEncode = {
            # T0/Basic
            0: {
                "dp":       0x0004,
                "RED":      0x0104,
                "thc":      0x0204,
                "dim":      0x0304,
                "wup":      0x0404,
                "sya0":     0x0504,
                "tch0":     0x0604,
                "sya1":     0x0704,
                "tch1":     0x0804,
                "tch2":     0x0904,
                "tch3":     0x0a04,
                "BLUE":     0x0b04,
                "GRAY":     0x0c04,
                "rand":     0x0d04,
                "baud":     0x0e04,
                "thsp":     0x0f04,
                "ussp":     0x1004,
                "thup":     0x1104,
                "usup":     0x1204,
                "addr":     0x1304,
                "dims":     0x1404,
                "bcpu":     0x1504,
                "spax":     0x1604,
                "spay":     0x1704,
                "WHITE":    0x0008,
                "BLACK":    0x0108,
                "GREEN":    0x0208,
                "BROWN":    0x0308,
                "thdra":    0x0408,
                "appid":    0x0508,
                "bkcmd":    0x0608,
                "usize":    0x0708,
                "sleep":    0x0808,
                "tpdir":    0x0908,
                "bauds":    0x0a08,
                "delay":    0x0b08,
                "YELLOW":   0x0c08,
                "recmod":   0x0d08,
                "runmod":   0x0e08,
                "crcval":   0x0f08,
                "sendxy":   0x1008,
                "portbusy": 0x1108,
            },
            # K0/Enhanced
            1: {
                "dp":       0x0004,
                "RED":      0x0104,
                "thc":      0x0204,
                "dim":      0x0304,
                "wup":      0x0404,
                "sya0":     0x0504,
                "rtc0":     0x0604,
                "tch0":     0x0704,
                "pio0":     0x0804,
                "sya1":     0x0904,
                "rtc1":     0x0a04,
                "tch1":     0x0b04,
                "pio1":     0x0c04,
                "rtc2":     0x0d04,
                "tch2":     0x0e04,
                "pio2":     0x0f04,
                "rtc3":     0x1004,
                "tch3":     0x1104,
                "pio3":     0x1204,
                "rtc4":     0x1304,
                "pwm4":     0x1404,
                "pio4":     0x1504,
                "rtc5":     0x1604,
                "pwm5":     0x1704,
                "pio5":     0x1804,
                "rtc6":     0x1904,
                "pwm6":     0x1a04,
                "pio6":     0x1b04,
                "pwm7":     0x1c04,
                "pio7":     0x1d04,
                "BLUE":     0x0008,
                "GRAY":     0x0108,
                "rand":     0x0208,
                "baud":     0x0308,
                "pwmf":     0x0408,
                "thsp":     0x0508,
                "ussp":     0x0608,
                "thup":     0x0708,
                "usup":     0x0808,
                "addr":     0x0908,
                "dims":     0x0a08,
                "bcpu":     0x0b08,
                "spax":     0x0c08,
                "spay":     0x0d08,
                "WHITE":    0x0e08,
                "BLACK":    0x0f08,
                "GREEN":    0x1008,
                "BROWN":    0x1108,
                "thdra":    0x1208,
                "appid":    0x1308,
                "bkcmd":    0x1408,
                "usize":    0x1508,
                "sleep":    0x1608,
                "tpdir":    0x1708,
                "bauds":    0x1808,
                "delay":    0x1908,
                "YELLOW":   0x1a08,
                "recmod":   0x1b08,
                "runmod":   0x1c08,
                "crcval":   0x1d08,
                "sendxy":   0x1e08,
                "portbusy": 0x1f08,
            },
            # X3/-
            2: {
                "dp":       0x0004,
                "eq0":      0x0104,
                "eq1":      0x0204,
                "eq2":      0x0304,
                "eq3":      0x0404,
                "eq4":      0x0504,
                "eq5":      0x0604,
                "eq6":      0x0704,
                "eq7":      0x0804,
                "eq8":      0x0904,
                "eq9":      0x0a04,
                "RED":      0x0b04,
                "thc":      0x0c04,
                "aph":      0x0d04,
                "eqh":      0x0e04,
                "eql":      0x0f04,
                "dim":      0x1004,
                "eqm":      0x1104,
                "wup":      0x1204,
                "sya0":     0x1304,
                "tch0":     0x1404,
                "sya1":     0x1504,
                "tch1":     0x1604,
                "tch2":     0x1704,
                "tch3":     0x1804,
                "BLUE":     0x1904,
                "GRAY":     0x1a04,
                "tprc":     0x1b04,
                "rand":     0x1c04,
                "baud":     0x1d04,
                "thsp":     0x1e04,
                "ussp":     0x1f04,
                "thup":     0x2004,
                "usup":     0x2104,
                "addr":     0x2204,
                "dims":     0x2304,
                "bcpu":     0x2404,
                "spax":     0x2504,
                "spay":     0x2604,
                "WHITE":    0x0008,
                "BLACK":    0x0108,
                "GREEN":    0x0208,
                "BROWN":    0x0308,
                "thdra":    0x0408,
                "appid":    0x0508,
                "bkcmd":    0x0608,
                "usize":    0x0708,
                "sleep":    0x0808,
                "tpdir":    0x0908,
                "bauds":    0x0a08,
                "delay":    0x0b08,
                "audio0":   0x0c08,
                "audio1":   0x0d08,
                "YELLOW":   0x0e08,
                "recmod":   0x0f08,
                "runmod":   0x1008,
                "volume":   0x1108,
                "crcval":   0x1208,
                "sendxy":   0x1308,
                "portbusy": 0x1408,
            },
            # X5/Intelligent
            3: {
                "dp":       0x0004,
                "eq0":      0x0104,
                "eq":       0x0204,
                "eq2":      0x0304,
                "eq3":      0x0404,
                "eq4":      0x0504,
                "eq5":      0x0604,
                "eq6":      0x0704,
                "eq7":      0x0804,
                "eq8":      0x0904,
                "eq9":      0x0a04,
                "RED":      0x0b04,
                "thc":      0x0c04,
                "aph":      0x0d04,
                "eqh":      0x0e04,
                "eql":      0x0f04,
                "dim":      0x1004,
                "eqm":      0x1104,
                "wup":      0x1204,
                "sya0":     0x1304,
                "rtc0":     0x1404,
                "tch0":     0x1504,
                "pio0":     0x1604,
                "sya":      0x1704,
                "rtc":      0x1804,
                "tch":      0x1904,
                "pio":      0x1a04,
                "rtc2":     0x1b04,
                "tch2":     0x1c04,
                "pio2":     0x1d04,
                "rtc3":     0x1e04,
                "tch3":     0x1f04,
                "pio3":     0x2004,
                "rtc4":     0x2104,
                "pwm4":     0x2204,
                "pio4":     0x2304,
                "rtc5":     0x2404,
                "pwm5":     0x2504,
                "pio5":     0x2604,
                "rtc6":     0x2704,
                "pwm6":     0x2804,
                "pio6":     0x2904,
                "pwm7":     0x2a04,
                "pio7":     0x2b04,
                "BLUE":     0x2c04,
                "GRAY":     0x2d04,
                "tprc":     0x2e04,
                "rand":     0x2f04,
                "baud":     0x3004,
                "pwmf":     0x3104,
                "thsp":     0x3204,
                "ussp":     0x3304,
                "thup":     0x3404,
                "usup":     0x3504,
                "addr":     0x3604,
                "dims":     0x3704,
                "bcpu":     0x3804,
                "spax":     0x3904,
                "spay":     0x3a04,
                "WHITE":    0x0008,
                "BLACK":    0x0108,
                "GREEN":    0x0208,
                "BROWN":    0x0308,
                "thdra":    0x0408,
                "appid":    0x0508,
                "bkcmd":    0x0608,
                "usize":    0x0708,
                "sleep":    0x0808,
                "tpdir":    0x0908,
                "bauds":    0x0a08,
                "delay":    0x0b08,
                "audio0":   0x0c08,
                "audio":    0x0d08,
                "YELLOW":   0x0e08,
                "recmod":   0x0f08,
                "runmod":   0x1008,
                "volume":   0x1108,
                "crcval":   0x1208,
                "sendxy":   0x1308,
                "portbusy": 0x1408,
            },
            # T1/Discovery
            100: {
                "dp":       0x0004,
                "RED":      0x0104,
                "thc":      0x0204,
                "dim":      0x0304,
                "wup":      0x0404,
                "sya0":     0x0504,
                "tch0":     0x0604,
                "sya1":     0x0704,
                "tch1":     0x0804,
                "tch2":     0x0904,
                "tch3":     0x0a04,
                "BLUE":     0x0b04,
                "GRAY":     0x0c04,
                "rand":     0x0d04,
                "baud":     0x0e04,
                "thsp":     0x0f04,
                "ussp":     0x1004,
                "thup":     0x1104,
                "usup":     0x1204,
                "addr":     0x1304,
                "dims":     0x1404,
                "bcpu":     0x1504,
                "spax":     0x1604,
                "spay":     0x1704,
                "WHITE":    0x0008,
                "BLACK":    0x0108,
                "GREEN":    0x0208,
                "BROWN":    0x0308,
                "thdra":    0x0408,
                "appid":    0x0508,
                "bkcmd":    0x0608,
                "usize":    0x0708,
                "sleep":    0x0808,
                "tpdir":    0x0908,
                "bauds":    0x0a08,
                "delay":    0x0b08,
                "YELLOW":   0x0c08,
                "recmod":   0x0d08,
                "runmod":   0x0e08,
                "crcval":   0x0f08,
                "sendxy":   0x1008,
                "lowpower": 0x1108,
                "portbusy": 0x1208,
            },
        }
        _operandTypesDecode   = {v: k for k, v in _operandTypesEncode.items()}
        _listOperatorsDecode    = {type: {v: k for k, v in ops.items()} for type, ops in _listOperatorsEncode.items()}
        _systemVariablesDecode = {type: {v: k for k, v in sysvars.items()} for type, sysvars in _systemVariablesEncode.items()}

        def __init__(self, model_series:int, rawBlock:bytes, hexVals=True, globalVars=dict(), localVars=dict()):
            self.series = model_series
            self.raw = rawBlock
            self._asHex = hexVals
            self._globalVars = globalVars
            self._localVars  = localVars
            self.decoded = ""
            self._decode(hexVals)

        def _decode(self, hexVals=True):
            if not self.raw:
                self.decoded = "EMPTY_BLOCK"
                return
            else:
                self.decoded = ""
            operation = False
            strActive = False
            escActive = False
            skip = 0
            replaced = False
            # Check if its a (hash) value list
            # Format n * (4-byte-hash + 2-byte-index)
            isList = False
            if len(self.raw) % 6 == 0:
                entries = dict()
                for i in range(0, len(self.raw), 6):
                    value = self.raw[i + 0:i + 4]
                    key   = self.raw[i + 4:i + 6]
                    value = struct.unpack("<I", value)[0]
                    key   = struct.unpack("<H", key)[0]
                    value = self._hexOrNot(value)
                    entries[key] = value
                if (max(entries.keys()) + 1) * 6 == len(self.raw):
                    isList = True
                    for i in range(len(self.raw) // 6):
                        if i not in entries:
                            isList = False
            if isList:
                self.decoded = entries
            else:
                # Search for strings
                stringRegions = set()
                for i, b in enumerate(self.raw):
                    if strActive:
                        stringRegions.add(i)
                        if not escActive:
                            if b == ord("\\"):
                                escActive = True
                            elif b == ord("\""):
                                strActive = not strActive
                        else:
                            escActive = False
                nostrings = b"".join([chr(c).encode() for i, c in enumerate(self.raw) if i not in stringRegions])
                # Search for commands
                for op in self._unaryOperators:
                    if op.encode("ascii") in self.raw:
                        operation = True
                        break
                if not operation:
                    for op in self._binaryOperators:
                        if op.encode("ascii") in nostrings:
                            operation = True
                            break
                if not operation:
                    starts = (b"\x09", struct.pack("<H", self._listOperatorsEncode[self.series]["jmp"]))
                    for s in starts:
                        if self.raw.startswith(s):
                            l = len(s)
                            if l < 2:
                                if len(self.raw) == 3:
                                    operation = True
                                    break
                                else:
                                    l += 2
                            if l < len(self.raw):
                                c = self.raw[l]
                                if c in self._operandTypesDecode.keys() or chr(c) in string.printable:
                                    operation = True
                                    break

                if operation:
                    for i, b in enumerate(self.raw):
                        if skip:
                            skip -= 1
                            continue
                        if i not in stringRegions:
                            replaced = True
                            if b == 0x09 or (b == 0x20 and self.raw[i-1] == 0x54): # jmp is extra...
                                localI = i
                                dataStruct = "<H"
                                if b == 0x09:
                                    localI += 1
                                    skip = struct.calcsize(dataStruct)
                                else:
                                    # jmp. We need to remove the first byte of the command from the decode string
                                    self.decoded = self.decoded[:-1]
                                    localI -= 1
                                op = struct.unpack_from(dataStruct, self.raw, localI)[0]
                                if op in self._listOperatorsDecode[self.series]:
                                    self.decoded += self._listOperatorsDecode[self.series][op]
                                else:
                                    self.decoded += "op:" + self._hexOrNot(op)

                                self.decoded += " "
                            elif b in self._operandTypesDecode:
                                dataStruct = "<I"
                                skip = struct.calcsize(dataStruct)
                                try:
                                    val = struct.unpack_from(dataStruct, self.raw, i+1)[0]
                                    varLookup = dict()
                                    if b == 1: #local variable
                                        varLookup = self._localVars
                                    elif b== 5: #global variable
                                        varLookup = self._globalVars
                                    elif b == 4: #system variable
                                        varLookup = self._systemVariablesDecode[self.series]
                                    if val not in varLookup:
                                        self.decoded += self._operandTypesDecode[b] + self._hexOrNot(val)
                                    else:
                                        self.decoded += varLookup[val]
                                except:
                                    replaced = False
                            else:
                                replaced = False
                        if not replaced:
                            self.decoded += chr(b)
                else:
                    printable = True
                    for c in self.raw:
                        if chr(c) not in string.printable:
                            printable = False
                            break
                    if printable:
                        self.decoded = self.raw.decode()
                    else:
                        self.decoded = "RAW_DATA: " + hexStr(self.raw)

        def setHex(self, asHex):
            self._asHex = asHex
            self._decode()

        def _hexOrNot(self, val, asHex=-1):
            if asHex == -1:
                asHex = self._asHex
            if asHex:
                return hex(val)
            else:
                return str(val)

        def rawHex(self, raw:bytes):
            return " ".join(["{:02X}".format(c) for c in raw])

        def __repr__(self):
            if len(self.raw) == 0:
                return "EMPTY_BLOCK"
            elif self.decoded:
                return self.decoded
            else:
                return hexStr(self.raw)

    def __init__(self, model_series:int, rawUsercode:bytes, hexVals=True):
        self.series = model_series
        self.raw = rawUsercode
        nextBlock = 0
        #self.rawGlobalMem, nextBlock = self._getRawBlock(nextBlock)
        #self.rawPageList, nextBlock  = self._getRawBlock(nextBlock)
        self.blocks = dict()
        while nextBlock <= len(self.raw) - 4:
            currentBlock = nextBlock
            raw, nextBlock = self._getRawBlock(currentBlock)
            self.blocks[currentBlock] = self.CodeBlock(model_series, raw)
        #self.pages = dict()
        #for i in range(0, len(self.rawPageList), 6):
        #    value = self.rawPageList[i+0:i+4]
        #    key   = self.rawPageList[i+4:i+6]
        #    value = struct.unpack("<I", value)[0]
        #    key   = struct.unpack("<H", key)[0]
        #    self.pages[key] = value

    def _getRawBlock(self, offset):
        blockSize = struct.unpack_from("<I", self.raw, offset)[0]
        offset += 4
        newOffset = offset + blockSize
        return self.raw[offset:newOffset], newOffset

class HeaderData:
    def __init__(self, raw:bytes, properties:dict, decode_hint:int=0):
        self.size    = properties["size"]
        self.start   = properties["start"]
        self.hasCRC  = properties["hasCRC"]
        self.content = pdict(properties["content"])

        # Read content.
        self._contentStruct = "<" + "".join(v["struct"] for v in self.content.values())
        self._contentSize = struct.calcsize(self._contentStruct)
        self._emptyRegion = self.size - self._contentSize
        if self.hasCRC:
            self._emptyRegion -= 4
        if self._emptyRegion < 0:
            raise Exception("Header size mismatch")
        if len(raw) < self.size:
            raise Exception("raw size smaller than header")

        fullStruct = self._contentStruct + str(self._emptyRegion) + "x"
        if self.hasCRC:
            fullStruct += "I"

        # Now that the structure has been parsed from the content dict, convert it to a flat, "normal" k:v dict and
        # initialize it with the given default values.
        for k, v in self.content.items():
            self.content[k] = v["val"]

        data = raw[self.start: (self.start + self.size)]

        # XOR decoding. By default the key does nothing.
        self.key = bytes(len(raw))
        self.encrypted = False
        if type(decode_hint) is int:
            if decode_hint:
                self.encrypted = True
                if type(decode_hint) is int:
                    self.key = struct.pack("<I", decode_hint)
                    self.key = self.key * (self.size // len(self.key) + 1)
                else:
                    self.key = decode_hint
                # only decode the part that actually contains encoded data. Copy the rest as-is.
                data = bytes([b ^ self.key[i] for i, b in enumerate(data[:self._contentSize])]) + data[self._contentSize:]
            data = struct.unpack(fullStruct, data)
            for i, k in enumerate(self.content.keys()):
                self.content[k] = data[i]
            if self.hasCRC:
                self.crc = data[-1]
        # (partially) decoded header. In this case we ignore the data from raw.
        elif type(decode_hint) is str:
            # String can be hex data ("01 3a 44 [...]"), a json with values, or a file path to either one.
            # Check if it's a file path. If so, replace the hint with the file content.
            try:
                with open(decode_hint) as f:
                    decode_hint = f.read()
            except OSError:
                pass
            data = None
            # Check if it's a hex string...
            try:
                data = bytes.fromhex(decode_hint)
            except ValueError:
                pass
            if data:
                data = struct.unpack_from(self._contentStruct, data, 0)
                for i, k in enumerate(self.content.keys()):
                    self.content[k] = data[i]
            # ... else check if it's a json string...
            else:
                try:
                    # Double quotes get removed from the CLI if not escaped. Single quotes work, but the json parser
                    # doesn't like them.
                    data = json.loads(decode_hint.replace("\'", "\""))
                except json.decoder.JSONDecodeError:
                    pass
                if data:
                    # Skip all unknown keys.
                    for k, v in data.items():
                        if k in self.content:
                            self.content[k] = v

            # Update CRC. This requires serializing the data. Both things are done by getRaw
            # even though we don't use or need the actual raw version of the header.
            self.getRaw()


    def getRaw(self):
        raw = struct.pack(self._contentStruct, *self.content.values())
        if self.encrypted:
            raw = bytes([b ^ self.key[i] for i, b in enumerate(raw)])
        raw += b"\xff" * self._emptyRegion
        if self.hasCRC:
            self.crc = Checksum().CRC(data=raw)
            raw += struct.pack("<I", self.crc)
        return raw


class TFTFile:

    _modelXORs = {
         "NX3224T024_011": 0x6d713e32,
         "NX3224T028_011": 0x965cdd00,
         "NX4024T032_011": 0x3b91869c,
         "NX4832T035_011": 0xebab2932,
         "NX4827T043_011": 0x1eb276b6,
         "NX8048T050_011": 0x3b66b524,
         "NX8048T070_011": 0xc079789d,

         "NX3224F024_011": 0,
         "NX3224F028_011": 0,
         "NX4832F035_011": 0,

         "NX3224K024_011": 0x1324a9d7,
         "NX3224K028_011": 0xe8094ae5,
         "NX4024K032_011": 0x45c41179,
         "NX4832K035_011": 0x95febed7,
         "NX4827K043_011": 0x60e7e153,
         "NX8048K050_011": 0x453322c1,
         "NX8048K070_011": 0xbe2cef78,

         "NX4827P043_011": 0xcdc7c258,
         "NX8048P050_011": 0xe81301ca,
         "NX8048P070_011": 0x130ccc73,
         "NX1060P070_011": 0x18a58690,
         "NX1060P101_011": 0xdcb511f5,

        "TJC3224T022_011": 0x189a66fb,
        "TJC3224T024_011": 0x54cd4ea3,
        "TJC3224T028_011": 0xafe0ad91,
        "TJC4024T032_011": 0x022df60d,
        "TJC4832T035_011": 0xd21759a3,
        "TJC4827T043_011": 0x270e0627,
        "TJC8048T050_011": 0x02dac5b5,
        "TJC8048T070_011": 0xf9c5080c,

        "TJC1612T118_011": 0,
        "TJC3224T122_011": 0,
        "TJC3224T124_011": 0,
        "TJC3224T128_011": 0,
        "TJC4024T132_011": 0,
        "TJC4832T135_011": 0,

        "TJC3224K022_011": 0x66cff11e,
        "TJC3224K024_011": 0x2a98d946,
        "TJC3224K028_011": 0xd1b53a74,
        "TJC4024K032_011": 0x7c7861e8,
        "TJC4827K043_011": 0x595b91c2,
        "TJC4832K035_011": 0xac42ce46,
        "TJC8048K050_011": 0x7c8f5250,
        "TJC8048K070_011": 0x87909fe9,

        "TJC4848X340_011": 0x9ea280d2,
        "TJC4827X343_011": 0x767c3bae,
        "TJC8048X343_011": 0x5eb5f196,
        "TJC8048X350_011": 0x53a8f83c,
        "TJC8048X370_011": 0xa8b73585,
        "TJC1060X370_011": 0xa31e7f66,
        "TJC8060X380_011": 0xd9b92b5c,
        "TJC1060X3A1_011": 0x2c3a9902,

        "TJC4848X540_011": 0x8e472af9,
        "TJC4827X543_011": 0x66999185,
        "TJC8048X543_011": 0x4e505bbd,
        "TJC8048X550_011": 0x434d5217,
        "TJC8048X570_011": 0xb8529fae,
        "TJC1060X570_011": 0xb3fbd54d,
        "TJC8060X580_011": 0xc95c8177,
        "TJC1060X5A1_011": 0x3cdf3329,
    }
    _models = list(_modelXORs.keys())
    _modelCRCs = [Checksum().CRC(data=m.encode("ascii")) for m in _models]

    _fileHeader1 = {
        "size":    0xc8,
        "start":   0x00,
        "hasCRC":  True,
        "content": {
            "old_lcd_orientation":                  {"struct": "B", "val": 0}, # editor fixes this to 0
            "editor_version_main":                  {"struct": "B", "val": 0},
            "editor_version_sub":                   {"struct": "B", "val": 0},
            "editor_vendor":                        {"struct": "B", "val": 0},
            "unknown_old_firmware_address":         {"struct": "I", "val": 0},
            "unknwon_old_firmware_size":            {"struct": "I", "val": 0},
            "old_lcd_resolution_width":             {"struct": "H", "val": 0}, # always largest resolution
            "old_lcd_resolution_height":            {"struct": "H", "val": 0}, # always smallest resolution
            "lcd_resolution_x":                     {"struct": "H", "val": 0}, # x-resolution in current orientation (cf ui_orientation)
            "lcd_resolution_y":                     {"struct": "H", "val": 0}, # y-resolution in current orientation (cf ui_orientation)
            "ui_orientation":                       {"struct": "B", "val": 0},
            "model_series":                         {"struct": "B", "val": 0}, # 0=T0, 1=K0, 2=X3, 3=X5, 100=T1
            "unknown_otp":                          {"struct": "B", "val": 0},
            "editor_version_bugfix":                {"struct": "B", "val": 3},
            "unknown_stm32_lcddriver_address":      {"struct": "I", "val": 0},
            "unknown_res1":                         {"struct": "H", "val": 0},
            "unknown_old_stm32_lcddriver_address":  {"struct": "I", "val": 0},
            "unknown_stm32_lcddriver_size":         {"struct": "I", "val": 0},
            "unknown_stm32_binary_address":         {"struct": "I", "val": 0},
            "unknown_stm32_binary_size":            {"struct": "I", "val": 0},
            "model_crc":                            {"struct": "I", "val": 0},
            "file_version":                         {"struct": "B", "val": 0},
            "unknown_encode_start":                 {"struct": "B", "val": 0},
            "ressources_files_address":             {"struct": "I", "val": 0},
            "ressources_files_count":               {"struct": "I", "val": 0},
            "file_size":                            {"struct": "I", "val": 0},
            "ressource_files_size":                 {"struct": "I", "val": 0},
            "ressource_files_crc":                  {"struct": "I", "val": 0},
            "unknown_memory_fs_size":               {"struct": "I", "val": 0},
            "unknown_next_file_address":            {"struct": "I", "val": 0},
            "unknown_file_id":                      {"struct": "I", "val": 0},
            "unknown_metadata_size":                {"struct": "I", "val": 0},
        },
    }
    _fileHeader2 = {
        "size":    0xc8,
        "start":   0xc8,
        "hasCRC":  True,
        "content": {
            "static_usercode_address":      {"struct": "I", "val": 0},
            "unknown_app_vas_address":      {"struct": "I", "val": 0},
            "unknown_app_vas_count":        {"struct": "I", "val": 0},
            "app_attributes_data_address":  {"struct": "I", "val": 0},
            "ressources_files_address":     {"struct": "I", "val": 0},
            "usercode_address":             {"struct": "I", "val": 0},
            "unknown_pages_address":        {"struct": "I", "val": 0},
            "unknown_objects_address":      {"struct": "I", "val": 0},
            "pictures_address":             {"struct": "I", "val": 0},
            "gmovs_address":                {"struct": "I", "val": 0},
            "videos_address":               {"struct": "I", "val": 0},
            "audios_address":               {"struct": "I", "val": 0},
            "fonts_address":                {"struct": "I", "val": 0},
            "unknown_maincode_binary":      {"struct": "I", "val": 0},
            "pages_count":                  {"struct": "H", "val": 0},
            "unknown_objects_count":        {"struct": "H", "val": 0},
            "pictures_count":               {"struct": "H", "val": 0},
            "gmovs_count":                  {"struct": "H", "val": 0},
            "videos_count":                 {"struct": "H", "val": 0},
            "audios_count":                 {"struct": "H", "val": 0},
            "fonts_count":                  {"struct": "H", "val": 0},
            "unknown_res1":                 {"struct": "H", "val": 0},
            "unknown_encode":               {"struct": "B", "val": 0},
            "unknown_res2":                 {"struct": "B", "val": 0},
            "unknown_res3":                 {"struct": "H", "val": 0},
        },
    }

    def __init__(self, raw:bytes, hexVals=True, header2_hint:str="", decode_usercode=True):
        self.raw = raw
        self.hexVals = hexVals
        self.header1 = HeaderData(self.raw, self._fileHeader1)
        try:
            self.model = self._models[self._modelCRCs.index(self._getVal("model_crc"))]
        except:
            self.model = "Unknown display model"
        decode_hint = 0
        if self.model in self._modelXORs:
            decode_hint = self._modelXORs[self.model]
        if header2_hint:
            decode_hint = header2_hint
        self.header2 = HeaderData(self.raw, self._fileHeader2, decode_hint)

        # Decode Usercode if requested
        self.usercode = None
        if decode_usercode:
            self.decode_usercode(hexVals=hexVals)

    def decode_usercode(self, hexVals=True):
        self.usercode = Usercode(self._getVal("model_series"), self.getRawUsercode(), hexVals)

    def getRawBootloader(self):
        start = self._getVal("ressources_files_address")
        end = start + self._getVal("ressources_files_size")
        return self.raw[start:end]

    def getRawPictures(self):
        start = self._getVal("pictures_address")
        end = start + self._getVal("gmovs_address")
        return self.raw[start:end]

    def getRawFonts(self):
        # Hacky.
        end = -1
        for i in reversed(range(self._getVal("fonts_address"), self._getVal("usercode_address"))):
            if(self.raw[i] != 0x00):
                end = i + 1
                break
        if end > 0:
            return self.raw[self._getVal("fonts_address") : end]
        else:
            return b""

    def getRawUsercode(self):
        return self.raw[self._getVal("usercode_address") : self._getVal("unknown_pages_address")]

    def exportRawBootloader(self, path = "/Raw/Bootloader.bin"):
        with open(path, "w") as f:
            f.write(self.getRawBootloader())

    def exportRawPictures(self, path = "/Raw/Pictures.bin"):
        with open(path, "w") as f:
            f.write(self.getRawPictures())

    def exportRawFonts(self, path = "/Raw/Fonts.bin"):
        with open(path, "w") as f:
            f.write(self.getRawFonts())

    def exportRawUsercode(self, path = "/Raw/Usercode.bin"):
        with open(path, "w") as f:
            f.write(self.getRawUsercode())

    def getReadable(self, includeUnknowns = False, includeBins = False):
        d = pdict()
        d["GeneralInfo"] = {"Target Model": self.model}
        if not self.header2.encrypted:
            d["GeneralInfo"]["Header 2 XOR Key"] = "Unknown (used 0x00)"
        d["Header1"]     = dict([(k, v) for k,v in self.header1.content.items() if includeUnknowns or (not k.startswith("unknown"))])
        d["Header2"]     = dict([(k, hex(v)) for k,v in self.header2.content.items() if includeUnknowns or (not k.startswith("unknown"))])
        d["Bootloader"]  = "[binary data]"
        d["Pictures"]    = "[binary data]"
        d["Fonts"]       = "[binary data]"
        d["Usercode"]    = dict()

        if includeBins:
            d["Bootloader"] = hexStr(self.getRawBootloader())
            d["Pictures"]   = hexStr(self.getRawPictures())
            d["Fonts"]      = hexStr(self.getRawFonts())

        for addr,block in self.usercode.blocks.items():
            if self.hexVals:
                addr = hex(addr)
            d["Usercode"][addr] = block.decoded

        return str(d)

    def _getVal(self, key:str):
        if key in self.header1.content:
            return self.header1.content[key]
        elif key in self.header2.content:
            return self.header2.content[key]
        else:
            raise Exception("Value \"" + key + "\" not found in headers.")

    def setModel(self, model:str, force=False):
        if model not in self._models:
            raise Exception("Unknown model " + model)
        if model not in self._modelXORs:
            raise Exception("Unable to convert to specified model because the corresponding XOR key"
                            " is missing in the database.")
        # Vendor aside, the first 6 letters of the model name contain resolution and series
        # (NX8048T070 = 80, 48, T0 f.ex.)
        # These values must match, otherwise a simple conversion is not possible.
        current = self.model.lstrip("NX").lstrip("TJC")[:6]
        new     = model.lstrip("NX").lstrip("TJC")[:6]
        if not force and new != current:
            raise Exception("Cannot convert to a model with different resolution or from a different series.")
            pass

        # Set vendor, model CRC and XOR key to the new model
        self.model = model
        self.header1.content["editor_vendor"] = ord(model[0])
        self.header1.content["model_crc"] = self._modelCRCs[self._models.index(model)]
        self.header2.xor = self._modelXORs[model]

        # Convert modified headers back to raw, which also updates the header checksums
        raw  = self.header1.getRaw()
        raw += self.header2.getRaw()

        # Copy updated raw header content into the file raw
        self.raw = raw + self.raw[len(raw):]

        # Update file checksum with the correct checksum algorithm
        series = self._getVal("model_series")
        if series not in (0, 1, 2, 3, 100):
            raise Exception(f"Unknown model series ({series}).")
        # Remove old checksum
        self.raw = self.raw[:-4]
        if series in (2, 3):
            # word based
            words = len(self.raw) // 4
            missingBytes = len(self.raw) - words * 4
            words = list(struct.unpack("<{}I".format(words), self.raw + b"\x00" * missingBytes))
            checksum = Checksum().CRC(data=words)
        else:
            # byte based
            checksum = Checksum().CRC(data=self.raw)
        # Checksum LSB is XORed with some bytes from the header
        checksum ^= self.raw[0x03] ^ self.raw[0x2e] ^ self.raw[0x3c]
        self.raw += struct.pack("<I", checksum)


### Here begins the argparsing
if __name__ == '__main__':
    desc = "TFTTool v1.0.0 - Analyze and convert TFT files. " \
           "Note that the analyze part is very work-in-progress-ish. " \
           "Developped by Max Zuidberg, non-commercial usage only."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-i", "--input", metavar="TFT_FILE", type=str, required=True,
                        help="Path to the TFT source file")
    parser.add_argument("-o", "--output", metavar="OUTPUT_FILE", type=str, required=False, default="",
                        help="Optional path to the resulting text or TFT file. If only a folder is specified, the file "
                             "name is automatically determined based on the input file.")
    parser.add_argument("-t", "--target", default="TXT",
                        help="Optional parameter to specify a new model. No text file will be created but rather "
                             "a new TFT file according to the specified model. If no output file/folder is specified, "
                             "a new file will be created in the same directory with the new model as suffix to the "
                             "original file name. Use -t LIST to list all available models. Use -t NXT or -t TJC "
                             "to keep the original model but change the vendor. Note that this does not work for the "
                             "X3, X5 and P series.")
    parser.add_argument("--header2", default="",
                        help="Optional parameter to provide the decoded header 2 for T1/Discovery series files. Can "
                             "either be a string with a json (see TFTTool source for the parameters and their names "
                             "that header 2 includes), or a string with the raw hex values (\"00 01 AC D3 ...\") "
                             "or a path to a file with either a json or a hex string. In the case of the hex string "
                             "the full header is required (minus the empty part at the end). In the case of the json "
                             "the order and the number of parameters given does not matter. However, when the argument "
                             "is a json string you must enclose it with double quotes and use single quotes within the "
                             "json string like this: \"{'hello':42,'world':26}\". For the json file this is possible, "
                             "too, but not required. Alternatively, you must escape the double quotes in the json "
                             "string (\"{\\\"hello\\\":42,\\\"world\\\":26}\". This does not work for the json file.")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Add this flag to skip the model check during conversion. Not recommended and probably "
                             "doesn't give you the results you want. Use at your own risk. ")
    parser.add_argument("-v", action="store_true",
                        help="Add this flag to write the decoded text to the console. Useless with -t")

    args = parser.parse_args()
    tftPath = Path(args.input)
    if not tftPath.exists():
        parser.error("Invalid source file!")
    outputPath = args.output
    if outputPath:
        outputPath = Path(outputPath)

    with open(tftPath, "rb") as f:
        tft = TFTFile(f.read(), header2_hint=args.header2)

    args.target = args.target.upper()
    if args.target == "TXT":
        result = tft.getReadable(includeUnknowns=True)
        if args.v:
            print(result)
        if outputPath:
            if outputPath.is_dir():
                outputPath /= tftPath.with_suffix(".txt").name
            try:
                with open(outputPath, "w") as f:
                    f.write(result)
            except:
                parser.error("Can't open output file!")
    elif args.target == "LIST":
        def s(model):
            # Returns an ascending number to sort models by series, resolution, then size
            val = ["T", "K", "P", "X"].index(model[-8:-7])
            val <<= 4
            val += int(model[-7:-6])
            val <<= 8
            val += ord(model[0])
            val <<= 16
            val += int(model[-12:-10].replace("10", "100")) * int(model[-10:-8])
            val <<= 16
            val += int(model[-6:-4], 16)
            return val
        print("List of all supported models:")
        models = sorted(tft._modelXORs.keys(), key=s)
        for m in models:
            print("  " + m.replace("NX", " NX"))
    else:
        if args.target in ("NXT", "TJC"):
            args.target = args.target.rstrip("T") + tft.model[-12:]
        elif not args.target.endswith("_011"):
            args.target += "_011"

        tft.setModel(args.target, args.force)

        if not outputPath or outputPath == tftPath:
            outputPath = tftPath.with_stem(tftPath.stem + "_" + args.target)
        elif outputPath.is_dir():
            outputPath /= tftPath.with_stem(tftPath.stem + "_" + args.target).name
        else:
            outputPath = outputPath.with_suffix(".tft")
        with open(outputPath, "wb") as f:
            f.write(tft.raw)

