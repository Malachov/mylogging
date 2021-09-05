# List of what have been done in new versions

## 3.x - 2021
- LEVEL option addeed (DEBUG, WARNING, ERROR, FATAL). In traceback set as parameter.
- set_warnings removed. Warnings displayed only once handled inside based on new config value FILTER - "once", "always", "ignore", "error" (now also working on traceback and in logging to file).
- For filtering list of defined warning messages now warnings_filter function is defined. There is also possibility to reset user original filters with reset_warnings_filter.
- filter_warnings to be able to filter repeated warnings (if default warnings `once` filter not working)

## 2.x - 2021
- Api changed to more conventional usage - mylogging - warn, info