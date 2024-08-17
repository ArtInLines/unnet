:: Setup virtual environment
@echo Setting up environment
@call venv\Scripts\activate.bat

:: Install dependencies
@echo Installing dependencies...
@call pip install -r requirements.txt