all_instruction_sets = [
    {
        'versions': [
            'nxt-0.58',
        ],
        'models': {
            0: {
                'numerated_operators': {
                    8: [
                        'click', 'comok', 'btlen', 'print', 'ucopy', 'code_c', 'draw3d', 'qrcode', 'sendme', 'draw_h',
                        'printh', 'strlen', 'showqq', 'substr', 'prints', 'pa_txt', 'udelete', 'strsize', 'touch_j',
                        'randset', 'lcd_dev', 'lhmi_cle', 'whmi_cle', 'setbrush', 'ref_stop', 'com_stop', 'ref_star',
                        'com_star', 'doevents', 'timerset', 'getpassw', 'lcd_refx', 'setbaudz',
                    ],
                    4: [
                        'i', 'pic', 'cle', 'ref', 'cir', 'vis', 'cls', 'get', 'cov', 'tsw', 'xpic', 'page', 'line',
                        'fill', 'pa_q', 'picq', 'fstr', 'nstr', 'xstr', 'zstr', 'cirs', 'addt', 'init', 'rfpt', 'wfpt',
                        'rest', 'draw', 'covx',
                    ],
                },
                'numerated_system_variables': {
                    4: [
                        'dp', 'RED', 'thc', 'dim', 'wup', 'sya0', 'tch0', 'sys0', 'sya1', 'tch1', 'sys1', 'tch2',
                        'sys2', 'tch3', 'BLUE', 'GRAY', 'rand', 'baud', 'thsp', 'ussp', 'thup', 'usup', 'addr', 'dims',
                        'bcpu', 'spax', 'spay',
                    ],
                    8: [
                        'WHITE', 'BLACK', 'GREEN', 'BROWN', 'thdra', 'appid', 'bkcmd', 'usize', 'sleep', 'bauds',
                        'delay', 'YELLOW', 'recmod', 'runmod', 'sendxy', 'portbusy',
                    ],
                },
                'other_operators': {
                    'unary': [
                        '++', '--',
                    ],
                    'binary': [
                        '+', '-', '*', '/', '<<', '>>', '&', '|', '^', '=', '+=', '-=', '*=', '/=', '<<=', '>>=', '&=',
                        '|=', '^=',
                    ],
                    'jmp': 0x2054,
                },
            },
            1: {
                'numerated_operators': {
                    8: [
                        'click', 'comok', 'btlen', 'print', 'ucopy', 'code_c', 'draw3d', 'qrcode', 'sendme', 'draw_h',
                        'printh', 'strlen', 'cfgpio', 'showqq', 'substr', 'prints', 'pa_txt', 'udelete', 'strsize',
                        'touch_j', 'randset', 'lcd_dev', 'lhmi_cle', 'whmi_cle', 'setbrush', 'ref_stop', 'com_stop',
                        'ref_star', 'com_star', 'doevents', 'timerset', 'getpassw', 'lcd_refx', 'setbaudz',
                    ],
                    4: [
                        'i', 'pic', 'cle', 'ref', 'cir', 'vis', 'cls', 'get', 'cov', 'tsw', 'xpic', 'page', 'line',
                        'fill', 'repo', 'wepo', 'pa_q', 'picq', 'fstr', 'nstr', 'xstr', 'zstr', 'cirs', 'addt', 'init',
                        'rept', 'wept', 'rfpt', 'wfpt', 'rest', 'draw', 'covx',
                    ],
                },
                'numerated_system_variables': {
                    4: [
                        'dp', 'RED', 'thc', 'dim', 'wup', 'sya0', 'rtc0', 'tch0', 'pio0', 'sys0', 'sya1', 'rtc1',
                        'tch1', 'pio1', 'sys1', 'rtc2', 'tch2', 'pio2', 'sys2', 'rtc3', 'tch3', 'pio3', 'rtc4', 'pwm4',
                        'pio4', 'rtc5', 'pwm5', 'pio5', 'rtc6', 'pwm6', 'pio6', 'pwm7', 'pio7', 'BLUE', 'GRAY', 'rand',
                        'baud', 'pwmf', 'thsp', 'ussp', 'thup', 'usup', 'addr', 'dims', 'bcpu', 'spax', 'spay',
                    ],
                    8: [
                        'WHITE', 'BLACK', 'GREEN', 'BROWN', 'thdra', 'appid', 'bkcmd', 'usize', 'sleep', 'bauds',
                        'delay', 'YELLOW', 'recmod', 'runmod', 'sendxy', 'portbusy',
                    ],
                },
                'other_operators': {
                    'unary': [
                        '++', '--',
                    ],
                    'binary': [
                        '+', '-', '*', '/', '<<', '>>', '&', '|', '^', '=', '+=', '-=', '*=', '/=', '<<=', '>>=', '&=',
                        '|=', '^=',
                    ],
                    'jmp': 0x2054,
                },
            },
            2: {
                'numerated_operators': {
                    8: [
                        'click', 'comok', 'btlen', 'redir', 'print', 'ucopy', 'code_c', 'draw3d', 'qrcode', 'rdfile',
                        'refile', 'twfile', 'sendme', 'draw_h', 'printh', 'strlen', 'cfgpio', 'showqq', 'deldir',
                        'newdir', 'substr', 'prints', 'pa_txt', 'delfile', 'newfile', 'udelete', 'strsize', 'touch_j',
                        'finddir', 'randset', 'lcd_dev', 'lhmi_cle', 'whmi_cle', 'findfile', 'setbrush', 'ref_stop',
                        'com_stop', 'ref_star', 'com_star', 'setlayer', 'doevents', 'timerset', 'getpassw', 'lcd_refx',
                        'setbaudz',
                    ],
                    4: [
                        'i', 'pic', 'cle', 'ref', 'cir', 'vis', 'cls', 'get', 'cov', 'tsw', 'xpic', 'page', 'line',
                        'move', 'fill', 'repo', 'wepo', 'pa_q', 'picq', 'nstr', 'xstr', 'zstr', 'cirs', 'addt', 'init',
                        'rept', 'wept', 'rfpt', 'wfpt', 'rest', 'draw', 'covx', 'play',
                    ],
                },
                'numerated_system_variables': {
                    4: [
                        'dp', 'eq0', 'eq1', 'eq2', 'eq3', 'eq4', 'eq5', 'eq6', 'eq7', 'eq8', 'eq9', 'RED', 'thc', 'aph',
                        'eqh', 'eql', 'dim', 'eqm', 'wup', 'sya0', 'tch0', 'sys0', 'sya1', 'tch1', 'sys1', 'tch2',
                        'sys2', 'tch3', 'BLUE', 'GRAY', 'tprc', 'rand', 'baud', 'thsp', 'ussp', 'thup', 'usup', 'addr',
                        'dims', 'bcpu', 'spax', 'spay',
                    ],
                    8: [
                        'WHITE', 'BLACK', 'GREEN', 'BROWN', 'thdra', 'appid', 'bkcmd', 'usize', 'sleep', 'bauds',
                        'delay', 'audio0', 'audio1', 'YELLOW', 'recmod', 'runmod', 'volume', 'sendxy', 'portbusy',
                    ],
                },
                'other_operators': {
                    'unary': [
                        '++', '--',
                    ],
                    'binary': [
                        '+', '-', '*', '/', '<<', '>>', '&', '|', '^', '=', '+=', '-=', '*=', '/=', '<<=', '>>=', '&=',
                        '|=', '^=',
                    ],
                    'jmp': 0x2054,
                },
            },
            3: {
                'numerated_operators': {
                    8: [
                        'click', 'comok', 'btlen', 'redir', 'print', 'ucopy', 'code_c', 'draw3d', 'qrcode', 'rdfile',
                        'refile', 'twfile', 'sendme', 'draw_h', 'printh', 'strlen', 'cfgpio', 'showqq', 'deldir',
                        'newdir', 'substr', 'prints', 'pa_txt', 'delfile', 'newfile', 'udelete', 'strsize', 'touch_j',
                        'finddir', 'randset', 'lcd_dev', 'lhmi_cle', 'whmi_cle', 'findfile', 'setbrush', 'ref_stop',
                        'com_stop', 'ref_star', 'com_star', 'setlayer', 'doevents', 'timerset', 'getpassw', 'lcd_refx',
                        'setbaudz',
                    ],
                    4: [
                        'i', 'pic', 'cle', 'ref', 'cir', 'vis', 'cls', 'get', 'cov', 'tsw', 'xpic', 'page', 'line',
                        'move', 'fill', 'repo', 'wepo', 'pa_q', 'picq', 'nstr', 'xstr', 'zstr', 'cirs', 'addt', 'init',
                        'rept', 'wept', 'rfpt', 'wfpt', 'rest', 'draw', 'covx', 'play',
                    ],
                },
                'numerated_system_variables': {
                    4: [
                        'dp', 'eq0', 'eq1', 'eq2', 'eq3', 'eq4', 'eq5', 'eq6', 'eq7', 'eq8', 'eq9', 'RED', 'thc', 'aph',
                        'eqh', 'eql', 'dim', 'eqm', 'wup', 'sya0', 'rtc0', 'tch0', 'pio0', 'sys0', 'sya1', 'rtc1',
                        'tch1', 'pio1', 'sys1', 'rtc2', 'tch2', 'pio2', 'sys2', 'rtc3', 'tch3', 'pio3', 'rtc4', 'pwm4',
                        'pio4', 'rtc5', 'pwm5', 'pio5', 'rtc6', 'pwm6', 'pio6', 'pwm7', 'pio7', 'BLUE', 'GRAY', 'tprc',
                        'rand', 'baud', 'pwmf', 'thsp', 'ussp', 'thup', 'usup', 'addr', 'dims', 'bcpu', 'spax', 'spay',
                    ],
                    8: [
                        'WHITE', 'BLACK', 'GREEN', 'BROWN', 'thdra', 'appid', 'bkcmd', 'usize', 'sleep', 'bauds',
                        'delay', 'audio0', 'audio1', 'YELLOW', 'recmod', 'runmod', 'volume', 'sendxy', 'portbusy',
                    ],
                },
                'other_operators': {
                    'unary': [
                        '++', '--',
                    ],
                    'binary': [
                        '+', '-', '*', '/', '<<', '>>', '&', '|', '^', '=', '+=', '-=', '*=', '/=', '<<=', '>>=', '&=',
                        '|=', '^=',
                    ],
                    'jmp': 0x2054,
                },
            },
        },
    },
    {
        'versions': [
            'tjc-0.58'
        ],
        'models': {
            0: {
                'numerated_system_variables': {
                    4: [
                        'dp', 'RED', 'thc', 'dim', 'wup', 'sya0', 'tch0', 'sys0', 'sya1', 'tch1', 'sys1', 'tch2',
                        'sys2', 'tch3', 'BLUE', 'GRAY', 'rand', 'baud', 'thsp', 'ussp', 'thup', 'usup', 'addr', 'dims',
                        'bcpu', 'spax', 'spay',
                    ],
                    8: [
                        'WHITE', 'BLACK', 'GREEN', 'BROWN', 'thdra', 'appid', 'bkcmd', 'usize', 'sleep', 'tpdir',
                        'bauds', 'delay', 'YELLOW', 'recmod', 'runmod', 'sendxy', 'portbusy',
                    ],
                },
                'numerated_operators': {
                    8: [
                        'click', 'comok', 'btlen', 'print', 'ucopy', 'code_c', 'draw3d', 'qrcode', 'sendme', 'draw_h',
                        'printh', 'strlen', 'showqq', 'substr', 'prints', 'pa_txt', 'udelete', 'strsize', 'touch_j',
                        'randset', 'lcd_dev', 'lhmi_cle', 'whmi_cle', 'setbrush', 'ref_stop', 'com_stop', 'ref_star',
                        'com_star', 'doevents', 'timerset', 'getpassw', 'lcd_refx', 'setbaudz',
                    ],
                    4: [
                        'i', 'pic', 'cle', 'ref', 'cir', 'vis', 'cls', 'get', 'cov', 'tsw', 'xpic', 'page', 'line',
                        'fill', 'pa_q', 'picq', 'fstr', 'nstr', 'xstr', 'zstr', 'cirs', 'addt', 'init', 'rfpt', 'wfpt',
                        'rest', 'draw', 'covx',
                    ],
                },
                'other_operators': {
                    'unary': [
                        '++', '--',
                    ],
                    'binary': [
                        '+', '-', '*', '/', '<<', '>>', '&', '|', '^', '=', '+=', '-=', '*=', '/=', '<<=', '>>=', '&=',
                        '|=', '^=',
                    ],
                    'jmp': 0x2054,
                },
            },
            1: {
                'numerated_system_variables': {
                    4: [
                        'dp', 'RED', 'thc', 'dim', 'wup', 'sya0', 'rtc0', 'tch0', 'pio0', 'sys0', 'sya1', 'rtc1',
                        'tch1', 'pio1', 'sys1', 'rtc2', 'tch2', 'pio2', 'sys2', 'rtc3', 'tch3', 'pio3', 'rtc4', 'pwm4',
                        'pio4', 'rtc5', 'pwm5', 'pio5', 'rtc6', 'pwm6', 'pio6', 'pwm7', 'pio7', 'BLUE', 'GRAY', 'rand',
                        'baud', 'pwmf', 'thsp', 'ussp', 'thup', 'usup', 'addr', 'dims', 'bcpu', 'spax', 'spay',
                    ],
                    8: [
                        'WHITE', 'BLACK', 'GREEN', 'BROWN', 'thdra', 'appid', 'bkcmd', 'usize', 'sleep', 'tpdir',
                        'bauds', 'delay', 'YELLOW', 'recmod', 'runmod', 'sendxy', 'portbusy',
                    ],
                },
                'numerated_operators': {
                    8: [
                        'click', 'comok', 'btlen', 'print', 'ucopy', 'code_c', 'draw3d', 'qrcode', 'sendme', 'draw_h',
                        'printh', 'strlen', 'cfgpio', 'showqq', 'substr', 'prints', 'pa_txt', 'udelete', 'strsize',
                        'touch_j', 'randset', 'lcd_dev', 'lhmi_cle', 'whmi_cle', 'setbrush', 'ref_stop', 'com_stop',
                        'ref_star', 'com_star', 'doevents', 'timerset', 'getpassw', 'lcd_refx', 'setbaudz',
                    ],
                    4: [
                        'i', 'pic', 'cle', 'ref', 'cir', 'vis', 'cls', 'get', 'cov', 'tsw', 'xpic', 'page', 'line',
                        'fill', 'repo', 'wepo', 'pa_q', 'picq', 'fstr', 'nstr', 'xstr', 'zstr', 'cirs', 'addt', 'init',
                        'rept', 'wept', 'rfpt', 'wfpt', 'rest', 'draw', 'covx',
                    ],
                },
                'other_operators': {
                    'unary': [
                        '++', '--',
                    ],
                    'binary': [
                        '+', '-', '*', '/', '<<', '>>', '&', '|', '^', '=', '+=', '-=', '*=', '/=', '<<=', '>>=', '&=',
                        '|=', '^=',
                    ],
                    'jmp': 0x2054,
                },
            },
            2: {
                'numerated_system_variables': {
                    4: [
                        'dp', 'eq0', 'eq1', 'eq2', 'eq3', 'eq4', 'eq5', 'eq6', 'eq7', 'eq8', 'eq9', 'RED', 'thc', 'aph',
                        'eqh', 'eql', 'dim', 'eqm', 'wup', 'sya0', 'tch0', 'sys0', 'sya1', 'tch1', 'sys1', 'tch2',
                        'sys2', 'tch3', 'BLUE', 'GRAY', 'tprc', 'rand', 'baud', 'thsp', 'ussp', 'thup', 'usup', 'addr',
                        'dims', 'bcpu', 'spax', 'spay',
                    ],
                    8: [
                        'WHITE', 'BLACK', 'GREEN', 'BROWN', 'thdra', 'appid', 'bkcmd', 'usize', 'sleep', 'tpdir',
                        'bauds', 'delay', 'audio0', 'audio1', 'YELLOW', 'recmod', 'runmod', 'volume', 'sendxy',
                        'portbusy',
                    ],
                },
                'numerated_operators': {
                    8: [
                        'click', 'comok', 'btlen', 'redir', 'print', 'ucopy', 'code_c', 'draw3d', 'qrcode', 'rdfile',
                        'refile', 'twfile', 'sendme', 'draw_h', 'printh', 'strlen', 'cfgpio', 'showqq', 'deldir',
                        'newdir', 'substr', 'prints', 'pa_txt', 'delfile', 'newfile', 'udelete', 'strsize', 'touch_j',
                        'finddir', 'randset', 'lcd_dev', 'lhmi_cle', 'whmi_cle', 'findfile', 'setbrush', 'ref_stop',
                        'com_stop', 'ref_star', 'com_star', 'setlayer', 'doevents', 'timerset', 'getpassw', 'lcd_refx',
                        'setbaudz',
                    ],
                    4: [
                        'i', 'pic', 'cle', 'ref', 'cir', 'vis', 'cls', 'get', 'cov', 'tsw', 'xpic', 'page', 'line',
                        'move', 'fill', 'repo', 'wepo', 'pa_q', 'picq', 'nstr', 'xstr', 'zstr', 'cirs', 'addt', 'init',
                        'rept', 'wept', 'rfpt', 'wfpt', 'rest', 'draw', 'covx', 'play',
                    ],
                },
                'other_operators': {
                    'unary': [
                        '++', '--',
                    ],
                    'binary': [
                        '+', '-', '*', '/', '<<', '>>', '&', '|', '^', '=', '+=', '-=', '*=', '/=', '<<=', '>>=', '&=',
                        '|=', '^=',
                    ],
                    'jmp': 0x2054,
                }
            },
            3: {
                'numerated_system_variables': {
                    4: [
                        'dp', 'eq0', 'eq1', 'eq2', 'eq3', 'eq4', 'eq5', 'eq6', 'eq7', 'eq8', 'eq9', 'RED', 'thc', 'aph',
                        'eqh', 'eql', 'dim', 'eqm', 'wup', 'sya0', 'rtc0', 'tch0', 'pio0', 'sys0', 'sya1', 'rtc1',
                        'tch1', 'pio1', 'sys1', 'rtc2', 'tch2', 'pio2', 'sys2', 'rtc3', 'tch3', 'pio3', 'rtc4', 'pwm4',
                        'pio4', 'rtc5', 'pwm5', 'pio5', 'rtc6', 'pwm6', 'pio6', 'pwm7', 'pio7', 'BLUE', 'GRAY', 'tprc',
                        'rand', 'baud', 'pwmf', 'thsp', 'ussp', 'thup', 'usup', 'addr', 'dims', 'bcpu', 'spax', 'spay',
                    ],
                    8: [
                        'WHITE', 'BLACK', 'GREEN', 'BROWN', 'thdra', 'appid', 'bkcmd', 'usize', 'sleep', 'tpdir',
                        'bauds', 'delay', 'audio0', 'audio1', 'YELLOW', 'recmod', 'runmod', 'volume', 'sendxy',
                        'portbusy',
                    ],
                },
                'numerated_operators': {
                    8: [
                        'click', 'comok', 'btlen', 'redir', 'print', 'ucopy', 'code_c', 'draw3d', 'qrcode', 'rdfile',
                        'refile', 'twfile', 'sendme', 'draw_h', 'printh', 'strlen', 'cfgpio', 'showqq', 'deldir',
                        'newdir', 'substr', 'prints', 'pa_txt', 'delfile', 'newfile', 'udelete', 'strsize', 'touch_j',
                        'finddir', 'randset', 'lcd_dev', 'lhmi_cle', 'whmi_cle', 'findfile', 'setbrush', 'ref_stop',
                        'com_stop', 'ref_star', 'com_star', 'setlayer', 'doevents', 'timerset', 'getpassw', 'lcd_refx',
                        'setbaudz'
                    ],
                    4: [
                        'i', 'pic', 'cle', 'ref', 'cir', 'vis', 'cls', 'get', 'cov', 'tsw', 'xpic', 'page', 'line',
                        'move', 'fill', 'repo', 'wepo', 'pa_q', 'picq', 'nstr', 'xstr', 'zstr', 'cirs', 'addt', 'init',
                        'rept', 'wept', 'rfpt', 'wfpt', 'rest', 'draw', 'covx', 'play'
                    ],
                },
                'other_operators': {
                    'unary': [
                        '++', '--'
                    ],
                    'binary': [
                        '+', '-', '*', '/', '<<', '>>', '&', '|', '^', '=', '+=', '-=', '*=', '/=', '<<=', '>>=', '&=',
                        '|=', '^=',
                    ],
                    'jmp': 0x2054,
                }
            },
        },
    },
    {
        'versions': [
            'nxt-1.63.1', 'nxt-1.63.2', 'nxt-1.63.3',
        ],
        'models': {
            0: {
                'numerated_operators': {
                    8: [
                        'click', 'comok', 'btlen', 'spstr', 'print', 'ucopy', 'code_c', 'draw3d', 'qrcode', 'sendme',
                        'draw_h', 'printh', 'strlen', 'showqq', 'substr', 'prints', 'pa_txt', 'udelete', 'strsize',
                        'crcputh', 'touch_j', 'crcputs', 'randset', 'crcrest', 'crcputu', 'lcd_dev', 'lhmi_cle',
                        'whmi_cle', 'setbrush', 'ref_stop', 'com_stop', 'ref_star', 'com_star', 'doevents', 'timerset',
                        'getpassw', 'lcd_refx', 'setbaudz',
                    ],
                    4: [
                        'i', 'pic', 'cle', 'ref', 'cir', 'vis', 'cls', 'get', 'cov', 'tsw', 'xpic', 'page', 'line',
                        'fill', 'pa_q', 'picq', 'fstr', 'nstr', 'xstr', 'zstr', 'cirs', 'addt', 'init', 'rfpt', 'wfpt',
                        'rest', 'draw', 'covx',
                    ],
                },
                'numerated_system_variables': {
                    4: [
                        'dp', 'RED', 'thc', 'dim', 'wup', 'sya0', 'tch0', 'sya1', 'tch1', 'tch2', 'tch3', 'BLUE',
                        'GRAY', 'rand', 'baud', 'thsp', 'ussp', 'thup', 'usup', 'addr', 'dims', 'bcpu', 'spax', 'spay',
                    ],
                    8: [
                        'WHITE', 'BLACK', 'GREEN', 'BROWN', 'thdra', 'appid', 'bkcmd', 'usize', 'sleep', 'tpdir',
                        'bauds', 'delay', 'YELLOW', 'recmod', 'runmod', 'crcval', 'sendxy', 'portbusy',
                    ],
                },
                'other_operators': {
                    'unary': [
                        '++', '--',
                    ],
                    'binary': [
                        '+', '-', '*', '/', '<<', '>>', '&', '|', '^', '=', '+=', '-=', '*=', '/=', '<<=', '>>=', '&=',
                        '|=', '^=',
                    ],
                    'jmp': 0x2054,
                },
            },
            100: {
                'numerated_operators': {
                    8: [
                        'click', 'comok', 'btlen', 'spstr', 'print', 'ucopy', 'code_c', 'draw3d', 'qrcode', 'sendme',
                        'draw_h', 'printh', 'strlen', 'showqq', 'substr', 'prints', 'pa_txt', 'udelete', 'strsize',
                        'crcputh', 'touch_j', 'crcputs', 'randset', 'crcrest', 'crcputu', 'lcd_dev', 'lhmi_cle',
                        'whmi_cle', 'setbrush', 'ref_stop', 'com_stop', 'ref_star', 'com_star', 'piccolor', 'doevents',
                        'timerset', 'getpassw', 'lcd_refx', 'setbaudz',
                    ],
                    4: [
                        'i', 'pic', 'cle', 'ref', 'cir', 'vis', 'cls', 'get', 'cov', 'tsw', 'xpic', 'page', 'line',
                        'fill', 'repo', 'wepo', 'pa_q', 'picq', 'fstr', 'nstr', 'xstr', 'zstr', 'cirs', 'addt', 'init',
                        'rfpt', 'wfpt', 'rest', 'getv', 'draw', 'covx',
                    ],
                },
                'numerated_system_variables': {
                    4: [
                        'dp', 'RED', 'thc', 'dim', 'wup', 'sya0', 'tch0', 'sya1', 'tch1', 'tch2', 'tch3', 'BLUE',
                        'GRAY', 'rand', 'baud', 'thsp', 'ussp', 'thup', 'usup', 'addr', 'dims', 'bcpu', 'spax', 'spay',
                    ],
                    8: [
                        'WHITE', 'BLACK', 'GREEN', 'BROWN', 'thdra', 'appid', 'bkcmd', 'usize', 'sleep', 'tpdir',
                        'bauds', 'delay', 'YELLOW', 'recmod', 'runmod', 'crcval', 'sendxy', 'lowpower', 'portbusy',
                    ],
                },
                'other_operators': {
                    'unary': [
                        '++', '--',
                    ],
                    'binary': [
                        '+', '-', '*', '/', '<<', '>>', '&', '|', '^', '=', '+=', '-=', '*=', '/=', '<<=', '>>=', '&=',
                        '|=', '^=',
                    ],
                    'jmp': 0x2054,
                },
            },
            1: {
                'numerated_operators': {
                    8: [
                        'click', 'comok', 'btlen', 'spstr', 'print', 'ucopy', 'code_c', 'draw3d', 'qrcode', 'sendme',
                        'draw_h', 'printh', 'strlen', 'cfgpio', 'showqq', 'substr', 'prints', 'pa_txt', 'udelete',
                        'strsize', 'crcputh', 'touch_j', 'crcputs', 'randset', 'crcrest', 'crcputu', 'lcd_dev',
                        'lhmi_cle', 'whmi_cle', 'setbrush', 'ref_stop', 'com_stop', 'ref_star', 'com_star', 'doevents',
                        'timerset', 'getpassw', 'lcd_refx', 'setbaudz',
                    ],
                    4: [
                        'i', 'pic', 'cle', 'ref', 'cir', 'vis', 'cls', 'get', 'cov', 'tsw', 'xpic', 'page', 'line',
                        'fill', 'repo', 'wepo', 'pa_q', 'picq', 'fstr', 'nstr', 'xstr', 'zstr', 'cirs', 'addt', 'init',
                        'rept', 'wept', 'rfpt', 'wfpt', 'rest', 'draw', 'covx',
                    ],
                },
                'numerated_system_variables': {
                    4: [
                        'dp', 'RED', 'thc', 'dim', 'wup', 'sya0', 'rtc0', 'tch0', 'pio0', 'sya1', 'rtc1', 'tch1',
                        'pio1', 'rtc2', 'tch2', 'pio2', 'rtc3', 'tch3', 'pio3', 'rtc4', 'pwm4', 'pio4', 'rtc5', 'pwm5',
                        'pio5', 'rtc6', 'pwm6', 'pio6', 'pwm7', 'pio7', 'BLUE', 'GRAY', 'rand', 'baud', 'pwmf', 'thsp',
                        'ussp', 'thup', 'usup', 'addr', 'dims', 'bcpu', 'spax', 'spay',
                    ],
                    8: [
                        'WHITE', 'BLACK', 'GREEN', 'BROWN', 'thdra', 'appid', 'bkcmd', 'usize', 'sleep', 'tpdir',
                        'bauds', 'delay', 'YELLOW', 'recmod', 'runmod', 'crcval', 'sendxy', 'portbusy',
                    ],
                },
                'other_operators': {
                    'unary': [
                        '++', '--',
                    ],
                    'binary': [
                        '+', '-', '*', '/', '<<', '>>', '&', '|', '^', '=', '+=', '-=', '*=', '/=', '<<=', '>>=', '&=',
                        '|=', '^=',
                    ],
                    'jmp': 0x2054,
                },
            },
            2: {
                'numerated_operators': {
                    8: [
                        'click', 'comok', 'btlen', 'redir', 'spstr', 'print', 'ucopy', 'code_c', 'draw3d', 'qrcode',
                        'rdfile', 'refile', 'twfile', 'sendme', 'draw_h', 'printh', 'strlen', 'cfgpio', 'showqq',
                        'deldir', 'newdir', 'substr', 'prints', 'pa_txt', 'delfile', 'newfile', 'udelete', 'strsize',
                        'crcputh', 'touch_j', 'finddir', 'crcputs', 'randset', 'cfguart', 'crcrest', 'crcputu',
                        'lcd_dev', 'lhmi_cle', 'whmi_cle', 'findfile', 'setbrush', 'ref_stop', 'com_stop', 'ref_star',
                        'com_star', 'setlayer', 'doevents', 'timerset', 'getpassw', 'lcd_refx', 'setbaudz',
                    ],
                    4: [
                        'i', 'pic', 'cle', 'ref', 'cir', 'vis', 'cls', 'get', 'cov', 'tsw', 'xpic', 'page', 'line',
                        'move', 'fill', 'xnum', 'repo', 'wepo', 'pa_q', 'picq', 'nstr', 'xstr', 'zstr', 'cirs', 'cuts',
                        'addt', 'init', 'rept', 'wept', 'rfpt', 'wfpt', 'rest', 'draw', 'covx', 'play',
                    ],
                },
                'numerated_system_variables': {
                    4: [
                        'dp', 'eq0', 'eq1', 'eq2', 'eq3', 'eq4', 'eq5', 'eq6', 'eq7', 'eq8', 'eq9', 'RED', 'thc', 'aph',
                        'eqh', 'eql', 'dim', 'eqm', 'wup', 'sya0', 'tch0', 'pio0', 'sya1', 'tch1', 'pio1', 'tch2',
                        'pio2', 'tch3', 'pio3', 'pwm4', 'pio4', 'pwm5', 'pio5', 'pwm6', 'pio6', 'pwm7', 'pio7', 'BLUE',
                        'GRAY', 'tprc', 'rand', 'baud', 'pwmf', 'thsp', 'ussp', 'thup', 'usup', 'addr', 'dims', 'bcpu',
                        'spax', 'spay',
                    ],
                    8: [
                        'WHITE', 'BLACK', 'GREEN', 'BROWN', 'thdra', 'appid', 'bkcmd', 'usize', 'sleep', 'tpdir',
                        'bauds', 'delay', 'audio0', 'audio1', 'YELLOW', 'recmod', 'runmod', 'scache', 'volume',
                        'crcval', 'sendxy', 'portbusy',
                    ],
                },
                'other_operators': {
                    'unary': [
                        '++', '--',
                    ],
                    'binary': [
                        '+', '-', '*', '/', '<<', '>>', '&', '|', '^', '=', '+=', '-=', '*=', '/=', '<<=', '>>=', '&=',
                        '|=', '^=',
                    ],
                    'jmp': 0x2054,
                },
            },
            3: {
                'numerated_operators': {
                    8: [
                        'click', 'comok', 'btlen', 'redir', 'spstr', 'print', 'ucopy', 'code_c', 'draw3d', 'qrcode',
                        'rdfile', 'refile', 'twfile', 'sendme', 'draw_h', 'printh', 'strlen', 'cfgpio', 'showqq',
                        'deldir', 'newdir', 'substr', 'prints', 'pa_txt', 'delfile', 'newfile', 'udelete', 'strsize',
                        'crcputh', 'touch_j', 'finddir', 'crcputs', 'randset', 'cfguart', 'crcrest', 'crcputu',
                        'lcd_dev', 'lhmi_cle', 'whmi_cle', 'findfile', 'setbrush', 'ref_stop', 'com_stop', 'ref_star',
                        'com_star', 'setlayer', 'doevents', 'timerset', 'getpassw', 'lcd_refx', 'setbaudz',
                    ],
                    4: [
                        'i', 'pic', 'cle', 'ref', 'cir', 'vis', 'cls', 'get', 'cov', 'tsw', 'xpic', 'page', 'line',
                        'move', 'fill', 'xnum', 'repo', 'wepo', 'pa_q', 'picq', 'nstr', 'xstr', 'zstr', 'cirs', 'cuts',
                        'addt', 'init', 'rept', 'wept', 'rfpt', 'wfpt', 'rest', 'draw', 'covx', 'play',
                    ],
                },
                'numerated_system_variables': {
                    4: [
                        'dp', 'eq0', 'eq1', 'eq2', 'eq3', 'eq4', 'eq5', 'eq6', 'eq7', 'eq8', 'eq9', 'RED', 'thc', 'aph',
                        'eqh', 'eql', 'dim', 'eqm', 'wup', 'sya0', 'rtc0', 'tch0', 'pio0', 'sya1', 'rtc1', 'tch1',
                        'pio1', 'rtc2', 'tch2', 'pio2', 'rtc3', 'tch3', 'pio3', 'rtc4', 'pwm4', 'pio4', 'rtc5', 'pwm5',
                        'pio5', 'rtc6', 'pwm6', 'pio6', 'pwm7', 'pio7', 'BLUE', 'GRAY', 'tprc', 'rand', 'baud', 'pwmf',
                        'thsp', 'ussp', 'thup', 'usup', 'addr', 'dims', 'bcpu', 'spax', 'spay',
                    ],
                    8: [
                        'WHITE', 'BLACK', 'GREEN', 'BROWN', 'thdra', 'appid', 'bkcmd', 'usize', 'sleep', 'tpdir',
                        'bauds', 'delay', 'audio0', 'audio1', 'YELLOW', 'recmod', 'runmod', 'scache', 'volume',
                        'crcval', 'sendxy', 'portbusy',
                    ],
                },
                'other_operators': {
                    'unary': [
                        '++', '--',
                    ],
                    'binary': [
                        '+', '-', '*', '/', '<<', '>>', '&', '|', '^', '=', '+=', '-=', '*=', '/=', '<<=', '>>=', '&=',
                        '|=', '^=',
                    ],
                    'jmp': 0x2054,
                },
            },
        },
    },
]
