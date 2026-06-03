@rem Gradle wrapper script for Windows
@if "%DEBUG%"=="" @echo off
@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%"=="" set DIRNAME=.
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%

set CLASSPATH=%APP_HOME%\gradle\wrapper\gradle-wrapper.jar

if not defined JAVA_HOME goto error

java %JAVA_OPTS% -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*
goto end

:error
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
exit /b 1

:end
if "%ERRORLEVEL%"=="0" goto mainEnd
exit /b 1
:mainEnd
