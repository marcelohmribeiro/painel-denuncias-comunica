import pandas as pd
from modules.db import get_db


def load_flat_df(collection: str) -> pd.DataFrame:
    
    db = get_db()
    q = db.collection(collection).select([
        "category",
        "location",
        "createdAt",
        "updatedAt"
    ])

    rows = [{"id": d.id, **(d.to_dict() or {})} for d in q.stream()]

    return pd.DataFrame() if (not rows) else pd.DataFrame(pd.json_normalize(rows, sep="."))