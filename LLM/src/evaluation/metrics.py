from typing import List, Dict
from sklearn.metrics import classification_report

def report(y_true: List[int], y_pred: List[int], target_names=None) -> str:
    return classification_report(y_true, y_pred, target_names=target_names, digits=4)
