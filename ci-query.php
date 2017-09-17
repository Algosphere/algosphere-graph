<?php

if (defined('ABSPATH') === false) {
    define('ABSPATH', dirname(__FILE__).'/../../../');
}

// Sets up WordPress vars and included files.
require_once ABSPATH.'wp-config.php';

header('Content-Type: text/xml');

$posts = get_posts(
    array(
        'posts_per_page'   => -1,
        'offset'           => 0,
        'category'         => '',
        'category_name'    => '',
        'orderby'          => 'date',
        'order'            => 'DESC',
        'include'          => '',
        'exclude'          => '',
        'meta_key'         => '',
        'meta_value'       => '',
        'post_type'        => 'ci',
        'post_mime_type'   => '',
        'post_parent'      => '',
        'author'     => '',
        'author_name'    => '',
        'post_status'      => 'publish',
        'suppress_filters' => true
    )
);


echo '<?xml version="1.0" ?>';
echo '<CI_list>';


foreach ($posts as $post) {
    $official = 'yes';

    echo '  <CI>';
    echo '    <id>'.$post->ID.'</id>';
    echo '    <name>'.$post->post_title.'</name>';
    echo '    <official>'.$official.'</official>';
    echo '    <date>'.$post->post_date.'</date>';
    echo '    <url>'.$post->url.'</url>';
    echo '  </CI>';
}

echo '</CI_list>';
