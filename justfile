# prints this menu
default:
    @just --list

# bootstrap
install:
    @poetry install >/dev/null

# run program
run: install
    poetry run app