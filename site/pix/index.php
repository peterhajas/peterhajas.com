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
    $a_date = $a_exif['DateTimeOriginal'];
    $b_date = $b_exif['DateTimeOriginal'];
    /* Some replacements */
    $a_date = str_replace(':', '', $a_date);
    $a_date = str_replace(' ', '', $a_date);
    $b_date = str_replace(':', '', $b_date);
    $b_date = str_replace(' ', '', $b_date);
    /* Sort backwards */
    return intval($b_date) - intval($a_date);
}

// plh-evil: use this for comparison above
function timestamp_for_exif($exif) {
    $datetime_str = $exif['DateTimeOriginal'];
    return strtotime($datetime_str);
}

function format_timestamp($timestamp) {
    // by default, show month + day + year
    $date_format = 'F j, Y';

    $current_year = intval(date('y'));
    $timestamp_year = intval(date('y', $timestamp));
    // If it's today, show the time
    if ((time() - $timestamp) < 60 * 60 * 24) {
        $date_format = 'h:m a';
    }
    // If it's this week, show the weekday
    else if ((time() - $timestamp) < 60 * 60 * 24 * 7) {
        $date_format = 'l';
    }
    // if it's this year, show the date (month + day)
    else if ($timestamp_year == $current_year) {
        $date_format = 'F j';
    }

    return date($date_format, $timestamp);
}

function exif_get_latlon($exifdata) {
    if ($exifdata['GPSLatitude'] == NULL) {
        return NULL;
    }
    $lat_str = $exifdata['GPSLatitude'][0] . ' ' . $exifdata['GPSLatitudeRef'][0];
    $lon_str = $exifdata['GPSLongitude'][0] . ' ' . $exifdata['GPSLongitudeRef'][0];
    return $lat_str . ' ' . $lon_str;
}

function exif_get_description($exifdata) {
    return $exifdata['ImageDescription'];
}

$files = scandir($GLOBALS['dir']);

/* Sort the files */
usort($files, 'compare_exif');

foreach ($files as $file) {
    /* Grab a relative path */
    $relative_path = $GLOBALS['dir'] ."/". $file;
    if (is_file($relative_path)) {
        $exif = exif_read_data($relative_path);
        ?>
            <li>
                <img width=300 src=<?php echo($relative_path) ?>>
                <?php
                    if (exif_get_latlon($exif) != NULL) {
                ?>
                <p class='image-location'>
                <?php
                        echo(exif_get_latlon($exif));
                    }
                ?>
                </p>
                <?php
                    if (exif_get_description($exif) != NULL) {
                ?>
                <p class='image-description'>
                <?php
                        echo(exif_get_description($exif));
                    }
                ?>
                </p>
                <p class='image-timestamp'>
                <?php
                echo(format_timestamp(timestamp_for_exif($exif)));
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

