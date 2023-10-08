
.PHONY: build, init
compile:
	colcon build --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

init:
	$(source install/local_setup.zsh)
