*Clean the Steam dataset - handle special characters and create analysis-ready columns;
*Facilities: SAS functions (COMPRESS, INPUT, YEAR, MISSING), conditional processing, creating data subsets;
*Note: variables with spaces in their names are referenced using name literals - 'variable name'n;

DATA work.steam;
	SET work.steam_raw;

	*Strip $ and commas from Revenue Estimated and convert to numeric;
	Revenue_Estimated_Num = INPUT(COMPRESS('Revenue Estimated'n, '$, '), BEST.);

	*Strip % from Reviews Score Fancy and convert to numeric;
	Review_Score = INPUT(COMPRESS('Reviews Score Fancy'n, '%'), BEST.);

	*Extract year from the already-parsed SAS date value;
	Release_Year = YEAR('Release Date'n);

	*Free-to-play games had non-numeric prices - they became missing during import;
	IF MISSING('Launch Price'n) THEN 'Launch Price'n = 0;

	*Keep only games with a positive revenue estimate - creates the analysis subset;
	IF Revenue_Estimated_Num > 0;

	DROP 'Revenue Estimated'n 'Reviews Score Fancy'n;
	RENAME Revenue_Estimated_Num = Revenue_Estimated;
RUN;

*Confirm cleaning results - row count and preview;
PROC PRINT DATA=work.steam(OBS=10) NOOBS;
	VAR Title Revenue_Estimated 'Launch Price'n Review_Score Release_Year Tags;
	TITLE "Steam Dataset - Cleaned Preview (First 10 Rows)";
RUN;
