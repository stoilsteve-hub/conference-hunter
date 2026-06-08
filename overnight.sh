#!/bin/bash
echo "Starting OVERNIGHT ORCHESTRATOR..."

echo "------------------------------------------------"
echo "PHASE 1: WAYBACK ABSOLUTE RESCUE"
echo "------------------------------------------------"
python3 wayback_absolute_rescue.py

echo "------------------------------------------------"
echo "PHASE 2: STRICT COLUMN VALIDATION"
echo "------------------------------------------------"
python3 strict_column_validator.py

echo "------------------------------------------------"
echo "PHASE 3: GENERATING FINAL REPORT"
echo "------------------------------------------------"
python3 generate_failed_report.py

echo "OVERNIGHT ORCHESTRATOR COMPLETE. Spreadsheet is ready for review."
