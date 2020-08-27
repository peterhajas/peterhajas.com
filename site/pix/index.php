<ul class='image-list'>
<?php

$GLOBALS['dir'] = 'pix';

function timestamp_for_exif($exif) {
    $datetime_str = $exif['DateTimeOriginal'];
    if ($datetime_str == NULL) {
        $datetime_str = $exif['DateTime'];
    }
    if ($datetime_str == NULL) {
        return intval($exif['FileDateTime']);
    }
    return strtotime($datetime_str);
}

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
    return timestamp_for_exif($b_exif) - timestamp_for_exif($a_exif);
}

function format_timestamp($timestamp) {
    // by default, show date + time
    $date_format = 'F j h:m a, Y';

    $current_year = intval(date('y'));
    $timestamp_year = intval(date('y', $timestamp));
    // If it's today, show the time
    if ((time() - $timestamp) < 60 * 60 * 24) {
        $date_format = 'h:m a';
    }
    // If it's this week, show the weekday
    else if ((time() - $timestamp) < 60 * 60 * 24 * 7) {
        $date_format = 'l h:m a';
    }
    // if it's this year, show the date (month + day)
    else if ($timestamp_year == $current_year) {
        $date_format = 'F j h:m a';
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
            <li class='image-item'>
                <img src=<?php echo($relative_path) ?>>
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

