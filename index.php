<style>
* {
    margin: 0;
    padding: 0;

    box-sizing: border-box;
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
}

h1 {
    font-size: 50px;
    text-align: center;
    background-color: F5F7F8;
}

.table_body {
    min-height: 100vh;

    display: flex;
    justify-content: center;
    align-items: center;
}

table, th, td {
    padding: 1rem;
}

th {
    background-color: #04AA6D;
    color: black;
}

tr:nth-child(even) {background-color: #f2f2f2;}

table {
    width: 82vw;
    height: 90vh;
    background-color: #fff5;

    backdrop-filter: blur(7px);
    box-shadow: 0 .4rem .8rem #0005;
    border-radius: .8rem;

    overflow: hidden;
}

.table_heading {
    width: 100%;
    height: 10%;
    background-color: #fff4;
    padding: .8rem 1rem;
}

.table_body {
    width: 95%;
    height: 89%;
    background-color: #fffb;

    margin: .8rem
}

.title {
    display: inline;
    margin-right: 50px;
}

.center {
  margin: auto;
  width: 50%;
  text-align: center;
  text-decoration: underline;
  padding: 10px;
}

.background-center {
    margin: auto;
}

.inner {
    height: 90%;
    width: 90%;
}

.table-background {
    background-color: F1EFEF;
    width: 80%;
    height: 100%;
    border-radius: 3px;
}

</style>

<?php 
    $db_host = "127.0.0.1";
    $db_port = 8889;
    $db_user = "root";
    $db_password = "root";
    $db_name = "image_bot";

    $conn = mysqli_connect($db_host, $db_user, $db_password, $db_name, $db_port);

    if(! $conn ) {
        die('Could not connect: ' . mysqli_connect_error());
    }
    
    

    #Select Data from Database
    $sql = "SELECT Msg_ID, User, Text, File_Name ,Image_Link, Time FROM inputs ORDER BY Msg_ID ASC";
    $result = mysqli_query($conn, $sql);

    
    if($result->num_rows > 0) {
    echo "<section class='table_heading'><h1>Data Log</h1></section>";
    echo "<section class='table_body'><table class='inner center'>
            <tr>
                <th>Msg_ID</th>
                <th>User</th>
                <th>Text</th>
                <th>Image Link</th>
                <th>Date</th>
            </tr>
        </section>";
      while($row = mysqli_fetch_assoc($result)) {
            $image_link = $row["Image_Link"];
            echo "<tr><td>" . $row["Msg_ID"] . "</td><td>". $row["User"] ."</td><td>". $row["Text"] . "</td><td> <a href={$image_link}>" . $row["File_Name"]. "</a></td><td>" .$row["Time"]. "</td></tr>";
        }
        echo "</table></section>";
    } else {
        echo "0 Results";
    }
    
    mysqli_close($conn);
?>
