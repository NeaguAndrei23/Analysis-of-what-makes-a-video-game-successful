*Import the Steam Trends 2023 CSV into a SAS dataset;
*Creating a SAS dataset from external files;

PROC IMPORT DATAFILE="/home/u64485570/Project-SAS part/Steam Trends 2023.csv"
	OUT=work.steam_raw
	DBMS=CSV
	REPLACE;
	GETNAMES=YES;
	GUESSINGROWS=500;
RUN;

*Check what was imported - variable names, types and lengths;
ODS EXCLUDE EngineHost; *exclusion to remove Engine/Host Dependent Information table;
PROC CONTENTS DATA=work.steam_raw VARNUM; *set variables in order of appearance in dataset;
	TITLE "Steam Dataset - Variable Overview";
RUN;
ODS EXCLUDE NONE;

*Preview the first 10 rows to confirm the import looks correct;
PROC PRINT DATA=work.steam_raw(OBS=10) NOOBS;
	TITLE "Steam Dataset - First 10 Rows";
RUN;
