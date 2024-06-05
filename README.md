# SPMCleanup

## Background

SPM is a package designed for working with functional magnetic resonance imaging (fMRI) data. This includes data preprocessing, which is typically more computationally expensive and produes larger amounts of data than statistical analysis. This includes the generation of intermediary files, which likely will not be of use to most researchers.

Servers use energy not only to process data, but also to store it. Additionally, filling servers with data increases the need to produce and purchase additional hardware to accomodate new projects. In both of these ways, the accumulation of unneeded 'junk' data contributes to the carbon footprint of research computing.

## Usage

As such, we provide here a script that can be used to automatically identify and delete 'junk' files produced by SPM during preprocessing, used as follows:

```
SPMCleanup.py -input_path <path to folder containing subjects' preprocessed functional output>
-method <'sim_link'/'sim_copy'/'delete'>
-preproc_label <string appended to the front of final preprocessed output>
-rel_path <path to preprocessed data within each subject's individual folder>
-also_keep <keep1,keep2,keep3>
-out_path <path to simulation output directory>

```

### Compulsory arguments


### Optional arguments
