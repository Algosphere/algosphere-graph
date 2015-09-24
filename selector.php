<!DOCTYPE html>
<html>
  <head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <title>centres of interest</title>
    <style type="text/css">
	  .fixe {
      position: fixed;
	  left: 0;
	  }
	</style>

</head>
<body>
  <div class="fixe">
	<select id="lang">
	  <?php
	  	 $langs = array("german", "english", "french");
	  	 foreach ($langs as $lang)
	  	 {
	  	 echo '<option value="' . $lang . '" selected>' . $lang . '</option>';
	  	 }
      ?>

	</select>
	<select id="kind">
	  <option value="utility" selected>utility graph</option>
	  <option value="by-date">list by date</option>
	  <option value="by-name">list by name</option>
	</select>
	<input type="checkbox" id="show_objects" value="show objects">show the CI objects<br>
  </div>

  <br/>
  <br/>
  <div id="graphs">
    <?php
	   foreach ($langs as $lang)
	   {
           echo '<img id="' . $lang . 'utility" src="output/ci-official-' . $lang . '.svg" alt="' . $lang . 'graph">';
		   $link = 'output/ci-official-' . $lang . '-by-date.html';
           echo '<div id="' . $lang . 'by-date">';
           include($link);
           echo '</div>';
		   $link = 'output/ci-official-' . $lang . '-by-name.html';
           echo '<div id="' . $lang . 'by-name">';
           include($link);
           echo '</div>';

           echo '<img id="' . $lang . 'utility_objects" src="output/ci-' . $lang . '.svg" alt="' . $lang . 'graph">';
		   $link = 'output/ci-' . $lang . '-by-date.html';
           echo '<div id="' . $lang . 'by-date_objects">';
           include($link);
           echo '</div>';
		   $link = 'output/ci-' . $lang . '-by-name.html';
           echo '<div id="' . $lang . 'by-name_objects">';
           include($link);
           echo '</div>';
	   }
    ?>

  </div>

  <script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
  <script type="text/javascript">
    function hide_all() {
        $('[id=graphs]').children().hide();
    }

	function reload() {
        hide_all();
		lang = $('[id=lang]').val();
		kind = $('[id=kind]').val();
        show_objects = $('[id=show_objects]').prop('checked');
		id = lang + kind;
        if(show_objects) {
            $('[id=' + id + '_objects]').show();
        } else {
            $('[id=' + id + ']').show();
        }
	}
    reload();
	$('[id=lang]').on('change', function (){reload()});
	$('[id=kind]').on('change', function (){reload()});
    $('[id=show_objects]').on('change', function (){reload()});
  </script>
</body>
</html>
