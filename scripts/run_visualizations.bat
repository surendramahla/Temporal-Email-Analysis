@echo off
REM ============================================================
REM  Temporal Email Analysis - Run Python Visualizations
REM ============================================================

echo ============================================================
echo  Generating Visualizations
echo ============================================================
echo.

set PROJECT_ROOT=%~dp0..
cd /d "%PROJECT_ROOT%"

echo Running visualize_activity.py ...
python visualization\visualize_activity.py
echo.

echo Running visualize_degree.py ...
python visualization\visualize_degree.py
echo.

echo Running visualize_components.py ...
python visualization\visualize_components.py
echo.

echo Running visualize_network.py ...
python visualization\visualize_network.py
echo.

echo ============================================================
echo  All visualizations generated!
echo  Charts saved in output/ subdirectories.
echo ============================================================
pause
