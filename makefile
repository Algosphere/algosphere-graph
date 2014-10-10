all: ci.svg clean

ci.svg: ci.dot
	dot -Tsvg ci.dot > ci.svg

ci.dot: ci.xml
	./xml_to_graphviz.py ci.xml ci.dot

clean:
	rm -f ci.dot

mrproper: clean
	rm -f ci.svg
