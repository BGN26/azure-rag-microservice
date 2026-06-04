import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_mock_erp_data(days=30, num_records=500):

    np.random.seed(42)  #

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    random_dates = [
        start_date + timedelta(seconds=int(x))
        for x in np.random.randint(
            0, int((end_date - start_date).total_seconds()), num_records
        )
    ]

    data = {
        "timestamp": sorted(random_dates),
        "user_id": np.random.choice(
            ["USR-001", "USR-002", "USR-003", "USR-004", "USR-005"], num_records
        ),
        "department": np.random.choice(
            ["HR", "Legal", "Engineering", "Sales"], num_records, p=[0.2, 0.4, 0.3, 0.1]
        ),
        "document_type": np.random.choice(
            ["Contract", "Invoice", "Technical_Manual", "Policy"], num_records
        ),
        "processing_time_sec": np.round(
            np.random.normal(loc=15.0, scale=5.0, size=num_records), 2
        ),
        "tokens_consumed": np.random.randint(500, 8000, num_records),
        "status": np.random.choice(
            ["success", "success", "success", "error"], num_records
        ),
    }

    df = pd.DataFrame(data)

    df.loc[df["processing_time_sec"] < 0, "processing_time_sec"] = 1.0

    return df


if __name__ == "__main__":
    df_mock = generate_mock_erp_data()
    print("Muestra de datos del ERP (Simulada):")
    print(df_mock.head())
