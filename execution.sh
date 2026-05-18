#!/bin/bash

python3 addLines.py

SOLVER="simpleFoam"
DAT_FILE="postProcessing/solverInfo/0/solverInfo.dat"

echo "========================================================"
echo " Starting OpenFOAM simulation and Live Plotting"
echo "========================================================"

# 1. Clean up old postProcessing folder
if [ -d "postProcessing" ]; then
    rm -rf postProcessing
fi

# 2. Run the solver in the background
$SOLVER > log.txt &
SOLVER_PID=$!

# 3. Wait until file exists AND has enough valid data
echo "Waiting for solver to generate usable data..."

while true; do
    if [ -f "$DAT_FILE" ]; then
        # Count only non-comment lines
        VALID_LINES=$(grep -v '^#' "$DAT_FILE" | wc -l)

        if [ "$VALID_LINES" -ge 5 ]; then
            break
        fi
    fi

    # Check if solver crashed
    if ! kill -0 $SOLVER_PID 2>/dev/null; then
        echo "Error: $SOLVER crashed. Check log.txt."
        exit 1
    fi

    sleep 0.5
done

echo "Data ready! Launching live plot..."

# 4. Live plotting (robust against file updates)
gnuplot -e "
    set datafile commentschars '#';
    set logscale y;
    set format y '%.1e';
    set title 'OpenFOAM Residuals (press q to quit)';
    set xlabel 'Time / Iterations';
    set ylabel 'Residual Value';
    set grid;

    bind all 'q' 'exit';

    while (1) {
        plot '$DAT_FILE' using 1:12 title 'p' with lines, \
             '$DAT_FILE' using 1:4 title 'Ux' with lines, \
             '$DAT_FILE' using 1:7 title 'Uy' with lines;
        pause 1;
    }
"

# 5. Cleanup after plot exits
echo "Plot closed. Stopping solver..."
kill $SOLVER_PID 2>/dev/null

echo "All processes stopped successfully."

postProcess -func wallShearStress

#paraFoam