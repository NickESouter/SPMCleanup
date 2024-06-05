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

- -input_path must be a valid directory, that will be targetted for cleanup. This script was written under the assumption that this folder contains subject-specific folders. This can include a number of different data types, we'll only be cleaning up preprocessed functional data.
  
- -method must be either 'sim_link' (simulation link mode), 'sim_copy' (simulation copy mode), or 'delete' (deletion mode).

- -preproc_label must be the stirng appended by SPM to final preprocessed data. For example, if data has gone through the modules, 'Realign: Estimate & Reslice', 'Normalise: Write', and 'Smooth', the label would (by default) be 'swr'.

### Optional arguments

- rel_path should be the relative path between a subject's folder and their preprocessed functional data, if relevant (not relevant if this data is in the first level of a subject's folder).
  
- also_keep should be a list of strings that the user also wants targeted for retention, beyond those we specify below. This list should be comma seperated, with no spaces between them.
  
- -out_path is only valid in simulation mode. If selected, simulated links to or copies of your target files will be placed in a new folder within this valid existing directory. This argument is not compatible with deletion mode.
