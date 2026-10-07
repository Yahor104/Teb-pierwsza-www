<?php

$macierzA = [
    [1, 2, 2],
    [3, 4, 7],
    [0, 1, 6]
];
$macierzB = [
    [5, 6, 2],
    [7, 8, 4],
    [3, 9, 5]
];

function wizualizatorMacierzy(array $tablica2D): string
{
    $html = "<tbody>";
    foreach ($tablica2D as $wiersz) {
        $html .= "<tr>";
        foreach ($wiersz as $kolumna) {
            $html .= "<td>" . $kolumna . "</td>";
        }
        $html .= "</tr>";
    }
    $html .= "</tbody>";

    return $html;
}

function add(array $macierzA, array $macierzB):array{
    $macierzC = [];
    foreach ($macierzA as $i => $wiersz) {
        foreach ($wiersz as $j => $kolumna) {
            $macierzC[$i][$j] = $kolumna + $macierzB[$i][$j];
        }
    }
    return $macierzC;
}

function scale(float $scale, array $macierzA):array{
    $macierzC = [];
    foreach ($macierzA as $i => $wiersz) {
        foreach ($wiersz as $j => $kolumna) {
            $macierzC[$i][$j] = $kolumna * $scale;
        }
    }
    return $macierzC;
}

function scaleArr(array $macierzA, array $macierzB):array{
    $macierzC = [];
    foreach ($macierzA as $i => $wiersz) {
        for ($j = 0; $j < count($macierzB); $j += 1) {
            $macierzC[$i][$j] = 0;
            for ($x = 0; $x < count($macierzB); $x += 1) {
                $macierzC[$i][$j] += $wiersz[$x] * $macierzB[$x][$j];
            }
            #$macierzC[$i][$j] = $wiersz[0] * $macierzB[0][$j] + $wiersz[1] * $macierzB[1][$j];
        }
    }
    #$macierzC[0][0] = $macierzA[0][0] * $macierzB[0][0] + $macierzA[0][1] * $macierzB[1][0];
    #$macierzC[0][1] = $macierzA[0][0] * $macierzB[0][1] + $macierzA[0][1] * $macierzB[1][1];
    #$macierzC[1][0] = $macierzA[1][0] * $macierzB[0][0] + $macierzA[1][1] * $macierzB[1][0];
    #$macierzC[1][1] = $macierzA[1][0] * $macierzB[0][1] + $macierzA[1][1] * $macierzB[1][1];
    return $macierzC;
}

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        hr{
            margin: 40px 0;
        }
        .obliczenia {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 40px;
            width: 400px;
        }

        .obliczenia table {
            border-left: 1px solid;
            border-right: 1px solid;
            padding: 0 2px 0 8px;
        }

        .obliczenia td {
            width: 20px;
            padding: 2px 5px;
        }

        span{
            width: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="obliczenia">
        <table>
            <?php echo wizualizatorMacierzy($macierzA) ?>
        </table>
        <span>+</span>
        <table>
            <?php echo wizualizatorMacierzy($macierzB) ?>
        </table>
        <span>=</span>
        <table>
            <?php echo wizualizatorMacierzy(add($macierzA, $macierzB)) ?>
        </table>
    </div>
    <div class="obliczenia">
        <table>
            <?php echo wizualizatorMacierzy($macierzA) ?>
        </table>
        <span>*</span>
        <table>
            <?php echo 6 ?>
        </table>
        <span>=</span>
        <table>
            <?php echo wizualizatorMacierzy(scale(6, $macierzA)) ?>
        </table>
    </div>
    <div class="obliczenia">
        <table>
            <?php echo wizualizatorMacierzy($macierzA) ?>
        </table>
        <span>*</span>
        <table>
            <?php echo wizualizatorMacierzy($macierzB) ?>
        </table>
        <span>=</span>
        <table>
            <?php echo wizualizatorMacierzy(scaleArr($macierzA, $macierzB)) ?>
        </table>
    </div>
</body>
</html>
