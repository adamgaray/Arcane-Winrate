# Arcane-Winrate

This is a simple twitter bot, currently deactivated, created in Python and deployed as an AWS Lambda function. Every day at 10:00 EST, it posts the combined winrate of champs from the hit Netflix show Arcane in the LCS, LEC, LCK, and LPL.

## Winrate Calculation

Champions included: Vi, Jinx, Ekko, Singed, Caitlyn, Jayce, Heimerdinger, Viktor

A game is counted for each Arcane champion picked. For example if blue side has Viktor and Jinx, and red side has Jayce, then if blue side wins it is counted as two wins over three games.

Currently, the winrate is calculated over the LCS, LEC, LCK and LPL spring splits.
