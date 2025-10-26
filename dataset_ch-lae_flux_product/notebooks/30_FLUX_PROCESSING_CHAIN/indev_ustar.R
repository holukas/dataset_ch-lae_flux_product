# CH-LAE
# Post-processing script for detecting USTAR thresholds


library(ggplot2)
library(REddyProc)
library(caTools)
library(dplyr)
library(viridis)
library(readr)
library(segmented)

run_id <- format(Sys.time(), "%Y%m%d%H%M%S",tz="GMT")  # Run ID
file_fluxes_meteo <- "31.3_SUBSET_NEE_QCF10_IRGA75_2005-2019.csv"
output_path <- getwd()
Sys.setenv(TZ = "GMT")

# DATA FROM FILE
filedata <- read.csv(file_fluxes_meteo, header = 1)
filedata$TIMESTAMP <- as.POSIXct(filedata$TIMESTAMP_END, format="%Y-%m-%d %H:%M:%S")
summary(filedata)
head(filedata)
colnames(filedata)



# DATA COLUMNS
EddyData.F <- filedata[FALSE]
EddyData.F$TIMESTAMP <- as.POSIXct(filedata$TIMESTAMP, format = '%m/%d/%Y %H:%M', tz = Sys.timezone())

# NEE w/ daytime QCF=0 and 1, and nighttime QCF=0, nighttime was defined as SW_IN < 20
EddyData.F$NEE <- as.numeric(as.character(filedata$NEE_L3.1_L3.2_QCF))
EddyData.F$Ustar <- as.numeric(as.character(filedata$USTAR))
EddyData.F$Rg <- as.numeric(as.character(filedata$SW_IN_T1_47_1_gfXG))
EddyData.F$Tair <- as.numeric(as.character(filedata$TA_T1_47_1_gfXG))

# cut the analysis period to the end of 2021
EddyData.F <- subset (EddyData.F, TIMESTAMP >= as.POSIXct('2004-01-01 00:30:00'))  # Date with first fluxes
EddyData.F <- subset (EddyData.F, TIMESTAMP <= as.POSIXct('2020-01-01 00:00:00'))

summary(EddyData.F)



# Initialize R5 reference class
# ============================
EddyProc.C <-sEddyProc$new('CH-LAE',  EddyData.F,
                           c('NEE', 'Rg', 'Tair', 'Ustar'), ColPOSIXTime = "TIMESTAMP")   
EddyProc.C$sSetLocationInfo(LatDeg = 47.478333, LongDeg = 8.364389, TimeZoneHour = 1)  # CH-LAE coordinates
str(EddyProc.C)
head(EddyProc.C$sDATA)
head(EddyProc.C$sTEMP)


# USTAR FILTERING
# ===============
# Use QC0 for USTAR detection
EddyProc.C$sEstimateUstarScenarios(

  # seasonFactor=seasonFactor,
  nSample = 100L,
  probs = c(0.5),
  # probs = c(0.16, 0.5, 0.84),
  NEEColName = "NEE",
  UstarColName = "Ustar",
  TempColName = "Tair",
  RgColName = "Rg",

  ctrlUstarEst = usControlUstarEst(

    ustPlateauFwd = 10,
    ustPlateauBack = 6,
    plateauCrit = 0.95,
    corrCheck = 0.5,
    firstUStarMeanCheck = 0.2,
    isOmitNoThresholdBins = TRUE,
    isUsingCPTSeveralT = FALSE,
    isUsingCPT = FALSE,
    minValidUStarTempClassesProp = 0.2,
    minValidBootProp = 0.1,
    minNuStarPlateau = 3L),

  ctrlUstarSub = usControlUstarSubsetting(
        taClasses = 6,
        UstarClasses = 30,
        swThr = 20,
        minRecordsWithinTemp = 100,
        minRecordsWithinSeason = 160,
        minRecordsWithinYear = 3000,
        isUsingOneBigSeasonOnFewRecords = TRUE)
  )


(uStarTh <- EddyProc.C$sGetEstimatedUstarThresholdDistribution())
# EddyProc.C$useSeaonsalUStarThresholds()
# EddyProc.C$useAnnualUStarThresholds()
# EddyProc.C$sGetUstarScenarios()
# thr = EddyProc.C$sGetUstarScenarios()
write.csv(uStarTh, file = paste("out_USTAR_thresholds_RP-", run_id,".csv",sep=""))

