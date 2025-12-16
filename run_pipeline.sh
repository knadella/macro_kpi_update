#!/bin/bash
# Wrapper script to run the inflation pipeline with logging

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Set up logging
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/pipeline_$(date +%Y%m%d_%H%M%S).log"

# Run the pipeline
echo "==========================================" >> "$LOG_FILE"
echo "Pipeline run started: $(date)" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

python3 pipelines/inflation_pipeline.py --source statcan >> "$LOG_FILE" 2>&1

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "Pipeline completed successfully at $(date)" >> "$LOG_FILE"
else
    echo "Pipeline failed with exit code $EXIT_CODE at $(date)" >> "$LOG_FILE"
    # Optional: Send notification (email, Slack, etc.)
fi

echo "==========================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

exit $EXIT_CODE

