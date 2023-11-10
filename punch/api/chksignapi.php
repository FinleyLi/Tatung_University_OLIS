<?php

$DocumentRoot = $_SERVER['DOCUMENT_ROOT'];

$ScriptName = explode('/',$_SERVER['PHP_SELF']);
$nArg = count($ScriptName);
$ProgName = $ScriptName[$nArg-1];

require_once($DocumentRoot . "/include/authutf8.php");
require_once($DocumentRoot . "/include/initializeutf8.php");

$ID ='';
//$ID = $_SESSION['ID'];
$Today = date("Y-m-d");
$now = time();
$db_conn = connect2db($dbinfo['hr']['host'],
            $dbinfo['hr']['user'],$dbinfo['hr']['pwd'],'hrmgm');
$PageTitle = '大同大學--差勤系統';
$Title = '差勤系統：線上簽到/退';
require_once("include/include.php");
//require_once("include/header.php");

//簽到/退沒
$IsSignIn = False;
$IsSignOut = False;
if($TodayNeedSign[0]){
        $sqlcmd = "SELECT * FROM `` WHERE recdate = '$Today' AND id='$ID' AND valid in ('Y','L')";
        $signrs = querydb($sqlcmd , $db_conn);
        if(count($signrs)>0){
                if($signrs[0]['ip']<>''){
                        $IsSignIn = True;
                        $Rectime = $signrs[0]['rectime'];
                        $Recby = $signrs[0]['recby'];
                        $IP = $signrs[0]['ip'];
                }
                if($signrs[0]['recby_out']<>'') {
                        $IsSignOut = True;
                        $Outtime = $signrs[0]['rectime_out'];
                        $Outby = $signrs[0]['recby_out'];
                        $OutIP = $signrs[0]['ip_out'];
                        if($signrs[0]['recby']=='')             $INMsg ="已簽退不能簽到";
                }
        }
}

?>
<form action="" method="POST">

  <table width="70%" height="50" border="0" cellspacing="2" cellpadding="2" align="center">
  <?php if($TodayNeedSign[0]){?>
    <tr>
      <td align="center">
        <?php
                        $signstr = strtotime($Today.' '.$s_time);
                        if(!empty($INMsg)) echo $INMsg;
                        else if($IsSignIn)  echo '簽到時間: ' . $Rectime . '　登錄人員: ' . $Recby. '　來源IP: ' . $I$
                        else if($now > $signstr){     ?>
                <?php  }     ?>
      </td>
    </tr>
    <tr>
      <td align="center">
        <?php
                        $signoutstr = strtotime($Today." ".$l_time);
                        $signoutend = strtotime($Today." ".$e_time);
                //      echo "now:$now <p> signoutstr:$signoutstr <p>  signstr:$signstr";
                        if($IsSignOut)   echo '簽退時間: ' . $Outtime . '　登錄人員: ' . $Outby . '　來源IP: ' . $Out$
                        else if($signoutstr<$now && $now < $signoutend ){         ?>
                <?php  }  ?>
      </td>
    </tr>        <?php  }else{ ?>
    <?php }?>
  </table>

<?php
    require "signin_rec.php";
exit;  ?>
