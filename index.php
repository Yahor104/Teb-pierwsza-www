<?php

$condom = mysqli_connect("localhost", "root", "", "terminarz1"); // podłączenie do bazy danych

if ($condom->errno){
    exit;
};

$time = $_POST['time'];
$name = $_POST['name'];
$opis = $_POST['opis'];

$sql = "INSERT INTO `terninarz` (`id`, `time`, `name`, `opis`) VALUES (NULL, '$time', '$name', '$opis')"; //dodawanie do bazy danych

$result = mysqli_query($condom, $sql);

echo "Dodano zdarzenie";

?>
<form action="index1.php">
    <button>Wróć</button>
</form>