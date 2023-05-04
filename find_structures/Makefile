LDFLAGS="-L/usr/local/opt/flex/lib"


find_structures: find_structures.tab.c find_structures.yy.c
	gcc -o $@ $^ ${LDFLAGS} -ly -lfl
#	gcc -mmacosx-version-min=13.1 -o $@ $^ ${LDFLAGS} -ly -lfl

test: find_structures
	echo "bulge & interloop:"
	echo "..(((....)).).(..(...).)" 	| ./find_structures
	echo "no structure:"
	echo "..."							| ./find_structures
	echo "multiloop:"
	echo "..((..(.(....))...(...).))." 	| ./find_structures
	echo "pseudoknot:"
	echo "..(((..[[[[)))..]]]]." 	| ./find_structures

find_structures.tab.c: find_structures.y
	bison -d --report=all $^

find_structures.yy.c: find_structures.l
	flex -o $@ $^

install:
	sudo apt-get install -y libbison-dev


clean:
	rm -f find_structures find_structures.output find_structures.vcg
	rm -f find_structures.tab.c find_structures.tab.h
	rm -f find_structures.yy.c



LADIR="FIND_STRUCTURES"

zip:
	rm -rf ${LADIR}
	mkdir ${LADIR}
	cp find_structures.l find_structures.y Makefile ${LADIR}
	rm -f ${LADIR}.zip
	zip -r ${LADIR}.zip ${LADIR}
	rm -rf ${LADIR}
