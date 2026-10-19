# Experimental revision and controlled evaluation

Open the **[primary comparison](controlled/index.html)**. The [primary README](controlled/README.md) explains the protocol, captures, review and commands. The canonical skill remains unchanged; the baseline and experimental revision are separate frozen snapshots.

The primary study compares the same three tasks with two runs per condition: twelve design jobs and 192 expected matched screenshots. Each job receives only its task-specific contract and data. See [controlled/protocol.json](controlled/protocol.json) and [controlled/recovery.json](controlled/recovery.json) for frozen inputs and service-interruption records. The experimental revision is not promoted automatically.

The earlier cohort in this directory is an **excluded pilot**. Its shared contract listed all three apps and caused unequal workloads. Every pilot output and log remains available, but none supports the primary adoption judgment. [PILOT-EXCLUSION.json](PILOT-EXCLUSION.json) records the reason; [PILOT-README.md](PILOT-README.md) retains the earlier documentation. Its [viewer](index.html) and [assessment](assessment.json) are pilot evidence only.

The shared `tools/` scripts accept `--study controlled` or `--protocol controlled/protocol.json` as documented in the primary README. Preparation scripts were used once before each cohort and must not be rerun over the frozen inputs.
