*Use arrays to flag each game across multiple performance metrics in one pass;
*Facility: using arrays;

DATA work.steam_flags;
    SET work.steam;

    *Define thresholds - median values used as the cut-off for "high" performance;
    ARRAY metrics[3]   Revenue_Estimated Review_Score 'Launch Price'n;
    ARRAY thresholds[3] _TEMPORARY_ (10000, 75, 10);
    ARRAY flags[3]     Flag_Revenue Flag_Score Flag_Price;

    *Flag each metric as 1 (above threshold) or 0 (at or below);
    DO i = 1 TO 3;
        IF metrics[i] > thresholds[i] THEN flags[i] = 1;
        ELSE flags[i] = 0;
    END;

    *Count how many metrics the game scores "high" on;
    High_Count = SUM(OF flags[*]);

    DROP i;
RUN;

*Summary: how many games score high on 0, 1, 2, or all 3 metrics;
PROC FREQ DATA=work.steam_flags;
    TABLES High_Count / NOCUM;
    TITLE "Games by Number of High-Performance Metrics (Revenue, Score, Price)";
RUN;

*Mean revenue broken down by how many metrics a game scored high on;
PROC MEANS DATA=work.steam_flags MEAN MEDIAN N;
    CLASS High_Count;
    VAR Revenue_Estimated;
    TITLE "Mean and Median Revenue by High-Performance Count";
RUN;
