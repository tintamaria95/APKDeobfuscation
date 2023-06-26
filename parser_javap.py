def parse_javap(txt: str):
    methods_instructions = []
    # get class name
    class_name = txt.split('\n')[0].split('/')[-1].split('.')[0]
    # print(class_name)
    # get instructions
    txt = txt.split('{\n')[1]
    txt = txt.split('\n}')[0]

    # split attributes and methods
    instances = txt.split('\n\n')
    for inst in instances:
        lines = inst.split('\n')
        method_name = ''
        method_name_parts = lines[0].split()
        for part in method_name_parts:
            if '(' in part:
                method_name = part.split('(')[0]
                break
        if method_name == '':
            continue
        is_composed_name = '.' in method_name
        if is_composed_name:
            if method_name.split('(')[0].split('.')[-1] == class_name:
                # Constructor
                continue
        if method_name.split('(')[0] == class_name:
            # Constructor
            continue
        if lines[0].find(');') != -1:
            instructions = lines[5:]
            instr_formatted = []
            for inst in instructions:
                if ':' in inst:
                    if inst.split(':')[0].strip().isnumeric():
                        inst_list = inst.strip().split()
                        is_has_ref = len(inst_list) == 6
                        if is_has_ref:
                            instr_formatted.append(
                                (inst_list[1], inst_list[5]))
                        else:
                            instr_formatted.append((inst_list[1], ''))

            is_instructions_list_empty = len(instr_formatted) == 0
            if not is_instructions_list_empty:
                methods_instructions.append((method_name, instr_formatted))
    return methods_instructions


if __name__ == "__main__":
    f = open('../javap_test.txt', 'r')
    txt = f.read()
    methods_instructions = parse_javap(txt=txt)
    print(methods_instructions)
