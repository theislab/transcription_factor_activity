import math
import os
import shutil
import tempfile
from typing import Union


def call_peaks(
    fragpaths: Union[str, list],
    macs2_path: str = None,
    outdir: str = tempfile.gettempdir(),
    broad: bool = False,
    format: str = "BED",
    effective_genome_size: int = 2.7e9,
    pval_thresh: float = 0.01,
    extsize: int = 200,
    shift: float = None,
    cap_num_peak: int = 300000,
    mem_gb: int = 4.0,
    kwargs: dict = None,
):
    """Run relaxed peak calling on pseudo bulk fragment files.

    Parameters
    ----------
        fragpaths : Union[str, list]
            Path to fragment files. If multiple paths are given, they are collapsed to a single space-separated string.
        macs2_path : str, optional
            Path to macs2 executable. If None, macs2 is searched in PATH.
        outdir : str, optional
            Output directory. Defaults to temporary directory.
        broad : bool, optional
            If True, run broad peak calling. Defaults to False.
        format : str, optional
            Format of fragment files. Defaults to "BED".
        effective_genome_size : int, optional
            Sum all of chromosome lengths. Defaults to 2.7e9.
        pval_thresh : float, optional
            P-value threshold. Defaults to 0.01.
        extsize : int, optional
            Smoothing window size.
        shift : float, optional
            Shift size. If None, shift is set to -extsize/2.
        cap_num_peak : int, optional
            Cap number of detected peaks. Defaults to 300000.
        mem_gb : int, optional
            Maximum memory in GB. Defaults to 4.0.
        kwargs : dict, optional
            Additional arguments to pass to macs2.
    Returns
    -------
    None
    """
    # find macs2
    macs2_path = macs2_path or shutil.which("macs2")

    if macs2_path is None:
        raise ValueError("macs2 not found in PATH")

    # check if fragpaths is a list
    if isinstance(fragpaths, str):
        fragpaths = [fragpaths]

    # if list of paths given, collapse to a single space-separated string
    fragpaths = " ".join(fragpaths)

    # compute shift
    if shift is None:
        shift = -int(round(float(extsize) / 2.0))

    broadstr = "--broad" if broad else ""
    nomod_str = f"--nomodel --extsize {extsize} --shift {shift}" if format == "BED" else ""

    args = ""
    for key, value in kwargs.items():
        if isinstance(value, bool):
            if value:
                args += f"--{key} "
        else:
            args += f"--{key}={value} "
    cmd = f"{macs2_path} callpeak -t {fragpaths} -f {format} -g {effective_genome_size} -p {pval_thresh} {broadstr} {nomod_str} -n {outdir} {args}"

    # run peak calling
    os.system(cmd)

    if not broad:
        # temporary files
        npeak_tmp = f"{tempfile.gettempdir()}/{os.path.basename(outdir)}.tmp"

        cmd = "".join(
            [
                f'LC_COLLATE=C sort -k 8gr,8gr {get_gnu_sort_param(mem_gb * 1024 ** 3, ratio=0.5)} "{outdir}_peaks.narrowPeak" | ',
                'awk \'BEGIN{OFS="\\t"}',
                '{$4="Peak_"NR; if ($2<0) $2=0; if ($3<0) $3=0; if ($10==-1) ',
                f"$10=$2+int(($3-$2+1)/2.0); print $0}}' > {npeak_tmp}",
            ]
        )
        os.system(cmd)

        cmd = f"head -n {cap_num_peak} {npeak_tmp} > {outdir}_peaks.narrowPeak"
        os.system(cmd)

        os.remove(npeak_tmp)

    return


# code from https://github.com/ENCODE-DCC/atac-seq-pipeline/blob/master/src/encode_lib_common.py#L283
def get_gnu_sort_param(max_mem_job, ratio=0.5):
    """Get a string of parameters for GNU sort according to maximum memory of a job/instance.

    For GNU `sort`, `-S` or `--buffer-size` defines the buffer size for the sorting,
    which defaults to max(available_mem, 1/8 * total_mem) of a node/instance.

    sort -S [SIZE][UNIT] ...

    See the following link for details.
    https://github.com/coreutils/coreutils/blob/master/src/sort.c#L1492

    This can be a problem if a job is assigned with a limited amount of memory,
    but the job runs on a large node (e.g. 256GB of memory).

    `-S` defines an INITIAL buffer size and it will automatically grow
    if more memory is needed by `sort`.


    Args:
        max_mem_job:
            Maximum amount of memory for a job/instance in bytes.
        ratio:
            Ratio to define the buffer size according to `max_mem_job`.
    """
    mem_mb = int(math.ceil(max_mem_job * ratio / (1024 * 1024)))
    return f"-S {mem_mb}M"
