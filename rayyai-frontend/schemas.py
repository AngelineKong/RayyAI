from pydantic import BaseModel, EmailStr, Field, field_validator, field_serializer, model_validator
from datetime import date
from typing import Optional

# Budget categories matching common personal finance categories
BUDGET_CATEGORIES = [
    "Housing",
    "Food", 
    "Transportation",
    "Entertainment",
    "Utilities",
    "Shopping",
    "Health & Fitness",
    "Travel",
    "Education",
    "Others"
]
BUDGET_CATEGORY_ALIASES = {
    **{category.lower(): category for category in BUDGET_CATEGORIES},
    "groceries": "Food",
}


def _normalize_budget_category(value: Optional[str]) -> Optional[str]:
    if value is None:
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in BUDGET_CATEGORY_ALIASES:
            return BUDGET_CATEGORY_ALIASES[normalized]
    raise ValueError(f'Category must be one of: {", ".join(BUDGET_CATEGORIES)}')

# Budget periods
BUDGET_PERIODS = ["weekly", "monthly", "quarterly", "yearly"]

GOAL_CATEGORIES = [
    "Emergency Fund",
    "Vacation", 
    "Car Purchase",
    "Home Down Payment",
    "Education",
    "Retirement",
    "Investment",
    "Savings",
    "Other"
]

GOAL_PRIORITIES = [
    "High",
    "Medium",
    "Low"
]

class BudgetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    limit_amount: float = Field(..., gt=0)
    category: str = Field(..., description="Budget category from predefined list")
    period_start: date
    period_end: date
    alert_threshold: float = Field(..., ge=0, le=100)
    
    _category_aliases = {category.lower(): category for category in BUDGET_CATEGORIES}
    _category_aliases.update({
        "groceries": "Food",
    })

    @classmethod
    def _normalize_category(cls, value: Optional[str]) -> str:
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in cls._category_aliases:
                return cls._category_aliases[normalized]
        raise ValueError(f'Category must be one of: {", ".join(BUDGET_CATEGORIES)}')

    @field_validator('category', mode='before')
    @classmethod
    def validate_category(cls, value):
        return cls._normalize_category(value)


class BudgetCreate(BudgetBase):
    pass

class BudgetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    limit_amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, description="Budget category from predefined list")
    period_start: Optional[date]
    period_end: Optional[date]
    alert_threshold: Optional[float] = Field(None, ge=0, le=100)

    @field_validator('category', mode='before')
    @classmethod
    def validate_category(cls, value):
        return _normalize_budget_category(value)
