name: Post Daily Countdown Tweet

on:
  schedule:
    - cron: '03 19 * * *' # 12:33 AM IST daily (19:03 UTC)
  workflow_dispatch:

jobs:
  tweet:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Tweepy
        run: |
          python -m pip install --upgrade pip
          pip install tweepy

      - name: Run script
        env:
          API_KEY: ${{ secrets.API_KEY }}
          API_SECRET: ${{ secrets.API_SECRET }}
          ACCESS_TOKEN: ${{ secrets.ACCESS_TOKEN }}
          ACCESS_SECRET: ${{ secrets.ACCESS_SECRET }}
        run: python your_script_name.py
