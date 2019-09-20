import re
import sys
import os

header = """\"""
#                     *Colour-printing Reference*
#########################################################################################
#   @'fore': # 前景色         @'back':# 背景              @'mode':# 显示模式               # 
#            'black': 黑色            'black':  黑色              'normal': 终端默认设置   # 
#            'red': 红色              'red':  红色                'bold':  高亮显示        # 
#            'green': 绿色            'green': 绿色               'underline':  使用下划线 #
#            'yellow': 黄色           'yellow': 黄色              'blink': 闪烁           # 
#            'blue':  蓝色            'blue':  蓝色               'invert': 反白显示       #    
#            'purple':  紫红色        'purple':  紫红色            'hide': 不可见          #    
#            'cyan':  青蓝色          'cyan':  青蓝色                                     #
#            'white':  白色           'white':  白色                                     #
#########################################################################################
\"""
"""


def level_template(level_name, term):
    res = ""
    res += "%s = {" % level_name
    for t in term:
        temp = """
    "%s": {
        "DEFAULT": %s,  # 默认值
        "fore": Fore.CYAN,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },
""" % (t, t + "_default")
        res += temp
    res += "}\n\n"
    return res


def new_pyfile_template(level_list, term, template):
    res = header
    # lib
    res += f"""from datetime import datetime
from colour_printing import Mode, Fore, Back\n
get_time = lambda: datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')[:-3]\n

TEMPLATE = "{template}"

"""
    # default
    for t in term:
        res += '''%s_default = ""\n\n''' % t
    # style
    for l in level_list:
        res += level_template(l, term)
    return res


def create_py_file(file_path, level_list, term, template):
    try:
        with open(file_path, 'w')as f:
            f.write(new_pyfile_template(level_list, term, template))
    except Exception as e:
        print(e)
        return 2
    else:
        print(f'[*]Tip>> 创建配置模板文件完成-->  {file_path}')
        return 0


def execute(argv=None):
    if argv is None:
        argv = sys.argv
    template = str(argv[1])
    if len(argv) == 2:
        file_path = f'{os.getcwd()}/colour_printing_config.py'
    else:
        name = str(argv[2])
        name = name if name.endswith('.py') else name + '.py'
        file_path = f'{os.getcwd()}/{name}'
    term = re.findall(r'(?<=\{)[^}]*(?=\})+', template)
    for t in term:
        if t.strip() == '':
            print('\n [*]Tip>> Template have {} ! ')
            sys.exit(2)
    if "message" not in term:
        print('\n [*]Tip>> template muse have {message} ! ')
        sys.exit(2)
    level_list = ['INFO', 'SUCCESS', 'WARNING', 'ERROR', 'DEBUG']
    print('[*]Tip>> 创建配置模板文件中....')
    code = create_py_file(file_path, level_list, term, template)
    sys.exit(code)
