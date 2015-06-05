all: ci.svg ci_by_name.html ci_by_date.html clean

fill_dic_files:
	./fill_yaml_file.py -v ci.xml ./translations

ci.svg: ci.dot
	dot -Tsvg ./output/ci.dot > ./output/ci.svg

ci.dot: ci.xml
	./xml_to_graphviz.py ci.xml ./output/ci.dot

ci_by_name.html: ci.xml
	./xml_to_html_list.py ci.xml ./output/ci_by_name.html

ci_by_date.html: ci.xml
	./xml_to_html_list.py -d ci.xml ./output/ci_by_date.html

clean:
	rm -f ./output/ci.dot

mrproper: clean
	rm -f ./output/*

test:
	python -m unittest tests/test_*
