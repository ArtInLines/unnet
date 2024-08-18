:: Typecheck
@echo Typechecking...
@call mypy unnet.py --check-untyped-defs

:: Build & install as python package
@echo Building...
@call python setup.py build
@call python setup.py install