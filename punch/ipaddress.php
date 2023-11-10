<?php

/**
 * Gets IP address.
 */

echo 'User IP - '.$_SERVER['REMOTE_ADDR'];
echo '<br>';  

// PHP program to retrieve server’s Internet Protocol address
// Creating a variable to store the server address
$ip_server = $_SERVER['SERVER_ADDR'];
// Displaying the retrieved address
echo "Server IP Address is: $ip_server";

?>
