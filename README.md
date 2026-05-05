# entityml-cli

Official CLI for the EntityML Market Data API.

## Install

```bash
pip install entityml-cli
```

## Usage

```bash
export ENTITY_API_KEY="YOUR_API_KEY"

entityml health
entityml lookup-slug --slug will-bitcoin-hit-100k

entityml polymarket market-data \
  --condition-id 0x0008043c3ed513ecff7ee64380fc943dc73eb3dfb6674f281149efe4769f7515 \
  --date 2026-02-13

entityml polymarket orderbook-summary \
  --condition-id 0x0008043c3ed513ecff7ee64380fc943dc73eb3dfb6674f281149efe4769f7515 \
  --asset-id 97684905927345553455494278582909124912046930226695064344571162061840768197777 \
  --start-timestamp 1770940800000 \
  --end-timestamp 1770944399999 \
  --resolution 60

entityml kalshi market-data \
  --ticker KXBTC-26FEB2606-B60125 \
  --date 2026-02-26
```

## Command groups

- `health` and `monitoring-status`
- `lookup-slug`
- `polymarket list-markets`, `date-range`, `market-data`, `market-data-range`, and `orderbook-summary`
- `kalshi list-markets`, `date-range`, `market-data`, `market-data-range`, and `orderbook-summary`
- `api-keys create`, `list`, `delete`, `last-used`, and `name`
- `billing checkout`, `portal`, `subscription-status`, and `usage`
- `analytics user-request-count`, `user-request-count-timeframe`, `user-recent-requests`, `system-stats`, and `popular-markets`
