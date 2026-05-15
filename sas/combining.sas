*Combine datasets using PROC SQL and MERGE to enrich the main dataset;
*Facility: combining datasets with SAS/SQL (PROC SQL) and MERGE;

*Step 1 - use PROC SQL to build a summary table of median revenue by release year;
PROC SQL;
    CREATE TABLE work.year_summary AS
    SELECT
        Release_Year,
        COUNT(*)              AS Game_Count,
        MEDIAN(Revenue_Estimated) AS Median_Revenue,
        MEAN(Revenue_Estimated)   AS Mean_Revenue
    FROM work.steam
    GROUP BY Release_Year
    ORDER BY Release_Year;
QUIT;

*Preview the year summary;
PROC PRINT DATA=work.year_summary NOOBS;
    TITLE "Median and Mean Revenue by Release Year";
RUN;

*Step 2 - merge the year summary back onto the game-level dataset;
*Both datasets must be sorted by the merge key first;
PROC SORT DATA=work.steam;       BY Release_Year; RUN;
PROC SORT DATA=work.year_summary; BY Release_Year; RUN;

DATA work.steam_enriched;
    MERGE work.steam (IN=a) work.year_summary (IN=b);
    BY Release_Year;
    IF a;  *keep only rows that exist in the main game dataset;
RUN;

*Show the enriched dataset - each game now carries its year's median revenue;
PROC PRINT DATA=work.steam_enriched(OBS=10) NOOBS;
    VAR Title Release_Year Revenue_Estimated Median_Revenue Game_Count;
    TITLE "Enriched Dataset - Game Revenue vs Year Median (First 10 Rows)";
RUN;
