all:
	/usr/lib/x86_64-linux-gnu/qt5/bin/qmake -spec linux-g++-64 -o GUI/Makefile_GUI GUI/GUI.pro
	cd GUI/ && make --file Makefile_GUI
	mv GUI/CADO .
	cd CPP/Code/ && make --file Makefile release 

clean:
	rm -f CADO
	cd GUI/ && make --file Makefile_GUI clean
	rm -f GUI/Makefile_GUI
	cd CPP/Code/ && make --file Makefile clean
