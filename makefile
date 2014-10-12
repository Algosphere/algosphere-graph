all: ci.svg ci_by_name.html ci_by_date.html clean

ci.svg: ci.dot
	dot -Tsvg ci.dot > ci.svg

ci.dot: ci.xml
	./xml_to_graphviz.py ci.xml ci.dot

ci_by_name.html: ci.xml
	./xml_to_html_list.py ci.xml ci_by_name.html

ci_by_date.html: ci.xml
	./xml_to_html_list.py -d ci.xml ci_by_date.html

clean:
	rm -f ci.dot

mrproper: clean
	rm -f ci.svg
	rm -f ci_by_name.html
	rm -f ci_by_date.html
