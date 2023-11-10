<?php

/**
 * Copyright 2016 LINE Corporation
 *
 * LINE Corporation licenses this file to you under the Apache License,
 * version 2.0 (the "License"); you may not use this file except in compliance
 * with the License. You may obtain a copy of the License at:
 *
 *   https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

require_once('./LINEBotTiny.php');

$channelAccessToken = '';
$channelSecret = '';

//--start(test function)--
/* (1)
 * Subject: PHP實作Line bot
 * http://wwwang.tw/blog/php-%E5%AF%A6%E4%BD%9Cline-bot/
 */
/*
//讀取資訊
$HttpRequestBody = file_get_contents('php://input');
$HeaderSignature = $_SERVER['HTTP_X_LINE_SIGNATURE'];
//輸出json需將後方全部註解
file_put_contents('log.txt', $HttpRequestBody);
*/

// (2)ip address
$ip_add = $_SERVER['REMOTE_ADDR'];

/* (3)
 * Subject: 用 PHP 讀取或解析 CSV 檔案
 * https://www.delftstack.com/zh-tw/howto/php/read-parse-csv-in-php/
 */
/*
$file = "contacts.csv";
$openfile = fopen($file, "r");
$readcsv  = fread($openfile, filesize($file));
*/

/* (4)
 * 用 PHP 實現 Line Message API 接收系統訊息
 * https://blog.toright.com/posts/5727/%e7%94%a8-php-%e5%af%a6%e7%8f%be-line-message-api-%e6%8e%a5%e6%94%b6%e7%b3%bb%e7%b5%b1%e8%a8%8a%e6%81%af.html
 */
$dbFilePath = 'line-db.json';        // user info database file path

if (!file_exists($dbFilePath)) {
   file_put_contents($dbFilePath, json_encode(['user' => []]));
}
$db = json_decode(file_get_contents($dbFilePath), true);

/* (5)
 * 用curl只顯示Header資訊
 */
/*
// $url = "https://ttucis.ttu.edu.tw/chkgradstd.php?ID=710106020";
$url = "https://ttucis.ttu.edu.tw/hrmgm/chksignapi2.php?ID=1";
$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$result = curl_exec($ch);

curl_close($ch);
echo $result;
*/

/*(6)
 * exec - Manual - PHP
 * https://www.php.net/manual/en/function.exec.php
 */
// $output=null;
// $retval=null;
// exec('whoami', $output, $retval);

//--end(test function)--

$client = new LINEBotTiny($channelAccessToken, $channelSecret);
foreach ($client->parseEvents() as $event) {

    switch ($event['type']) {
        case 'message':
            $message = $event['message'];

            /* (4) Line Message API
             * To Be Continuum...
             */
            $userId = $event['source']['userId'];
            // bot dirty logic
            if (!isset($db['user'][$userId])) {
                $db['user'][$userId] = [
                    'userId' => $userId,
                    'timestamp' => $event['timestamp']
                ];
                file_put_contents($dbFilePath, json_encode($db));
                // $message = 'Login Success! Wellcome!';
            } else {
                // $message = 'Input password please.';
            }
            //--end(4) Line Message API--

            //--start(linebot echo)--
            if ($event['message']['text'] === 'id') {
                $echo_text = $message['id'];
            } elseif ($event['message']['text'] === 'uid') {
                $echo_text = $event['source']['userId'];
                // $echo_text = 'Returned UID: '.$userId;
            // } elseif ($event['message']['text'] === 'csv') {
            //     $echo_text = $readcsv;
            // } elseif ($event['message']['text'] === 'curl') {
            //     $echo_text = $result;
            // } elseif ($event['message']['text'] === 'whoami') {
            //     $echo_text = "Returned with status $retval and output:\n".print_r($output);
            } elseif ($event['message']['text'] === 'ip') {
                $echo_text = $ip_add;
            } else {
/*
$url = "http://example.com/";
$data_array = array("acc"=>"F", "pwd"=>"123");
$url = $url . http_build_query($data_array); 
// 組出 http://sample.com/?acc=F&pwd=123
*/
                $url_dcert = "";
                $studentid = $event['message']['text'];
                $data_array = array("ID"=>$studentid);
                $url_dcert = $url_dcert . http_build_query($data_array);
                $ch = curl_init();

                curl_setopt($ch, CURLOPT_URL, $url_dcert);
                curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                $result = curl_exec($ch);

                curl_close($ch);
                echo $result;

                $echo_text = 'echo 我收到你的訊息了' . $result;
            }
            //--end(linebot echo)--

            switch ($message['type']) {
                case 'text':
                    $client->replyMessage([
                        'replyToken' => $event['replyToken'],
                        'messages' => [
                            [
                                'type' => 'text',
                                'text' => $echo_text //--(linebot echo)--
                            ]
                        ]
                    ]);
                    break;
                default:
                    error_log('Unsupported message type: ' . $message['type']);
                    break;
            }
            break;
        default:
            error_log('Unsupported event type: ' . $event['type']);
            break;
    }
};
