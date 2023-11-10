<?php
header("Content-Type:application/json");
// https://ttucis.ttu.edu.tw/chkgradstd.php?RegNo=410606120
// HTMLPurifier是PHP Pear套件，可以協助清理Cross site scription的內容
// 安裝方式(必須以root的身分為之)：
// pear channel-discover htmlpurifier.org
// pear install hp/HTMLPurifier
//ini_set('display_errors', 1); //偵錯用

require_once 'HTMLPurifier.auto.php';
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
//$ID ='F128087565';
if (isset($_GET['ID'])) $ID = $_GET['ID'];


$db_conn = connect2db($servername,$username,$password,'');
/* // Create connection for hr system use
*/

$sqlcmd = "SELECT * FROM `` WHERE recdate = '$Today' AND id='$ID' AND valid in ('Y','L')";
//echo $sqlcmd;

$signrs = querydb($sqlcmd , $db_conn);
//echo count($signrs);

$Rectime = $signrs[0]['rectime'];
$Outtime = $signrs[0]['rectime_out'];
$Recby = $signrs[0]['recby'];

//簽到/退沒
//---connect2db end---


//exit;
////unit
// JSON回應中，chinese_name註記驗證成功與否，error(驗證失敗)
// 先預設驗證失敗，驗證成功後再改成OK
//$RetMsgs = array('chinese_name'=>'error');
$ParaOK = TRUE;
// 拆解接收到的參數
//if (isset($_GET['ID'])) $RegNo = $_GET['ID'];
$RegNo = $ID;

// 其實PHP可以用下面的指令：
// if (isset($_GET)) extract($_GET, EXTR_OVERWRITE);

if (isset($RegNo)) {
    // 參數檢查
    // 先做SQL Injection及Cross site scription的消除運算
    // 此處僅為範例，請使用自己的常用的處裡方式
    $RegNo = addslashes($RegNo);
    $RegNo = xsspurify($RegNo);
    if (empty($RegNo)) $ParaOK = FALSE;

    // 透過傳遞過來的參數確認是否為該校學生，並將學生姓名及編碼後的身分證字號回傳
    if ($ParaOK) {
        //姓名編碼方式僅允許UTF-8及BIG5
        $RetMsgs['當天日期:'] = $Today;		
        //$RetMsgs['cmd:'] = $sqlcmd;
        $RetMsgs['rec時間:'] = $Rectime;
        $RetMsgs['out時間:'] = $Outtime;
        $RetMsgs['now時間:'] = $DateAndTime;
        $RetMsgs['登錄人員:'] = $Recby;//"fanli";
    }
}
// 以JSON格式回傳內容
//echo json_encode($RetMsgs);

$jsonData = json_encode($RetMsgs);
$newJsonData = preg_replace_callback('/\\\\u(\w{4})/', function ($matches) {
    return html_entity_decode('&#x' . $matches[1] . ';', ENT_COMPAT, 'UTF-8');
}, $jsonData);
echo $newJsonData;

//echo json_encode($RetMsgs, JSON_UNESCAPED_UNICODE);

//$RetMsgs2=urlencode($RetMsgs);
//echo urldecode(json_encode($RetMsgs2));

exit();

