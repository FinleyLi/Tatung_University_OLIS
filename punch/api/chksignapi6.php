<?php
/*
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
</head>
<body>
*/
function xsspurify($InString) {
    $config = HTMLPurifier_Config::createDefault();
    $config->set('Core.Encoding', 'UTF-8');
    $config->set('HTML.Doctype', 'XHTML 1.0 Transitional');
    $config->set('Cache.SerializerPath', '/tmp');
    $purifier = new HTMLPurifier($config);
    return $purifier->purify($InString);
}
function connect2db($dbhost, $dbuser, $dbpwd, $dbname) {
        $dbh = explode(':', $dbhost);
        $dbhost = $dbh[0];
        $dbport = $dbh[1];
        if(isset($dbh[1])&&!empty($dbh[1]))
                $dbport = "port=$dbport;";

    $dsn = "mysql:host=$dbhost;".$dbport."dbname=$dbname";
    try {
        $db_conn = new PDO($dsn, $dbuser, $dbpwd);
    }
    catch (PDOException $e) {
        echo $e->getMessage();
        die ('錯誤: 無法連接到資料庫');
    }
    $db_conn->query("SET NAMES UTF8");
    return $db_conn;
}
function querydb($querystr, $conn_id) {
    try {
        $result = $conn_id->query($querystr);
    } catch (PDOException $e) {
        die ('資料庫查詢失敗，請重試，若問題仍在，請通知管理單位。');
    }
    $rs = array();
    if ($result) $rs = $result->fetchall();
    return $rs;
}

//---connetc2db---
//Database parameters for hr system use
$DocumentRoot = $_SERVER['DOCUMENT_ROOT'];
$Today = date("Y-m-d");
$now = time();
$DateAndTime = date('h:i:s a', time());

$servername = "localhost";
$username = "";
$password = "";

// Create connection
$db_conn = connect2db($servername,$username,$password,'');

$sqlcmd = "SELECT * FROM `` WHERE recdate = '$Today' AND rectime_out='00:00:00' AND valid in ('Y','L')";
//echo $sqlcmd. "<br>";
$signrs = querydb($sqlcmd , $db_conn);
//echo count($signrs);

// --- 顯示資料 ---
// 獲得資料筆數
if ($signrs) {
    $num = count($signrs);
    // echo "db_conn 資料表有 " . $num . " 筆資料<br>";
}

echo $DateAndTime . " 未簽退" . $num . "名";
echo " :(TEST)-> ";

foreach($signrs as $row){
    echo " " . $row['recby'];
}
//</body></html>
echo " <-(END)";
?>