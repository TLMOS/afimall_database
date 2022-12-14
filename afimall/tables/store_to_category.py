"""Store to category m2m table."""


import os
import pandas as pd
import numpy as np
from typing import List
from afimall.sql_utils import df_to_sql


def create_script(sql_scripts_path: str, store_size: int,
                  store_category_size: int, parent_id: List[int],
                  max_cat: int = 4) -> None:
    """Create SQL script to fill store_to_category table"""
    store_id = []
    category_id = []
    for sid in range(1, store_size + 1):
        n_cat = np.random.randint(1, max_cat + 1)
        store_category_id = np.arange(store_category_size) + 1
        possible_cats = np.random.choice(store_category_id, n_cat)
        cats = []
        for cat in possible_cats:
            parents = set()
            p = parent_id[cat - 1]
            while p:
                parents.add(p)
                p = parent_id[p - 1]
            if not parents.intersection(possible_cats):
                cats.append(cat)
        for cat in cats:
            store_id.append(sid)
            category_id.append(cat)

    store_to_category = pd.DataFrame(data={
        'relation_id': np.arange(len(store_id)) + 1,
        'store_id': store_id,
        'category_id': category_id
    })

    fpath = os.path.join(sql_scripts_path, 'fill_store_to_category.sql')
    with open(fpath, 'w') as f:
        df_to_sql(store_to_category, 'store_to_category', f)
