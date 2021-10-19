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
        _listOperatorsEncode = {
            "com_stop": 0x081E,
            "com_star": 0x0820,
            "code_c":   0x0806,
            "click":    0x0800,
            "cir":      0x0404,
            "cirs":     0x0414,
            "cjmp":     0x0400,
            "cls":      0x0406,
            "covx":     0x041B,
            "crcrest":  0x0817,
            "crcputs":  0x0815,
            "doevents": 0x0821,
            "draw":     0x041A,
            "fill":     0x040D,
            "get":      0x0407,
            "line":     0x040C,
            "page":     0x040B,
            "printh":   0x080B,
            "prints":   0x080F,
            "pic":      0x0401,
            "picq":     0x040F,
            "ref_stop": 0x081D,
            "ref_star": 0x081F,
            "randset":  0x0816,
            "ref":      0x0403,
            "sendme":   0x0809,
            "strlen":   0x080C,
            "spstr":    0x0803,
            "touch_j":  0x0814,
            "tsw":      0x0409,
            "vis":      0x0405,
            "jmp":      0x2054,
            # Components (prefixed with "c_")
            # "c_text":    0x081c,

        }
        _unaryOperators  = ["++", "--"]
        _binaryOperators = ["+", "-", "*", "/", "<<", ">>", "&", "|"]
        _binaryOperators.extend([c + "=" for c in _binaryOperators])
        _binaryOperators.append("=")

        _systemVariablesEncode = {
            "dp":     0x00000004,
            "WHITE":  0x00000008,
            "RED":    0x00000104,
            "BLACK":  0x00000108,
            "thc":    0x00000204,
            "GREEN":  0x00000208,
            "dim":    0x00000304,
            "BROWN":  0x00000308,
            "wup":    0x00000404,
            "thdra":  0x00000408,
            "tch0":   0x00000604,
            "bkcmd":  0x00000608,
            "usize":  0x00000708,
            "tch1":   0x00000804,
            "sleep":  0x00000808,
            "tch2":   0x00000904,
            "tch3":   0x00000A04,
            "bauds":  0x00000A08,
            "BLUE":   0x00000B04,
            "delay":  0x00000B08,
            "GRAY":   0x00000C04,
            "YELLOW": 0x00000C08,
            "recmod": 0x00000D08,
            "baud":   0x00000E04,
            "thsp":   0x00000F04,
            "crcval": 0x00000F08,
            "ussp":   0x00001004,
            "sendxy": 0x00001008,
            "thup":   0x00001104,
            "usup":   0x00001204,
            "addr":   0x00001304,
            "dims":   0x00001404,
            "spax":   0x00001604,
            "spay":   0x00001704,
        }
        _operandTypesDecode    = dict([(v, k) for k, v in _operandTypesEncode.items()])
        _listOperatorsDecode   = dict([(v, k) for k, v in _listOperatorsEncode.items()])
        _systemVariablesDecode = dict([(v, k) for k, v in _systemVariablesEncode.items()])

        def __init__(self, rawBlock:bytes, hexVals=True, globalVars=dict(), localVars=dict()):
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
                    starts = (b"\x09", struct.pack("<H", self._listOperatorsEncode["jmp"]))
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
                                if op in self._listOperatorsDecode:
                                    self.decoded += self._listOperatorsDecode[op]
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
                                        varLookup = self._systemVariablesDecode
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

    def __init__(self, rawUsercode:bytes, hexVals=True):
        self.raw = rawUsercode
        nextBlock = 0
        #self.rawGlobalMem, nextBlock = self._getRawBlock(nextBlock)
        #self.rawPageList, nextBlock  = self._getRawBlock(nextBlock)
        self.blocks = dict()
        while nextBlock < len(self.raw):
            currentBlock = nextBlock
            raw, nextBlock = self._getRawBlock(nextBlock)
            self.blocks[currentBlock] = self.CodeBlock(raw)
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
    def __init__(self, raw:bytes, properties:dict, xor:int=0):
        self.xor     = xor
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

        data = struct.unpack_from(fullStruct, raw, self.start)
        for i,k in enumerate(self.content.keys()):
            self.content[k] = data[i] ^ self.xor
        if self.hasCRC:
            self.crc = data[-1]

    def getRaw(self):
        data = [d ^ self.xor for d in self.content.values()]
        raw = struct.pack(self._contentStruct, *data)
        raw += b"\xff" * self._emptyRegion
        if self.hasCRC:
            self.crc = Checksum().CRC(data=raw)
            raw += struct.pack("<I", self.crc)
        return raw

class TFTFile:
    _models = [
        "TJC3224T022_011",
        "TJC3224T024_011",
        "TJC3224T028_011",
        "TJC4024T032_011",
        "TJC4832T035_011",
        "TJC4827T043_011",
        "TJC8048T050_011",
        "TJC8048T070_011",
        "TJC3224T122_011",
        "TJC3224T124_011",
        "TJC3224T128_011",
        "TJC4024T132_011",
        "TJC4832T135_011",
        "TJC3224K022_011",
        "TJC3224K024_011",
        "TJC3224K028_011",
        "TJC4024K032_011",
        "TJC4832K035_011",
        "TJC4827K043_011",
        "TJC8048K050_011",
        "TJC8048K070_011",
        "TJC4848X340_011",
        "TJC4827X343_011",
        "TJC8048X343_011",
        "TJC8048X350_011",
        "TJC8048X370_011",
        "TJC1060X370_011",
        "TJC8060X380_011",
        "TJC1060X3A1_011",
        "TJC4848X540_011",
        "TJC4827X543_011",
        "TJC8048X543_011",
        "TJC8048X550_011",
        "TJC8048X570_011",
        "TJC1060X570_011",
        "TJC8060X580_011",
        "TJC1060X5A1_011",
         "NX3224T024_011",
         "NX3224T028_011",
         "NX4024T032_011",
         "NX4832T035_011",
         "NX4827T043_011",
         "NX8048T050_011",
         "NX8048T070_011",
         "NX3224K024_011",
         "NX3224K028_011",
         "NX4024K032_011",
         "NX4832K035_011",
         "NX4827K043_011",
         "NX8048K050_011",
         "NX8048K070_011",
         "NX4827P043_011",
         "NX8048P050_011",
         "NX8048P070_011",
         "NX1060P070_011",
         "NX1060P101_011",
    ]
    _modelCRCs = [Checksum().CRC(data=m.encode("ascii")) for m in _models]

    _modelXORs = {
         "NX4024K032_011": 0x45c41179,
         "NX4832K035_011": 0x95febed7,
         "NX4827K043_011": 0x60e7e153,
         "NX8048K050_011": 0x453322c1,
         "NX8048K070_011": 0xbe2cef78,
         "NX3224T028_011": 0x965cdd00,
         "NX4024T032_011": 0x3b91869c,
         "NX4832T035_011": 0xebab2932,
         "NX4827T043_011": 0x1eb276b6,
         "NX8048T050_011": 0x3b66b524,
         "NX8048T070_011": 0xc079789d,
         "NX3224K024_011": 0x1324a9d7,
         "NX3224K028_011": 0xe8094ae5,
         "NX3224T024_011": 0x6d713e32,

        "TJC3224K022_011": 0x66cff11e,
        "TJC3224K024_011": 0x2a98d946,
        "TJC3224K028_011": 0xd1b53a74,
        "TJC3224T022_011": 0x189a66fb,
        "TJC3224T024_011": 0x54cd4ea3,
        "TJC3224T028_011": 0xafe0ad91,
        "TJC4024K032_011": 0x7c7861e8,
        "TJC4024T032_011": 0x022df60d,
        "TJC4827K043_011": 0x595b91c2,
        "TJC4827T043_011": 0x270e0627,
        "TJC4832K035_011": 0xac42ce46,
        "TJC4832T035_011": 0xd21759a3,
        "TJC8048K050_011": 0x7c8f5250,
        "TJC8048K070_011": 0x87909fe9,
        "TJC8048T050_011": 0x02dac5b5,
        "TJC8048T070_011": 0xf9c5080c,

        "NX1060P070_011": 0x18a58690,
        "NX1060P101_011": 0xdcb511f5,
        "NX8048P050_011": 0xe81301ca,
        "NX8048P070_011": 0x130ccc73,
        "TJC1060X370_011": 0xa31e7f66,
        "TJC1060X3A1_011": 0x2c3a9902,
        "TJC1060X570_011": 0xb3fbd54d,
        "TJC1060X5A1_011": 0x3cdf3329,
        "TJC4827X343_011": 0x767c3bae,
        "TJC4827X543_011": 0x66999185,
        "TJC4848X340_011": 0x9ea280d2,
        "TJC4848X540_011": 0x8e472af9,
        "TJC8048X343_011": 0x5eb5f196,
        "TJC8048X350_011": 0x53a8f83c,
        "TJC8048X370_011": 0xa8b73585,
        "TJC8048X543_011": 0x4e505bbd,
        "TJC8048X550_011": 0x434d5217,
        "TJC8048X570_011": 0xb8529fae,
        "TJC8060X380_011": 0xd9b92b5c,
        "TJC8060X580_011": 0xc95c8177,
    }

    _fileHeader1 = {
        "size":    0xc8,
        "start":   0x00,
        "hasCRC":  True,
        "content": {
            "unknown0":                {"struct": "B", "val": None},
            "editorVersionMain":       {"struct": "B", "val": None},
            "editorVersionSub":        {"struct": "B", "val": None},
            "editorVendor":            {"struct": "B", "val": None},
            "unknown1":                {"struct": "I", "val": None},
            "brv0":                    {"struct": "H", "val": None}, #bootloader related value 0
            "unknown2":                {"struct": "H", "val": None},
            "resolutionHor":           {"struct": "H", "val": None},
            "resolutionVer":           {"struct": "H", "val": None},
            "resolutionHorCopy":       {"struct": "H", "val": None},
            "resolutionVerCopy":       {"struct": "H", "val": None},
            "orientation":             {"struct": "B", "val": None},
            "fileCRCAlgorithm":        {"struct": "H", "val": None},
            "editorVersionBugfix":     {"struct": "B", "val": None},
            "brv1":                    {"struct": "H", "val": None}, #bootloader related value 1
            "unknown4":                {"struct": "H", "val": None},
            "unknown5":                {"struct": "H", "val": None},
            "brv1Copy":                {"struct": "H", "val": None},
            "unknown4Copy":            {"struct": "H", "val": None},
            "unknown6":                {"struct": "I", "val": None},
            "unknown7":                {"struct": "I", "val": None},
            "brv2":                    {"struct": "H", "val": None}, #bootloader related value 2
            "unknown8":                {"struct": "H", "val": None},
            "modelCRC":                {"struct": "I", "val": None},
            "unknown9":                {"struct": "H", "val": None},
            "sectionSize":             {"struct": "I", "val": None},
            "unknown10":               {"struct": "I", "val": None},
            "fileLength":              {"struct": "I", "val": None},
            "unknown11":               {"struct": "I", "val": None},
            "bootloaderRessourcesCRC": {"struct": "I", "val": None},
            "unknown12":               {"struct": "I", "val": None},
        },
    }
    _fileHeader2 = {
        "size":    0xc8,
        "start":   0xc8,
        "hasCRC":  True,
        "content": {
            "usercodeLength":          {"struct": "I", "val": None},
            "usercodeLengthCopy":      {"struct": "I", "val": None},
            "unknown21":               {"struct": "I", "val": None},
            "unknown22":               {"struct": "I", "val": None},
            "bootloaderStart":         {"struct": "I", "val": None},
            "usercodeStart":           {"struct": "I", "val": None},
            "unknown23":               {"struct": "I", "val": None},
            "unknown24":               {"struct": "I", "val": None},
            "ressourcesPicturesStart": {"struct": "I", "val": None},
            "unknown25":               {"struct": "I", "val": None}, # POSSIBLY the key
            "unknown26":               {"struct": "I", "val": None},
            "unknown27":               {"struct": "I", "val": None},
            "ressourcesFontsStart":    {"struct": "I", "val": None},
            "unknown28":               {"struct": "I", "val": None},
            "unknown29":               {"struct": "I", "val": None},
            "ressourcesPicturesCount": {"struct": "I", "val": None},
            "unknown30":               {"struct": "I", "val": None},
            "ressourcesFontsCount":    {"struct": "I", "val": None},
            "unknown31":               {"struct": "I", "val": None},
        },
    }

    def __init__(self, raw:bytes, hexVals=True):
        self.raw = raw
        self.hexVals = hexVals
        self.header1 = HeaderData(self.raw, self._fileHeader1)
        try:
            self.model = self._models[self._modelCRCs.index(self._getVal("modelCRC"))]
        except:
            self.model = "Unknown display model"
        xor = 0
        if self.model in self._modelXORs:
            xor = self._modelXORs[self.model]
        self.header2 = HeaderData(self.raw, self._fileHeader2, xor)

        # Decode Usercode:
        usercodeStart = self._getVal("usercodeStart")
        usercodeEnd   = usercodeStart + self._getVal("usercodeLength")
        self.usercode = Usercode(self.raw[usercodeStart : usercodeEnd], hexVals)

    def getRawBootloader(self):
        return self.raw[self._getVal("bootloaderStart") : self._getVal("ressourcesPicturesStart")]

    def getRawPictures(self):
        return self.raw[self._getVal("ressourcesPicturesStart") : self._getVal("ressourcesFontsStart")]

    def getRawFonts(self):
        # Hacky.
        end = -1
        for i in reversed(range(self._getVal("ressourcesFontsStart"), self._getVal("usercodeStart"))):
            if(self.raw[i] != 0x00):
                end = i + 1
                break
        if end > 0:
            return self.raw[self._getVal("ressourcesFontsStart") : end]
        else:
            return b""

    def getRawUsercode(self):
        return self.raw[self._getVal("usercodeStart") : -4]

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
        d["GeneralInfo"] = {"Target Model": self.model, "Header 2 XOR Key": hex(self.header2.xor)}
        if not self.header2.xor:
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
        self.header1.content["editorVendor"] = ord(model[0])
        self.header1.content["modelCRC"] = self._modelCRCs[self._models.index(model)]
        self.header2.xor = self._modelXORs[model]

        # Convert modified headers back to raw, which also updates the header checksums
        raw  = self.header1.getRaw()
        raw += self.header2.getRaw()

        # Copy updated raw header content into the file raw
        self.raw = raw + self.raw[len(raw):]

        # Update file checksum with the correct checksum algorithm
        crcAlgo = self._getVal("fileCRCAlgorithm")
        if crcAlgo not in (0, 1, 2, 3):
            raise Exception("Unknown file CRC ({}).".format(crcAlgo))
        # Remove old checksum
        self.raw = self.raw[:-4]
        if crcAlgo >= 2:
            # word based
            words = len(self.raw) // 4
            missingBytes = len(self.raw) - 4 * words
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
        tft = TFTFile(f.read())

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

