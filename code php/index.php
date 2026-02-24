<?php
// \n - to następna linija
// . - dodać coś w echo
// echo - wypisuje
echo "<pre>";
// także podczas wypisywania możemy dodawać, odejmować, mnożyć i td.
echo 2 . "\n"; // 2
echo 2+2 . "\n"; // 4(dodawanie)
echo 2-2 . "\n"; // 0(odejmowanie)
echo 2*2 . "\n"; // 4(mnożenie)
echo 2/2 . "\n"; // 1(dzielenie)
echo 2**4 . "\n"; // 16(podnieśienie do potęgi)
echo 5%2 . "\n"; // 1(reszta z dzielenia)
echo "Witaj świecie!" . "\n"; // Witaj świecie!
echo "</pre>";

$name; // tworzenie zmiennej name
$name = "Kamil"; // nadawanie jej wartości Kamil
echo "Witaj, " . $name; // możemy tak dodawać zmienną
echo "<br>";
echo "Witaj, $name"; // ale także możemy ją zapisać tak
echo "<br>";

echo "Czas procesora" . time(); // tak możemy dodać funkcje
echo "<br>";
echo "Czas procesora time()"; // a tak nie bo po prostu wypisze time()
?>