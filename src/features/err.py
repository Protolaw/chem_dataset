from random import randint, choice

def charge_err(smiles):
    try:
        x = randint(0, 1)
        p_list, n_list = [], []
        if '+' in smiles and x == 0:
            for j in range(len(smiles)):
                if smiles[j] == '+':
                    p_list.append(j)
            i = choice(p_list)
            return (smiles[0:i] + '-' + smiles[i + 1:])

        if '-' in smiles:
            for j in range(len(smiles)):
                if smiles[j] == '-':
                    n_list.append(j)
            i = choice(n_list)
            return (smiles[0:i] + '+' + smiles[i + 1:])
    except:
        return smiles


def brace_err(smiles):
    try:
        x = randint(0, 3)

        op_list, cl_list = [], []
        ln = len(smiles)

        if '(' in smiles and x == 0:
            for j in range(ln):
                if smiles[j] == '(':
                    op_list.append(j)
            i = choice(op_list)
            return (smiles[0:i] + '' + smiles[i + 1:])

        if ')' in smiles and x == 1:
            for j in range(ln):
                if smiles[j] == ')':
                    cl_list.append(j)
            i = choice(cl_list)
            return (smiles[0:i] + '' + smiles[i + 1:])

        i = randint(0, ln)
        if x == 2:
            return (smiles[0:i] + ')' + smiles[i + 1:])
        else:
            return (smiles[0:i] + ')' + smiles[i + 1:])
    except:
        return smiles


def lc_err(smiles):
    try:
        if smiles.isupper() == False:
            lc = ['c', 'o', 's', 'n', 'p']
            g_list = []
            for i in range(len(lc)):
                if lc[i] in smiles:
                    for j in range(len(smiles)):
                        if smiles[j] == lc[i]:
                            g_list.append(j)

            i = choice(g_list)
            return (smiles[0:i] + smiles[i].upper() + smiles[i + 1:])
    except:
        return smiles

def cycle_err(smiles):
    try:
        if any(c.isdigit() for c in smiles):
            nbr_list = []
            for j in range(len(smiles)):
                if smiles[j].isdigit():
                    nbr_list.append(j)
            i = choice(nbr_list)
            return (smiles[0:i] + '' + smiles[i + 1:])
    except:
        return smiles