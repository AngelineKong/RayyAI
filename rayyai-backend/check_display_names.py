"""Quick script to check display_name values in database"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from database import SessionLocal
from models import Statement

def check_display_names():
    db = SessionLocal()
    try:
        statements = db.query(Statement).filter(
            Statement.is_deleted == False,
            Statement.statement_type.in_(['bank', 'credit_card', 'ewallet'])
        ).order_by(Statement.statement_id.desc()).limit(5).all()

        print(f"\n{'='*100}")
        print(f"{'ID':<5} | {'Display Name':<40} | {'Period Start':<12} | {'Period End':<12}")
        print(f"{'='*100}")

        for stmt in statements:
            display_name = stmt.display_name or 'NULL'
            period_start = str(stmt.period_start) if stmt.period_start else 'NULL'
            period_end = str(stmt.period_end) if stmt.period_end else 'NULL'
            print(f"{stmt.statement_id:<5} | {display_name:<40} | {period_start:<12} | {period_end:<12}")

        print(f"{'='*100}\n")

    finally:
        db.close()

if __name__ == "__main__":
    check_display_names()
