:: Get the absolute path of the current directory
set CURRENT_DIR=%cd%

:: Convert backslashes to forward slashes for Docker compatibility
set "CURRENT_DIR=%CURRENT_DIR:\=/%"

:: Run docker image with mounted volume
set RUN_CMD=docker run --rm -it -v "%CURRENT_DIR%:/app" -p 4200:4200 decp_preprocessing /bin/bash
echo Running docker image with command: %RUN_CMD%
%RUN_CMD%