# SPMCleanup

## Background

SPM is a package designed for working with functional magnetic resonance imaging (fMRI) data. This includes data preprocessing, which is typically more computationally expensive and produes larger amounts of data than statistical analysis. This includes the generation of intermediate files, which likely will not be of use to most researchers.

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

- -rel_path should be the relative path between a subject's folder and their preprocessed functional data, if relevant (not relevant if this data is in the first level of a subject's folder).
  
- -also_keep should be a list of strings that the user also wants targeted for retention, beyond those we specify below. This list should be comma seperated, with no spaces between them.
  
- -out_path is only valid in simulation mode. If selected, simulated links to or copies of your target files will be placed in a new folder within this valid existing directory. This argument is not compatible with deletion mode.

### The method

The basic approach of this tool is to use the arguments provided by the user to identify final preprocessed files for each subject, and use this file naming convention to find and delete intermediate files. For example, if your preprocessed data for a given subject was in the form:

/path/to/preprocessed/data/sub-001/func/swrsub-001_bold.nii

the script would expect the following information to provided:

-input_path /path/to/preprocessed/data
-rel_path func
-preproc_label swr

From this information, the script would summise that this subject's raw data is likely in the format 'sub-001_bold.nii'. The user will be asked to confirm this is the case before proceeding, after which point the same logic will be applied to all subjects' folders. The script will be able to idnetify whether there is one or multiple raw files for a given subject.

From here, the script identifies all files within the relevant folder which contain the raw data string and deletes any that don't meet the following conditions:

* The raw file itself
* Starts with the preprocessed label (e.g., 'swr')
* Starts with 'rp_', reflecting realignment parameters for this subject
* Starts with 'mean', reflecting the mean of preprocessed data for this subject across volumes

As such, this script should never delete any files that do not contain the raw data string for a given subject. In the example proposed above, this would involve the deletion of the following files for our subject:

* rsub-001_bold.nii
* wrsub-001_bold.nii

