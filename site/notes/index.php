Title: Pix
<ul class='item-list'>
<?php

include '../common';

$GLOBALS['dir'] = 'files';

function timestamp_for_exif($exif) {
    if ($exif == NULL) {
        return NULL;
    }

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

    return compare_timestamps(timestamp_for_exif($a_exif), timestamp_for_exif($b_exif));
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

function item_for($timestamp, $description, $image_relative_path, $latlon) {
    $item = "<li id=" . $timestamp . " class='item'>" . "\n";
    $item = $item . "<a class='item-link' href='#" . $timestamp . "'>" . format_timestamp($timestamp) . "</a>";

    if ($image_relative_path != NULL) {
        $item = $item . "<img src=" . $image_relative_path . ">";
    }
    if ($latlon != NULL) {
        $item = $item . "<p class='item-location'>" . $latlon . '</p>';
    }
    if ($description != NULL) {
        $item = $item . "<p class='item-description'>" . $description . '</p>';
    }
    $item = $item . "</li>\n";

    return $item;
}

$files = scandir($GLOBALS['dir']);

/* Sort the files */
usort($files, 'compare_exif');



foreach ($files as $file) {
    /* Grab a relative path */
    $relative_path = $GLOBALS['dir'] ."/". $file;
    if (is_file($relative_path)) {

        $timestamp = 0;
        $description = NULL;
        $image_relative_path = NULL;
        $latlon = NULL;

        /* Determine if this is a note (text) or an image */
        /* We can do this by seeing if it has EXIF */
        $exif = exif_read_data($relative_path);
        if ($exif != false) {
            $timestamp = timestamp_for_exif($exif);
            $description = exif_get_description($exif);
            $image_relative_path = $relative_path;
            $latlon = exif_get_latlon($exif);
        }
        else {
            $handle = fopen($relative_path, 'r');
            $description = fread($handle, filesize($relative_path));
            fclose($handle);
        }

        $item = item_for($timestamp, $description, $image_relative_path, $latlon);
        echo($item);
    }
}
?>
</ul>

