"""Store category table."""


import os
import pandas as pd
import numpy as np
from typing import Iterator, List
from afimall.sql_utils import df_to_sql


def build_cat_tree(parent_id: int, it: Iterator, x: int,
                   max_depth: int = 4, split_chance: float = 0.5,
                   depth: int = 1) -> None:
    """Builds a tree of categories recursively."""
    if depth == max_depth:
        return x
    if np.random.random() < split_chance:
        left = next(it, 0)
        if left:
            parent_id[left - 1] = x
            build_cat_tree(parent_id, it, left, max_depth=max_depth,
                           split_chance=split_chance, depth=depth + 1)
        right = next(it, 0)
        if right:
            parent_id[right - 1] = x
            build_cat_tree(parent_id, it, right, max_depth=max_depth,
                           split_chance=split_chance, depth=depth + 1)


def create_parent_id(store_category_size, max_depth=4,
                     split_chance=0.5) -> List[int]:
    """Create parent_id for store_category table"""
    parent_id = [0 for i in range(store_category_size)]
    it = range(1, store_category_size + 1).__iter__()
    x = next(it, 0)
    while x:
        parent_id[x - 1] = 0
        build_cat_tree(parent_id, it, x, max_depth=max_depth,
                       split_chance=split_chance)
        x = next(it, 0)
    return parent_id


def create_script(sql_scripts_path: str, samples_path: str,
                  store_category_size: int, parent_id: List[int]) -> None:
    """Create SQL script to fill store_category table"""
    cat_names = pd.read_csv(os.path.join(samples_path, 'catch_phrase.csv'))
    cat_names = cat_names['"name"']
    cat_names = cat_names.drop_duplicates()
    cat_names = cat_names.apply(lambda x: f'\'{x}\'')
    store_category = pd.DataFrame(data={
        'category_id': np.arange(store_category_size) + 1,
        '"name"': cat_names.values[:store_category_size]
    })

    store_category['parent_id'] = parent_id
    store_category['parent_id'] = store_category['parent_id'].apply(
        lambda x: x if x else 'null')

    fpath = os.path.join(sql_scripts_path, 'fill_store_category.sql')
    with open(fpath, 'w') as f:
        df_to_sql(store_category, 'store_category', f)
