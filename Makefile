VENV_NAME="venv"
VENV_PATH="./${VENV_NAME}/bin/activate" # ./ is optional at front

py-setup:
	@python3 -m venv $(VENV_NAME) && \
		source $(VENV_PATH) && \
		pip install --upgrade pip

day6:
	@python -um day-6.tasks;

day6-test:
	@python -um day-6.tasks test;

day7:
	@python -um day-7.tasks;

day7-test:
	@python -um day-7.tasks test;

day8:
	@python -um day-8.tasks;

day8-test:
	@python -um day-8.tasks test;

day9:
	@python -um day-9.tasks;

day9-test:
	@python -um day-9.tasks sample;

day9-test2:
	@python -um day-9.tasks sample2;

day10:
	@python -um day-10.tasks;

day10-test:
	@python -um day-10.tasks sample;

day10-test2:
	@python -um day-10.tasks sample2;

day13-test:
	@python -um day-13.tasks sample1;

day13:
	@python -um day-13.tasks input1;