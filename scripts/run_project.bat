@echo off
REM ============================================================
REM  Temporal Email Analysis - Build and Run Script
REM  Run this from the project root directory
REM ============================================================

echo ============================================================
echo  Temporal Email Interaction Analysis - Build and Run
echo ============================================================
echo.

REM Set environment variables
set HADOOP_HOME=C:\hadoop
set SPARK_HOME=C:\spark\spark-3.3.4-bin-hadoop3
set SBT_HOME=C:\sbt-install\sbt
set PATH=%SBT_HOME%\bin;%SPARK_HOME%\bin;%PATH%

REM Get project root (directory where this script resides)
set PROJECT_ROOT=%~dp0..
cd /d "%PROJECT_ROOT%"
echo Project root: %CD%
echo.

REM Check if dataset exists
if not exist "dataset\email-Eu-core-temporal.txt" (
    echo [ERROR] Dataset file not found!
    echo Please download from: https://snap.stanford.edu/data/email-Eu-core-temporal.txt.gz
    echo Extract and place at: dataset\email-Eu-core-temporal.txt
    echo.
    pause
    exit /b 1
)

echo [Step 1/3] Compiling Scala code with SBT...
echo.
call sbt clean compile package
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Compilation failed!
    pause
    exit /b 1
)
echo.
echo [Step 1/3] Compilation successful!
echo.

REM Find the compiled JAR
for /f "tokens=*" %%i in ('dir /b /s target\scala-2.12\temporal-email-analysis_2.12-*.jar 2^>nul') do set JAR_FILE=%%i

if not defined JAR_FILE (
    echo [ERROR] Could not find compiled JAR file.
    pause
    exit /b 1
)

echo [Step 2/3] Running Spark application...
echo JAR: %JAR_FILE%
echo.

call %SPARK_HOME%\bin\spark-submit ^
    --class com.emailanalytics.Main ^
    --master "local[*]" ^
    --driver-memory 2g ^
    --conf "spark.ui.enabled=false" ^
    --conf "spark.hadoop.hadoop.home.dir=C:\hadoop" ^
    "%JAR_FILE%" ^
    "%CD%"

if %ERRORLEVEL% neq 0 (
    echo [ERROR] Spark application failed!
    pause
    exit /b 1
)

echo.
echo [Step 2/3] Spark application completed successfully!
echo.

echo [Step 3/3] Running Python visualizations...
call "%~dp0run_visualizations.bat"

echo.
echo ============================================================
echo  ALL TASKS COMPLETED!
echo  Check the output/ directory for results.
echo ============================================================
pause
