*Formats, descriptive statistics, and tabular reporting;
*Facilities: user-defined formats, statistical procedures (PROC MEANS, PROC FREQ), report procedures (PROC TABULATE);

*Define revenue tier, price tier, and review score band formats;
PROC FORMAT;
    VALUE rev_tier
        0       -< 1000    = 'Under $1k'
        1000    -< 10000   = '$1k - $10k'
        10000   -< 100000  = '$10k - $100k'
        100000  - HIGH     = '$100k+';

    VALUE price_tier
        0              = 'Free-to-Play'
        0 <-< 5        = 'Under $5'
        5  -< 20       = '$5 - $20'
        20 - HIGH      = '$20+';

    VALUE score_band
        LOW -< 60  = 'Below 60'
        60  -< 75  = '60 - 74'
        75  -< 90  = '75 - 89'
        90  - HIGH = '90+';
RUN;

*Descriptive statistics for the three key numeric predictors and the outcome;
PROC MEANS DATA=work.steam N MEAN MEDIAN STD MIN MAX;
    VAR Revenue_Estimated Review_Score 'Launch Price'n 'Reviews Total'n;
    TITLE "Descriptive Statistics - Key Variables";
RUN;

*Frequency distribution of games across revenue tiers;
PROC FREQ DATA=work.steam;
    TABLES Revenue_Estimated / NOCUM;
    FORMAT Revenue_Estimated rev_tier.;
    TITLE "Game Count by Revenue Tier";
RUN;

*Median revenue and game count by review score band and price tier;
PROC TABULATE DATA=work.steam;
    CLASS Review_Score 'Launch Price'n;
    VAR Revenue_Estimated;
    FORMAT Review_Score score_band. 'Launch Price'n price_tier.;
    TABLE Review_Score ALL,
          'Launch Price'n ALL,
          Revenue_Estimated * (N MEDIAN) / BOX="Revenue by Score Band and Price Tier";
    TITLE "Revenue Summary by Review Score Band and Price Tier";
RUN;
