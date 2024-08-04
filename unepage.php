<?php
    function encrypt($msg) {
        $res = `/bin/bash -c 'python3 encrypt.py <<< "{$msg}"'` or die("rip");
        return $res;
    }

    function decrypt($cipher) {
        $res = `/bin/bash -c 'python3 decrypt.py <<< "{$cipher}"'` or die("rip");
        return $res;
    }

    function multi_encrypt($filepath) {
        $res = `/bin/bash -c './multi_encrypt.sh 16 < "{$filepath}"'` or die("rip");
        return $res;
    }

    function multi_decrypt($filepath) {
        $res = `/bin/bash -c './multi_decrypt.sh < "{$filepath}"'` or die("rip");
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
    if (isset($_FILES["encrypt"])) {
        $filepath = $_FILES["encrypt"]["tmp_name"];
        echo multi_encrypt($filepath);
        exit(0);
    }
    if (isset($_FILES["decrypt"])) {
        $filepath = $_FILES["decrypt"]["tmp_name"];
        echo multi_decrypt($filepath);
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
