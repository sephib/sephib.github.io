# basic dataclass
import numpy as np
from dataclasses import dataclass


@dataclass
class Split:
    X: np.ndarray = None
    y: np.array = None
    idx: np.array = None
    pred_class: np.array = None
    pred_proba: np.ndarray = None
    kwargs: Dict = None

    def __init__(self, name: str):
        self.name = name


def get_split_from_idx(X, y, split1: Split, split2: Split):
    split1.X, split2.X = X.iloc[split1.idx], X.iloc[split2.idx]
    split1.y, split2.y = y.iloc[split1.idx], y.iloc[split2.idx]
    return split1, split2


for fold_name, (train.idx, test.idx) in enumerate(
    StratifiedSplitValid(X, y, n_split=5, train_size=0.8)
):
    train, test = get_split_from_idx(X, y, train, test)  # a helper function


catboost_clf = CatBoostClassifier()

train_vlaid = Split(name="train_vlaid")
vlaid = Split(name="vlaid")
for fold_name, (train_vlaid.idx, vlaid.idx) in enumerate(
    StratifiedSplitValid(_train_X, train.y, n_split=10, train_size=0.9)
):
    train_vlaid, vlaid = get_split_from_idx(_train_X, train.y, train_vlaid, vlaid)

    pipe.steps.append(("catboost_clf", catboost_clf))

    pipe.fit(
        train_size.X,
        train_vlaid.y,
        catboost_clf__eval_set=[(valid.X, valid.y)],
    )
