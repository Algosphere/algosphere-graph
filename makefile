OUTPUT_DIR = ./output

all: create_svg_graphs create_html_lists clean

fill_dic_files:
	./fill_yaml_file.py -v ci.xml ./translations

create_html_lists: create_lists_by_name create_lists_by_date

create_svg_graphs: create_dot_files $(wildcard $(OUTPUT_DIR)/ci*.dot)
	$(foreach file, $?, dot -Tsvg $(file) > $(basename $(file)).svg;)
# for file in $?
# do
# 	echo "create $${file%.*}.svg"
# 	dot -Tsvg $$file > $${file%.*}.svg
# done

_create_dot_files: ci.xml ./translations/*.yml
	./xml_to_graphviz.py -v ci.xml $(OUTPUT_DIR)/

create_lists_by_name: ci.xml ./translations/*.yml
	./xml_to_html_list.py -v -sn -n="ci_by_name" ci.xml $(OUTPUT_DIR)/

create_lists_by_date: ci.xml ./translations/*.yml
	./xml_to_html_list.py -v -sd -n="ci_by_date" ci.xml $(OUTPUT_DIR)/

clean:
	rm -f $(OUTPUT_DIR)/ci*.dot

mrproper:
	rm -f $(OUTPUT_DIR)/*

test:
	python -m unittest tests/test_*
