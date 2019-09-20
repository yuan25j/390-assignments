"""
Util functions
"""
import pandas as pd
import numpy as np
import os
import git

def assign_log(df, col_name):
    """defining log as log(x + EPSILON) to avoid division by zero"""
    # This is to avoid division by zero while doing np.log10
    # EPSILON = 1e-4
    EPSILON = 1
    return np.log10(df[col_name].values + EPSILON)


def assign_percentile(df, col_name):
    """assign percentile to df[col_name]"""
    return pd.qcut(df[col_name].rank(method='first'), 100, labels=range(1, 101))


def get_git_dir():
    repo = git.Repo('.', search_parent_directories=True)
    return repo.working_tree_dir


def create_dir(*args):
    fullpath = os.path.join(*args)
    if not os.path.exists(fullpath):
        os.makedirs(fullpath)
    return fullpath
