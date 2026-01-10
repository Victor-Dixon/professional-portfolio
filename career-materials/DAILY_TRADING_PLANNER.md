# Daily Trading Planner (SSOT)

Use this template as the single source of truth for daily planning, execution, and review.

---

## Daily Planner Template

### Header
- **date:** `YYYY-MM-DD`
- **ticker:** `TSLA`
- **account**
  - starting_equity:
  - buying_power:
- **market_context**
  - trend_bias: `bull | bear | chop`
  - key_levels:
    - premarket_high:
    - premarket_low:
    - yesterday_high:
    - yesterday_low:
    - vwap_zone:
  - news_events: []

### Risk Plan
- **R_value_dollars:**
- **max_daily_loss_R:** `2`
- **max_trades_closed:** `3` (hard cap; prevents 6-sell days)
- **max_actions_total:** `8` (hard cap; prevents 16-action days)
- **allowed_setups_only:**
  - Setup_A:
  - Setup_B:
  - Setup_C:
- **no_trade_conditions:**
  - First 5-min candle is giant + whippy
  - Spread too wide / fills trash
  - Emotional state != calm

### Trade Plan
- **primary_play**
  - direction: `long | short`
  - trigger:
  - entry_zone:
  - stop:
  - take_profit_1:
  - take_profit_2:
  - management_rule: Trim at TP1, move stop to BE after X
- **alt_play**
  - direction: `long | short`
  - trigger:
  - entry_zone:
  - stop:
  - take_profit_1:

### Execution Log (Fast)
_Fill live; 1 line per ACTION (buy/sell/add/trim/stop)._

- time: `HH:MM`
  - action: `buy | sell | add | trim | stop`
  - size:
  - price:
  - reason:
  - emotion_0_10:

### End of Day Review
- **results**
  - closed_trades_count:
  - wins:
  - losses:
  - pnl_pct_total:
  - biggest_win_pct:
  - biggest_loss_pct:
- **behavior**
  - followed_rules: `yes | no`
  - broke_rules: []
  - overtraded: `yes | no`
  - revenge_or_fomo: `yes | no`
- **lessons**
  - what_worked:
  - what_failed:
  - one_fix_tomorrow:
- **scorecards**
  - discipline_0_10:
  - execution_0_10:
  - patience_0_10:
  - overall_grade: `A|B|C|D|F`

---

## Non-Negotiables
- If you hit **-2R** (or your equivalent), you are done for the day.
- If actions hit **8** OR closed trades hit **3**, you are done. Journal + walk.
- No new position when **emotion_0_10 >= 7**.
