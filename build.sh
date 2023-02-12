# build.sh - Build script for UNIX systems
validate_modules() {
	./tools/setupenv.sh
}

clean_build() {
	./tools/cleandist.sh
}

process_build() {
	pyinstaller disrichie --onefile --clean --noconfirm \
		--workpath "dist/build" --specpath "dist" --version-file "assets/version_info.txt"
}

validate_modules
clean_build
process_build