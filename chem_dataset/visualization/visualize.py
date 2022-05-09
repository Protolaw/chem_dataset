import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os


def plot(df, path_graphs, buff):
    fig, axes = plt.subplots(figsize=(20, 9))
    sns.set_theme(style="whitegrid")
    res = sns.barplot(x=buff, y='molecules', data=df, ax=axes)
    res.set_xlabel(buff, fontsize=20)
    res.set_ylabel("molecules (%)", fontsize=20)
    for tick in axes.xaxis.get_major_ticks():
        tick.label.set_fontsize(16)
    for tick in axes.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)
    inp = input('[show], [edit], [save] the plot or [exit]\n\t')
    if inp == 'show':
        plt.show()
        plot(df, path_graphs, buff)
    if inp == 'edit':
        max, min = input("Enter two values (max and min): ").split()
        df = df[df[buff] < int(max)]
        df = df[df[buff] > int(min)]
        plot(df, path_graphs, buff)
    if inp == 'save':
        plt.savefig(os.path.join(path_graphs, buff + '.png'))
    elif inp == 'exit':
        exit()
    return res

def df_create(path_to_stat, buff):
    data = pd.read_csv(path_to_stat)
    df = pd.DataFrame(data)
    df = df.sort_values(by=buff, ignore_index=True)
    s = sum(df['molecules'])
    df_proc = df.copy()
    df_proc['molecules'] = df_proc['molecules'] / s * 100
    return df_proc

def vis():
    head_list = ['rot_bonds', 'h_acc', 'h_don', 'heavy_atoms', 'ring_count', 'bonds_count', 'mol_mass']
    # main_dir = os.path.join(os.getcwd(), '../../')
    # os.chdir(main_dir)
    # main_dir = os.getcwd()

    main_dir = os.getcwd()
    path = main_dir

    try:
        isExist = os.path.exists(path + '/reports/figures/graphs')
        if not isExist:
            os.mkdir(path + '/reports/figures/graphs')
        print('ok')
    except OSError as error: 
        print(error)

    stat_file = str()
    while stat_file not in head_list:
        stat_file = input("Choose stat_file from list or 'exit'\n" + str(head_list) + '\n\t')
        if stat_file == 'exit':
            exit()
    buff = stat_file
    stat_file = stat_file + '.csv'
    path_to_stat = os.path.join(main_dir, "reports/figures/table", stat_file)
    path_graphs = os.path.join(main_dir, "reports/figures/graphs")
    df_proc = df_create(path_to_stat, buff)
    chart = plot(df_proc, path_graphs, buff)

