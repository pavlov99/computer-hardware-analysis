.PHONY: help
# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

.PHONY: pipenv
# target pipenv - install python requirements
pipenv:
	@pipenv install --dev

.PHONY: notebook
# target notebook - run jupyter notebook
notebook:
	@pipenv run jupyter notebook
