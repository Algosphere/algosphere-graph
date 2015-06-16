all: ci.svg ci_by_name.html ci_by_date.html clean

fill_dic_files:
	./fill_yaml_file.py -v ci.xml ./translations

create_graph: create_dot create_svg

.ONESHELL:
create_svg: ./output/ci*.dot
	for file in $?
	do
		echo "create $${file%.*}.svg"
		dot -Tsvg $$file > $${file%.*}.svg
	done

create_dot: ci.xml ./translations/*.yml
	./xml_to_graphviz.py -v ci.xml ./output/

ci_by_name.html: ci.xml ./translations/*.yml
	./xml_to_html_list.py ci.xml ./output/ci_by_name.html

ci_by_date.html: ci.xml ./translations/*.yml
	./xml_to_html_list.py -d ci.xml ./output/ci_by_date.html

clean:
	rm -f ./output/ci*.dot

mrproper:
	rm -f ./output/*

test:
	python -m unittest tests/test_*
