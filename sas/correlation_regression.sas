*Correlation and regression analysis - mirrors Spearman results from Python app;
*Facility: statistical procedures (PROC CORR, PROC REG);

*Spearman correlations between Revenue and the three numeric predictors;
PROC CORR DATA=work.steam SPEARMAN NOSIMPLE;
    VAR Revenue_Estimated;
    WITH 'Reviews Total'n Review_Score 'Launch Price'n;
    TITLE "Spearman Correlations with Revenue Estimated";
RUN;

*Multiple linear regression of Revenue on the three numeric predictors;
*Note: revenue is heavily right-skewed so log transform stabilises variance;
DATA work.steam_log;
    SET work.steam;
    Log_Revenue = LOG(Revenue_Estimated);
RUN;

PROC REG DATA=work.steam_log;
    MODEL Log_Revenue = 'Reviews Total'n Review_Score 'Launch Price'n;
    TITLE "Multiple Regression: Log(Revenue) on Reviews, Score, and Price";
RUN;
QUIT;
