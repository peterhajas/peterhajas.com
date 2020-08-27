<!DOCTYPE html>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta charset="utf-8">
<html>
<head>
<title>Hey</title>
</head>

<body>
<ul>
<?php

$GLOBALS['dir'] = 'photos';

/* Sorts by EXIF dates reversed */
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

function datetime_for_exif($exif) {
    $datetime_str = exif_read_data($relative_path)['DateTime'];
    return $datetime_str;
}

$files = scandir($GLOBALS['dir']);

/* Sort the files */
usort($files, 'compare_exif');

foreach ($files as $file) {
    /* Grab a relative path */
    $relative_path = $GLOBALS['dir'] ."/". $file;
    if (is_file($relative_path)) {
        ?>
            <li>
            <img width=300 src=<?php echo($relative_path) ?>>
            <p>
            <?php
            echo(datetime_for_exif(exif_read_data($relative_path)))
            ?>
            </p>
            </li>
        <?php
    }
}
?>
</ul>
</body>

</html>

