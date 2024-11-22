name: Run event-watcher.py

on:
  schedule:
    - cron: '0 16 */14 * *'  # Runs every 14 days at 16:00 UTC - 19:00 EEST
  workflow_dispatch:       # Allows manual triggering

jobs:
  run-script:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests python-dotenv

      - name: Run Script
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: |
          python event-watcher.py
