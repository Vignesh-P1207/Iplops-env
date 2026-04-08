@echo off
setlocal ENABLEDELAYEDEXPANSION

echo ========================================
echo IPLOps-Env Validation Script (Windows)
echo ========================================
echo.

echo [1/6] Checking Docker build...
docker build -t iplops-env . >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [X] Docker build failed
    exit /b 1
)
echo [OK] Docker image builds successfully
echo.

echo [2/6] Starting container...
docker run -d -p 8000:7860 --name iplops-test iplops-env >nul 2>&1
timeout /t 5 /nobreak >nul

docker ps | findstr iplops-test >nul
if %ERRORLEVEL% NEQ 0 (
    echo [X] Container failed to start
    docker logs iplops-test
    docker rm -f iplops-test >nul 2>&1
    exit /b 1
)
echo [OK] Container started successfully
echo.

echo [3/6] Testing health endpoint...
curl -s http://localhost:8000/health | findstr /c:"healthy" >nul
if %ERRORLEVEL% NEQ 0 (
    echo [X] Health endpoint failed
    docker logs iplops-test
    docker rm -f iplops-test >nul 2>&1
    exit /b 1
)
echo [OK] Health endpoint responds correctly
echo.

echo [4/6] Testing reset endpoint (with payload)...
curl -s -X POST http://localhost:8000/reset -H "Content-Type: application/json" -d "{\"task_id\": 1}" | findstr /c:"observation" >nul
if %ERRORLEVEL% NEQ 0 (
    echo [X] Reset endpoint failed
    docker rm -f iplops-test >nul 2>&1
    exit /b 1
)
echo [OK] Reset endpoint works
echo.

echo [5/6] Testing empty reset endpoint (testing fix for missing body)...
curl -s -X POST http://localhost:8000/reset -H "Content-Length: 0" | findstr /c:"observation" >nul
if %ERRORLEVEL% NEQ 0 (
    echo [X] Empty payload Reset endpoint failed
    docker rm -f iplops-test >nul 2>&1
    exit /b 1
)
echo [OK] Empty payload Reset endpoint works
echo.

echo [6/6] Testing inference script...
python inference.py 1 > inference_output.log 2>&1
findstr /c:"RESULT" inference_output.log >nul
if %ERRORLEVEL% NEQ 0 (
    echo [X] Inference script failed
    type inference_output.log
    docker rm -f iplops-test >nul 2>&1
    del inference_output.log >nul 2>&1
    exit /b 1
)
type inference_output.log
del inference_output.log >nul 2>&1
echo [OK] Inference script runs successfully
echo.

docker rm -f iplops-test >nul 2>&1

echo ========================================
echo [OK] All validation checks passed!
echo ========================================
echo.
echo Your submission is ready for:
echo   - Docker deployment
echo   - Hugging Face Spaces
echo   - OpenEnv validation
