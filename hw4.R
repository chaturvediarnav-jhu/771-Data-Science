#PROBLEM 3
library(tidyverse)

#add in csv files
Populaton = read.csv("county_pop_arcos.csv")
Annual = read.csv("county_annual.csv")
Land = read.csv("land_area.csv")

#Find areas with missing data
Annual = Annual %>% filter(!is.na(BUYER_COUNTY))

#Fix Montgomery county FIPS code
Annual = Annual %>% mutate(countyfips = case_when(
  BUYER_STATE == "AR" 
  & BUYER_COUNTY == "MONTGOMERY" 
  ~ as.character("05097"), TRUE ~ as.character(countyfips)))

#Remove rows with missing county data
Annual = Annual %>% filter(!is.na(countyfips))

#Build land_area table and rename countyfips column
Land_area = Land %>% select(Areaname, STCOU, LND110210D)
Land_area = Land_area %>% rename(countyfips = STCOU)

#Left join population with land based on countyfips
County_info = left_join(Populaton, Land_area, by = "countyfips")

#checks
print(nrow(Land)) #expect 3198
print(nrow(Land_area)) #expect 3198
print(nrow(County_info)) #expect 28265
print(nrow(Populaton)) #expect to match County_info