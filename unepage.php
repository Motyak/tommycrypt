<?php
    function encrypt($msg) {
        $res = `/bin/bash -c 'python3 encrypt.py <<< "{$msg}"'` or die("rip");
        return $res;
    }

    function decrypt($cipher) {
        $res = `/bin/bash -c 'python3 decrypt.py <<< "{$cipher}"'` or die("rip");
        return $res;
    }

    /* handle POST */
    if (isset($_POST["encrypt"])) {
        echo encrypt($_POST["encrypt"]);
        exit(0);
    }
    if (isset($_POST["decrypt"])) {
        echo decrypt($_POST["decrypt"]);
        exit(0);
    }
?>

<!-- encrypt -->
<form method="GET">
    <input name="encrypt" type="text" placeholder="&lt;message&gt;" />
    <input type="submit" value="ENCRYPT" />
</form>

<!-- decrypt -->
<form method="GET">
    <input name="decrypt" type="text" placeholder="&lt;cipher&gt;" />
    <input type="submit" value="DECRYPT" />
</form>

<?php
    /* handle GET */
    if (isset($_GET["encrypt"])) {
        echo "Your cipher is: " . encrypt($_GET["encrypt"]);
        exit(0);
    }
    if (isset($_GET["decrypt"])) {
        echo "Your message is: " . decrypt($_GET["decrypt"]);
    }
?>
