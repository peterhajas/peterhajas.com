<!DOCTYPE html>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta charset="utf-8">
<html>
<head>
<title>Hey</title>
</head>

<body>
<p>before</p>
<?php

$GLOBALS['dir'] = 'photos';

function compare_exif($a, $b) {
    $a_relative = $GLOBALS['dir'] ."/". $a;
    $b_relative = $GLOBALS['dir'] ."/". $b;

    /* Check for directories - these sort last */
    if (!is_file($a_relative)) {
        return -100;
    }
    if (!is_file($b_relative)) {
        return -100;
    }
    /* Grab EXIF */
    $a_exif = exif_read_data($a_relative);
    $b_exif = exif_read_data($b_relative);

    /* Grab dates */
    $a_date = $a_exif['DateTime'];
    $b_date = $b_exif['DateTime'];
    /* Some replacements */
    $a_date = str_replace(':', '', $a_date);
    $a_date = str_replace(' ', '', $a_date);
    $b_date = str_replace(':', '', $b_date);
    $b_date = str_replace(' ', '', $b_date);
    /* Sort backwards */
    return intval($b_date) - intval($a_date);
}

$files = scandir($GLOBALS['dir']);

/* var_dump($files); */
var_dump('hey');

/* Sort the files */
usort($files, 'compare_exif');

var_dump($files);

foreach ($files as $file) {
    /* Grab a relative path */
    $relative_path = $GLOBALS['dir'] ."/". $file;
    if (is_file($relative_path)) {
        var_dump(exif_read_data($relative_path));
        ?>
            <br>
            <img width=300 src=<?php echo($relative_path) ?>>
            <br>
        <?php
    }
}
?>
<p>after</p>
</body>

</html>

