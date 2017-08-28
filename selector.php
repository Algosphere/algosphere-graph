<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->

    <!-- FAVICON -->
    <link rel="shortcut icon" href="#" />

    <!-- BOOTSTRAP -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

    <!-- STYLE -->
    <link href="style.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->

    <title>centres of interest</title>
  </head>
  <body>
    <nav class="navbar navbar-default navbar-static-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <p class="navbar-text" style="padding-left: 10px;">Algosphere Alliance's centers of interest graphical representation</p>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <form class="navbar-form navbar-left">
              <div class="form-group">
                <label for="lang">Language </label>
                <select id="lang" class="form-control">
                  <?php
                  $langs = array("german", "english", "french");
                  foreach ($langs as $lang)
                  {
                      echo '<option value="' . $lang . '" selected>' . $lang . '</option>';
                  }
                  ?>
                </select>
              </div>
              <!-- <div class="form-group">
                   <label for="kind">Type </label>
                   <select id="kind" class="form-control">
                   <option value="utility" selected>utility graph</option>
                   <option value="by-date">list by date</option>
                   <option value="by-name">list by name</option>
                   </select>
                   </div> -->
              <div class="checkbox">
                <label>
                  <input type="checkbox" id="show_objects" value="show objects"><span> Show the CI objects</span>
                </label>
              </div>
            </form>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div class="container">
      <div id="graphs">
        <?php
        foreach ($langs as $lang) {
            echo '<object id="'.$lang.'utility" data="output/ci-official-'.$lang.'.svg" type="image/svg+xml"></object>';
            $link = 'output/ci-official-'.$lang.'-by-date.html';
            echo '<div id="'.$lang.'by-date">';
            include($link);
            echo '</div>';
            $link = 'output/ci-official-'.$lang.'-by-name.html';
            echo '<div id="'.$lang.'by-name">';
            include($link);
            echo '</div>';

            echo '<object id="'.$lang.'utility_objects" data="output/ci-'.$lang.'.svg" type="image/svg+xml"></object>';
            $link = 'output/ci-'.$lang.'-by-date.html';
            echo '<div id="'.$lang.'by-date_objects">';
            include($link);
            echo '</div>';
            $link = 'output/ci-'.$lang.'-by-name.html';
            echo '<div id="'.$lang.'by-name_objects">';
            include($link);
            echo '</div>';
        }
        ?>
      </div>
    </div> <!-- container -->

    <!-- Javascript -->
    <script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
    <script type="text/javascript">
     function hide_all() {
         $('[id=graphs]').children().hide();
     }

     function reload() {
         hide_all();
         lang = $('[id=lang]').val();
         kind = $('[id=kind]').val();
         if(kind == null) {
             kind = "utility"
         }

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

    <!-- Bootstrap -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

    <script type="text/javascript">
     // fondu dropdowns
     $('.navbar .dropdown').hover(function() {
         $(this).find('.dropdown-menu').first().stop(true, true).fadeIn(150);
     }, function() {
         $(this).find('.dropdown-menu').first().stop(true, true).fadeOut(150);
     });
    </script>
  </body>
</html>
