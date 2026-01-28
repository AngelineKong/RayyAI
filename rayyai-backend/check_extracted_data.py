"""Quick script to check extracted_data account_info"""
import sys
from pathlib import Path
import json

sys.path.append(str(Path(__file__).parent))

from database import SessionLocal
from models import Statement

def check_extracted_data():
    db = SessionLocal()
    try:
        statements = db.query(Statement).filter(
            Statement.is_deleted == False,
            Statement.statement_type.in_(['bank', 'credit_card', 'ewallet']),
            Statement.extracted_data.isnot(None)
        ).order_by(Statement.statement_id.desc()).limit(3).all()

        for stmt in statements:
            print(f"\n{'='*100}")
            print(f"Statement ID: {stmt.statement_id}")
            print(f"Display Name: {stmt.display_name}")
            print(f"Statement Type: {stmt.statement_type}")

            if stmt.extracted_data:
                if isinstance(stmt.extracted_data, str):
                    extracted = json.loads(stmt.extracted_data)
                else:
                    extracted = stmt.extracted_data

                account_info = extracted.get('account_info')
                print(f"\nAccount Info: {json.dumps(account_info, indent=2)}")
            else:
                print("\nNo extracted_data")

            print(f"{'='*100}")

    finally:
        db.close()

if __name__ == "__main__":
    check_extracted_data()
