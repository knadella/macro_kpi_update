# Scheduling the Inflation Pipeline

This document explains how to schedule the inflation pipeline to run automatically.

## Option 1: Cron (macOS/Linux) - Recommended

### Setup Steps

1. **Open your crontab for editing:**
   ```bash
   crontab -e
   ```

2. **Add a weekly schedule (runs every Monday at 9:00 AM):**
   ```
   0 9 * * 1 /Users/karthiknadella/macro_kpi_update/run_pipeline.sh
   ```

   Or run every Sunday at 2:00 AM:
   ```
   0 2 * * 0 /Users/karthiknadella/macro_kpi_update/run_pipeline.sh
   ```

### Cron Schedule Format

```
* * * * *
│ │ │ │ │
│ │ │ │ └─── Day of week (0-7, where 0 and 7 = Sunday)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

### Common Schedule Examples

- **Every Monday at 9 AM:** `0 9 * * 1`
- **Every Sunday at 2 AM:** `0 2 * * 0`
- **Every day at 8 AM:** `0 8 * * *`
- **First day of every month at 6 AM:** `0 6 1 * *`

### Verify Cron Job

1. **List your cron jobs:**
   ```bash
   crontab -l
   ```

2. **Check cron logs (macOS):**
   ```bash
   grep CRON /var/log/system.log
   ```

3. **Test the script manually:**
   ```bash
   ./run_pipeline.sh
   ```

## Option 2: GitHub Actions (Cloud-based)

If you prefer cloud-based scheduling, you can use GitHub Actions.

### Setup Steps

1. **Create `.github/workflows/weekly_pipeline.yml`:**
   ```yaml
   name: Weekly Inflation Pipeline
   
   on:
     schedule:
       # Runs every Monday at 9:00 AM UTC
       - cron: '0 9 * * 1'
     workflow_dispatch: # Allows manual trigger
   
   jobs:
     run-pipeline:
       runs-on: ubuntu-latest
       
       steps:
       - uses: actions/checkout@v3
       
       - name: Set up Python
         uses: actions/setup-python@v4
         with:
           python-version: '3.9'
       
       - name: Install dependencies
         run: |
           pip install -r requirements.txt
       
       - name: Run pipeline
         run: |
           python3 pipelines/inflation_pipeline.py --source statcan
       
       - name: Upload output
         uses: actions/upload-artifact@v3
         with:
           name: inflation-data
           path: data_outputs/
           retention-days: 90
   ```

2. **Commit and push to GitHub:**
   ```bash
   git add .github/workflows/weekly_pipeline.yml
   git commit -m "Add weekly pipeline workflow"
   git push
   ```

## Option 3: Launchd (macOS native)

macOS also supports `launchd` for scheduling.

### Setup Steps

1. **Create `~/Library/LaunchAgents/com.macro_kpi.pipeline.plist`:**
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.macro_kpi.pipeline</string>
       <key>ProgramArguments</key>
       <array>
           <string>/Users/karthiknadella/macro_kpi_update/run_pipeline.sh</string>
       </array>
       <key>StartCalendarInterval</key>
       <dict>
           <key>Weekday</key>
           <integer>1</integer>
           <key>Hour</key>
           <integer>9</integer>
           <key>Minute</key>
           <integer>0</integer>
       </dict>
       <key>StandardOutPath</key>
       <string>/Users/karthiknadella/macro_kpi_update/logs/launchd.log</string>
       <key>StandardErrorPath</key>
       <string>/Users/karthiknadella/macro_kpi_update/logs/launchd_error.log</string>
   </dict>
   </plist>
   ```

2. **Load the job:**
   ```bash
   launchctl load ~/Library/LaunchAgents/com.macro_kpi.pipeline.plist
   ```

3. **Check status:**
   ```bash
   launchctl list | grep macro_kpi
   ```

## Monitoring

- **Logs:** Check `logs/` directory for pipeline execution logs
- **Output:** Check `data_outputs/` for generated CSV files
- **Errors:** Check cron/system logs if pipeline fails

## Troubleshooting

1. **Cron not running:**
   - Ensure the script has execute permissions: `chmod +x run_pipeline.sh`
   - Check cron service is running: `sudo launchctl list | grep cron`
   - Verify full path in crontab

2. **Python not found:**
   - Use full path to python3 in the script
   - Or activate virtual environment in the script

3. **Permission issues:**
   - Ensure script and directories are writable
   - Check file ownership

