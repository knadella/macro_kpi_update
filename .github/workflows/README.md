# GitHub Actions Workflows

## Weekly Inflation Pipeline

The `weekly_pipeline.yml` workflow automatically runs the inflation data pipeline every Monday at 9:00 AM UTC.

### Features

- **Automatic scheduling:** Runs weekly on Mondays
- **Manual trigger:** Can be triggered manually from the Actions tab
- **Artifact storage:** Saves CSV outputs and logs for 90 days
- **Summary reports:** Shows run status in GitHub Actions UI

### How to Use

1. **Push the workflow file to GitHub:**
   ```bash
   git add .github/workflows/weekly_pipeline.yml
   git commit -m "Add GitHub Actions workflow for weekly pipeline"
   git push
   ```

2. **Enable Actions (if not already enabled):**
   - Go to your repository on GitHub
   - Click "Actions" tab
   - If prompted, click "I understand my workflows, go ahead and enable them"

3. **Manual trigger (optional):**
   - Go to Actions tab
   - Select "Weekly Inflation Pipeline"
   - Click "Run workflow" button

### Schedule Customization

To change the schedule, edit the `cron` line in `weekly_pipeline.yml`:

```yaml
schedule:
  - cron: '0 9 * * 1'  # Monday 9 AM UTC
```

**Cron format:** `minute hour day month weekday`

Examples:
- `'0 9 * * 1'` - Every Monday at 9 AM UTC
- `'0 2 * * 0'` - Every Sunday at 2 AM UTC
- `'0 14 * * 1'` - Every Monday at 2 PM UTC (9 AM EST)

### Viewing Results

1. **Check Actions tab:**
   - Go to repository → Actions
   - Click on the latest workflow run
   - View logs and summary

2. **Download artifacts:**
   - In the workflow run page, scroll to "Artifacts"
   - Download `inflation-data-{run_number}` for CSV files
   - Download `pipeline-logs-{run_number}` for logs

### Timezone Notes

- GitHub Actions uses UTC time
- 9 AM UTC = 4 AM EST / 1 AM PST
- Adjust the cron schedule to match your preferred timezone

