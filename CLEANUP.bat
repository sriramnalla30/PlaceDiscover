@echo off
REM =========================================================
REM  Project Cleanup Script - SerpStack-Only v3.0
REM  Removes unnecessary files from old versions
REM =========================================================

echo.
echo =========================================================
echo   Place Search Gen AI - Project Cleanup
echo   Version: 3.0 (SerpStack-Only)
echo =========================================================
echo.
echo This script will:
echo   - Delete old Gemini/Hybrid services
echo   - Remove redundant test files
echo   - Clean up obsolete documentation
echo   - Organize remaining docs into docs/ folder
echo   - Move requirements.txt to backend/
echo.
echo Total: ~19 files will be deleted/moved
echo.
pause

echo.
echo Creating backup first...
git add .
git commit -m "Pre-cleanup backup - before v3.0 cleanup"
echo ✅ Backup committed to git
echo.

echo.
echo =========================================================
echo   Step 1: Deleting Old Backend Services
echo =========================================================
echo.

if exist "backend\services\gemini_service.py" (
    del /F "backend\services\gemini_service.py"
    echo ✅ Deleted: gemini_service.py
) else (
    echo ⚠️  Not found: gemini_service.py
)

if exist "backend\services\hybrid_search_service.py" (
    del /F "backend\services\hybrid_search_service.py"
    echo ✅ Deleted: hybrid_search_service.py
) else (
    echo ⚠️  Not found: hybrid_search_service.py
)

echo.
echo =========================================================
echo   Step 2: Deleting Redundant Test Files
echo =========================================================
echo.

if exist "test_parallel_search.py" (
    del /F "test_parallel_search.py"
    echo ✅ Deleted: test_parallel_search.py
)

if exist "test_serpstack.py" (
    del /F "test_serpstack.py"
    echo ✅ Deleted: test_serpstack.py
)

if exist "test_serpstack_simple.py" (
    del /F "test_serpstack_simple.py"
    echo ✅ Deleted: test_serpstack_simple.py
)

if exist "test_serpstack_api.py" (
    del /F "test_serpstack_api.py"
    echo ✅ Deleted: test_serpstack_api.py
)

echo ℹ️  Keeping: test_complete_serpstack.py (main test file)

echo.
echo =========================================================
echo   Step 3: Deleting Obsolete Documentation
echo =========================================================
echo.

if exist "ACCURACY_FIX.md" del /F "ACCURACY_FIX.md" & echo ✅ Deleted: ACCURACY_FIX.md
if exist "AREA_FIX.md" del /F "AREA_FIX.md" & echo ✅ Deleted: AREA_FIX.md
if exist "PARALLEL_SEARCH.md" del /F "PARALLEL_SEARCH.md" & echo ✅ Deleted: PARALLEL_SEARCH.md
if exist "PROMPT_CHANGELOG.md" del /F "PROMPT_CHANGELOG.md" & echo ✅ Deleted: PROMPT_CHANGELOG.md
if exist "IMPLEMENTATION_SUMMARY.md" del /F "IMPLEMENTATION_SUMMARY.md" & echo ✅ Deleted: IMPLEMENTATION_SUMMARY.md
if exist "FREE_SOLUTIONS.md" del /F "FREE_SOLUTIONS.md" & echo ✅ Deleted: FREE_SOLUTIONS.md
if exist "DEPLOYMENT.md" del /F "DEPLOYMENT.md" & echo ✅ Deleted: DEPLOYMENT.md

echo.
echo =========================================================
echo   Step 4: Deleting Redundant Startup Scripts
echo =========================================================
echo.

if exist "start_backend.ps1" del /F "start_backend.ps1" & echo ✅ Deleted: start_backend.ps1
if exist "start_frontend.ps1" del /F "start_frontend.ps1" & echo ✅ Deleted: start_frontend.ps1
if exist "start_backend.py" del /F "start_backend.py" & echo ✅ Deleted: start_backend.py

echo ℹ️  Keeping: START_APP.bat (all-in-one launcher)

echo.
echo =========================================================
echo   Step 5: Organizing Documentation
echo =========================================================
echo.

REM Create docs folder
if not exist "docs" mkdir docs
echo ✅ Created: docs\ folder

REM Move documentation files
if exist "SERPSTACK_ONLY.md" move /Y "SERPSTACK_ONLY.md" "docs\" >nul & echo ✅ Moved: SERPSTACK_ONLY.md → docs\
if exist "VERSION_COMPARISON.md" move /Y "VERSION_COMPARISON.md" "docs\" >nul & echo ✅ Moved: VERSION_COMPARISON.md → docs\
if exist "IMPLEMENTATION_COMPLETE.md" move /Y "IMPLEMENTATION_COMPLETE.md" "docs\" >nul & echo ✅ Moved: IMPLEMENTATION_COMPLETE.md → docs\
if exist "QUICK_SUMMARY.md" move /Y "QUICK_SUMMARY.md" "docs\" >nul & echo ✅ Moved: QUICK_SUMMARY.md → docs\
if exist "SERPSTACK_QUICKSTART.md" move /Y "SERPSTACK_QUICKSTART.md" "docs\" >nul & echo ✅ Moved: SERPSTACK_QUICKSTART.md → docs\
if exist "CHROME_TESTING_GUIDE.md" move /Y "CHROME_TESTING_GUIDE.md" "docs\" >nul & echo ✅ Moved: CHROME_TESTING_GUIDE.md → docs\
if exist "SERPSTACK_SOLUTION.md" move /Y "SERPSTACK_SOLUTION.md" "docs\" >nul & echo ✅ Moved: SERPSTACK_SOLUTION.md → docs\
if exist "CLEANUP_PLAN.md" move /Y "CLEANUP_PLAN.md" "docs\" >nul & echo ✅ Moved: CLEANUP_PLAN.md → docs\

echo.
echo =========================================================
echo   Step 6: Moving requirements.txt
echo =========================================================
echo.

if exist "requirements.txt" (
    if not exist "backend\requirements.txt" (
        move /Y "requirements.txt" "backend\" >nul
        echo ✅ Moved: requirements.txt → backend\
    ) else (
        echo ⚠️  requirements.txt already exists in backend\
    )
)

echo.
echo =========================================================
echo   Step 7: Cleaning __pycache__ folders
echo =========================================================
echo.

if exist "backend\__pycache__" rd /S /Q "backend\__pycache__" & echo ✅ Deleted: backend\__pycache__
if exist "backend\services\__pycache__" rd /S /Q "backend\services\__pycache__" & echo ✅ Deleted: backend\services\__pycache__
if exist "backend\models\__pycache__" rd /S /Q "backend\models\__pycache__" & echo ✅ Deleted: backend\models\__pycache__

echo.
echo =========================================================
echo   ✅ CLEANUP COMPLETE!
echo =========================================================
echo.
echo Summary:
echo   • Deleted old Gemini and Hybrid services
echo   • Removed 4 redundant test files
echo   • Cleaned up 7 obsolete documentation files
echo   • Deleted 3 redundant startup scripts
echo   • Organized docs into docs\ folder
echo   • Moved requirements.txt to backend\
echo   • Cleaned __pycache__ folders
echo.
echo   📁 Total files deleted/moved: ~19
echo   🎉 Project is now clean and focused!
echo.
echo Next steps:
echo   1. Run: git status (to see changes)
echo   2. Run: git add .
echo   3. Run: git commit -m "v3.0 cleanup: Removed old services and docs"
echo   4. Test: python test_complete_serpstack.py
echo   5. Start: START_APP.bat
echo.
echo =========================================================
pause
