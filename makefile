all: create_svg_graphs create_html_lists clean

fill_dic_files:
	./fill_yaml_file.py -v ci.xml ./translations

create_html_lists: create_lists_by_name create_lists_by_date

.ONESHELL:
create_svg_graphs: ./output/ci*.dot
	for file in $?
	do
		echo "create $${file%.*}.svg"
		dot -Tsvg $$file > $${file%.*}.svg
	done

./output/ci*.dot: ci.xml ./translations/*.yml
	./xml_to_graphviz.py -v ci.xml ./output/

create_lists_by_name: ci.xml ./translations/*.yml
	./xml_to_html_list.py -v -sn -n="ci_by_name" ci.xml ./output/

create_lists_by_date: ci.xml ./translations/*.yml
	./xml_to_html_list.py -v -sd -n="ci_by_date" ci.xml ./output/

clean:
	rm -f ./output/ci*.dot

mrproper:
	rm -f ./output/*

test:
	python -m unittest tests/test_*
