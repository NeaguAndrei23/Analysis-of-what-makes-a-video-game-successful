*Machine learning - predict whether a game achieves high revenue;
*Facility: SAS ML (PROC HPSPLIT - decision tree, PROC HPFOREST - random forest);

*Prepare ML dataset - rename spaced variables and create binary target;
*High_Revenue = 1 if Revenue_Estimated >= 100000 (top revenue tier), else 0;
DATA work.steam_ml;
    SET work.steam;
    Reviews_Total  = 'Reviews Total'n;
    Launch_Price   = 'Launch Price'n;
    High_Revenue   = (Revenue_Estimated >= 100000);
    KEEP Revenue_Estimated Review_Score Release_Year Reviews_Total Launch_Price High_Revenue;
RUN;

*Check target class balance;
PROC FREQ DATA=work.steam_ml;
    TABLES High_Revenue / NOCUM;
    TITLE "Target Variable Distribution - High Revenue Games";
RUN;

*Decision tree using PROC HPSPLIT;
*Predicts High_Revenue from review score, price, review count, and release year;
PROC HPSPLIT DATA=work.steam_ml;
    CLASS High_Revenue;
    MODEL High_Revenue = Review_Score Launch_Price Reviews_Total Release_Year;
    GROW ENTROPY;
    PRUNE COSTCOMPLEXITY;
    TITLE "Decision Tree: Predicting High Revenue Games";
RUN;

*Random forest using PROC HPFOREST;
*Ensemble of trees - gives variable importance scores;
PROC HPFOREST DATA=work.steam_ml SEED=42;
    TARGET High_Revenue / LEVEL=NOMINAL;
    INPUT Review_Score Launch_Price Reviews_Total Release_Year / LEVEL=INTERVAL;
    TITLE "Random Forest: Predicting High Revenue Games";
RUN;
