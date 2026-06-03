import pandas as pd
from app.services.erp_simulator import generate_mock_erp_data


class AnalyticsEngine:
    def __init__(self):

        self.df = generate_mock_erp_data(days=30, num_records=500)

    def get_kpis(self):

        total_documents = len(self.df)


        success_rate = (len(self.df[self.df['status'] == 'success']) / total_documents) * 100
        total_tokens = int(self.df['tokens_consumed'].sum())

        estimated_cost_eur = round((total_tokens / 1000) * 0.002, 4)


        avg_time_dept = self.df.groupby('department')['processing_time_sec'].mean().round(2).to_dict()


        tokens_by_doc = self.df.groupby('document_type')['tokens_consumed'].sum().to_dict()

        return {
            "overview": {
                "total_documents_processed": total_documents,
                "success_rate_percentage": round(success_rate, 2),
                "total_tokens_consumed": total_tokens,
                "estimated_ai_cost_eur": estimated_cost_eur
            },
            "performance": {
                "avg_processing_time_per_department_sec": avg_time_dept,
                "token_usage_by_document_type": tokens_by_doc
            }
        }