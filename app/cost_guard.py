import time
from fastapi import HTTPException
from .config import settings

# ─────────────────────────────────────────────────────────
# Cost Management Module
# ─────────────────────────────────────────────────────────

_daily_cost = 0.0
_cost_reset_day = time.strftime("%Y-%m-%d")

def check_and_record_cost(input_tokens: int, output_tokens: int):
    """
    Prevents overspending by tracking daily token usage.
    Throws a 503 error if the budget is reached.
    """
    global _daily_cost, _cost_reset_day
    
    today = time.strftime("%Y-%m-%d")
    if today != _cost_reset_day:
        _daily_cost = 0.0
        _cost_reset_day = today
        
    if _daily_cost >= settings.daily_budget_usd:
        raise HTTPException(status_code=503, detail="Daily budget exhausted. Try tomorrow.")
    
    # Mock cost calculation
    # Input tokens: ~$0.00015 / 1k tokens
    # Output tokens: ~$0.0006 / 1k tokens
    cost = (input_tokens / 1000) * 0.00015 + (output_tokens / 1000) * 0.0006
    _daily_cost += cost

def get_current_cost():
    """Returns the current accumulated daily cost."""
    return _daily_cost
