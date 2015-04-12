<?php
define('user_name', 'dawx');
define('pass_wd', 's0oUU0du$P');
define('file_name', 'pre_publish.txt');
define('send_url', 'http://r.chinacache.com/content/preload');

function http_post_data($url, $data_string) {

	$ch = curl_init();
	curl_setopt($ch, CURLOPT_POST, 1);
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);
	curl_setopt($ch, CURLOPT_HTTPHEADER, array(
	'Content-Type: application/json; charset=utf-8',
	'Content-Length: ' . strlen($data_string))
	);
	ob_start();
	curl_exec($ch);
	$return_content = ob_get_contents();
	ob_end_clean();

	$return_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
	return array($return_code, $return_content);
}

    $filename = file_name;
    $username = user_name;
    $password = pass_wd;
    $handle = fopen($filename, "r");
    $count = time();
    while(!feof($handle))
    {
	$count = $count + 1;
    	$url = fgets($handle, 2048);
	#$url = str_replace(PHP_EOL, '', $url);
	$url = str_replace("\r\n","",$url); 
	$url = str_replace("\r","",$url); 
	$url = str_replace("\n","",$url); 

	echo $url;
	echo "\n";
        if ($url == "")
        {
		continue;
	}
    	$data = '{"username":"'.$username.'","password":"'.$password.'","speed": "","startTime": "","validationType": "BASIC","isOverride ": 1,"tasks":[{"id":"'.$count.'","url":"'.$url.'"}]}';
	var_dump(http_post_data(send_url, $data));
    }
	fclose($handle);
?>
