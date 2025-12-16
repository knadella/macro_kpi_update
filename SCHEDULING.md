# Scheduling the Inflation Pipeline

The inflation pipeline is scheduled to run automatically using GitHub Actions.

## Current Setup

The pipeline runs **every Monday at 9:00 AM UTC** via GitHub Actions workflow (`.github/workflows/weekly_pipeline.yml`).

## Manual Trigger

You can manually trigger the pipeline from GitHub:

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. Select **Weekly Inflation Pipeline**
4. Click **Run workflow** → **Run workflow**

## Customizing the Schedule

To change the schedule, edit the `cron` line in `.github/workflows/weekly_pipeline.yml`:

```yaml
schedule:
  - cron: '0 9 * * 1'  # Monday 9 AM UTC
```

**Cron format:** `minute hour day month weekday`

Examples:
- `'0 9 * * 1'` - Every Monday at 9 AM UTC
- `'0 2 * * 0'` - Every Sunday at 2 AM UTC
- `'0 14 * * 1'` - Every Monday at 2 PM UTC (9 AM EST)

**Note:** GitHub Actions uses UTC time. Adjust accordingly for your timezone.

## Viewing Results

1. **Check Actions tab:**
   - Go to repository → Actions
   - Click on the latest workflow run
   - View logs and summary

2. **Download artifacts:**
   - In the workflow run page, scroll to "Artifacts"
   - Download `inflation-data-{run_number}` for CSV files
   - Download `pipeline-logs-{run_number}` for logs

## Alternative: Local Scheduling

If you prefer to run the pipeline locally instead of using GitHub Actions, you can use:

- **Cron (macOS/Linux):** `crontab -e` and add a schedule
- **Launchd (macOS):** Create a plist file in `~/Library/LaunchAgents/`

For local scheduling, you would run:
```bash
python3 pipelines/inflation_pipeline.py --source statcan
```
