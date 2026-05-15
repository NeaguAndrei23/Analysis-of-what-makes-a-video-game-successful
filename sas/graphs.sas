*Graphical analysis of revenue and its predictors;
*Facility: generating graphs (PROC SGPLOT);

*Histogram of revenue on a log scale to handle extreme skew;
PROC SGPLOT DATA=work.steam;
    HISTOGRAM Revenue_Estimated;
    XAXIS TYPE=log LABEL="Revenue Estimated (log scale)";
    YAXIS LABEL="Number of Games";
    TITLE "Distribution of Estimated Revenue";
RUN;

*Median revenue by review score band;
PROC MEANS DATA=work.steam NOPRINT;
    CLASS Review_Score;
    VAR Revenue_Estimated;
    FORMAT Review_Score score_band.;
    OUTPUT OUT=work.rev_by_score MEDIAN=Median_Revenue;
RUN;

PROC SGPLOT DATA=work.rev_by_score(WHERE=(_TYPE_=1));
    VBAR Review_Score / RESPONSE=Median_Revenue STAT=mean FILLATTRS=(COLOR=steelblue);
    XAXIS LABEL="Review Score Band";
    YAXIS LABEL="Median Revenue Estimated ($)";
    FORMAT Review_Score score_band.;
    TITLE "Median Revenue by Review Score Band";
RUN;

*Median revenue by price tier;
PROC MEANS DATA=work.steam NOPRINT;
    CLASS 'Launch Price'n;
    VAR Revenue_Estimated;
    FORMAT 'Launch Price'n price_tier.;
    OUTPUT OUT=work.rev_by_price MEDIAN=Median_Revenue;
RUN;

PROC SGPLOT DATA=work.rev_by_price(WHERE=(_TYPE_=1));
    VBAR 'Launch Price'n / RESPONSE=Median_Revenue STAT=mean FILLATTRS=(COLOR=darkorange);
    XAXIS LABEL="Price Tier";
    YAXIS LABEL="Median Revenue Estimated ($)";
    FORMAT 'Launch Price'n price_tier.;
    TITLE "Median Revenue by Price Tier";
RUN;

*Scatter plot of Review Score vs Revenue Estimated;
PROC SGPLOT DATA=work.steam;
    SCATTER X=Review_Score Y=Revenue_Estimated / MARKERATTRS=(SIZE=3 COLOR=gray SYMBOL=circlefilled) TRANSPARENCY=0.7;
    LOESS X=Review_Score Y=Revenue_Estimated / LINEATTRS=(COLOR=red THICKNESS=2);
    YAXIS TYPE=log LABEL="Revenue Estimated (log scale)";
    XAXIS LABEL="Review Score";
    TITLE "Review Score vs Revenue Estimated";
RUN;
