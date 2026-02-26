# poly-storage-cli

Official CLI for the Entity Market Data API.

## Install

```bash
pip install poly-storage-cli
```

## Usage

```bash
export ENTITY_API_KEY="YOUR_API_KEY"

poly-storage health
poly-storage polymarket market-data \
  --condition-id 0x0008043c3ed513ecff7ee64380fc943dc73eb3dfb6674f281149efe4769f7515 \
  --date 2026-02-13
```
