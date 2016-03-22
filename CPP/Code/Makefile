all: release

release:
	mkdir -p build	
	cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make -j4 VERBOSE=1
	
debug:
	mkdir -p build
	cd build && cmake -DCMAKE_BUILD_TYPE=Debug .. && make -j4 VERBOSE=1

clean:
	rm -rf build
