# Flux Processing Chain

`````{admonition} Info
:class: note
Flux processing follows the [Swiss Fluxnet Flux Processing Chain](https://www.swissfluxnet.ethz.ch/index.php/data/ecosystem-fluxes/flux-processing-chain/)
`````

## Flowchart

```{mermaid}

flowchart
	ecbin[EC binary raw data]
    eccsv[EC ASCII raw data]
    met[meteo data]
    L0F[L0 fluxes]
    L1F[L1 fluxes]
	L42F[L4.2 partitioned fluxes]
    bico[bico]
    EP[fluxrun/EddyPro]

    %% ---------------- diive
    subgraph diive_scripts
    	diive[diive]
        L2QCF[L2 quality flags]
        L32QCF[L3.2 quality flags]
        L33QCF[L3.3 quality flags]
        QCF[overall quality flag QCF]
        L31F[L3.1 fluxes]
        L31QCF[L3.1 fluxes filtered]        
	    L31Ffiltered[L3.1 fluxes filtered]
        L41F[L4.1 gap-filled fluxes]
    end
    

	ecbin --> bico --> eccsv --> EP
    EP --> L0F -- informs --> L1F
    met -- informs --> L1F
    
    L1F --> diive    
    diive --> L2QCF
    diive --> L31F
    diive --> L33QCF
	L2QCF --> L31Ffiltered
    L2QCF --> QCF
    L32QCF --> QCF
    L33QCF --> QCF
    QCF --> L31QCF
    L31F --> L31QCF        
    L31QCF -- gap-filling --> L41F
    L31F --> L31Ffiltered
    L31Ffiltered --> L32QCF
    L41F -- partitioning (NEE) --> L42F

    classDef orange fill:#FFE0B2,stroke:#E65100,stroke_width:4px,color:#E65100
    class L2QCF,L32QCF,L33QCF,QCF orange

    classDef green fill:#DCEDC8,stroke:#33691E,stroke_width:4px,color:#33691E
    class L0F,L1F,L31F,L31Ffiltered,L31QCF,L41F,L42F green

    classDef blue fill:#E1F5FE,stroke:#01579B,stroke_width:4px,color:#01579B
    class bico,EP,diive blue

    classDef white fill:#FFFFFF,stroke:#000000,stroke_width:4px,color:#000000
    class diive_scripts white

```

## Processing steps

- **Raw data EC** are the eddy covariance raw data files.
- **Level-0** are preliminary calculations, used to fine-tune final processing settings.
- **Level-1** are final flux calculations that are used in all subsequent steps.
- **Level-2** creates additional quality flags based on Level-1 output
- **Level-3.1** adds the storage term to the respective flux
- **Level-3.2** detects outliers and creates additional quality flags
- **Level-3.3** creates additional quality flags based on three different constant USTAR thresholds, previously detected by FLUXNET (Pastorello et al., 2020)
- **Level-4.1** performs gap-filling (long-term random forest)
- **Level-4.2** partitions NEE fluxes (gap-filled with random forest) into GPP and RECO
