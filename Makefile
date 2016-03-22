
all:
	/usr/lib/x86_64-linux-gnu/qt5/bin/qmake -spec linux-g++-64 -o Makefile_GUI GUI/GUI.pro
	make --file Makefile_GUI
	make --file Makefile_GUI clean
	rm Makefile_GUI
	cd CPP/Code/ && make --file Makefile release && make --file Makefile clean

clean:
	rm -f CADO
	cd CPP/Code/ && make --file Makefile clean
