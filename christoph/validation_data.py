import pandas


def get_train():
    df = pandas.read_csv('./train_plag_data.txt', sep=r'\t', header=None, index_col=None, skipinitialspace=True,
                         names=['duplicate', 'text1', 'text2'], engine='python')

    return df.to_dict('records')


def get_test():
    df = pandas.read_csv('./dev_plag_data.txt', sep=r'\t', header=None, index_col=None, skipinitialspace=True,
                         names=['duplicate', 'text1', 'text2'], engine='python')

    return df.to_dict('records')
