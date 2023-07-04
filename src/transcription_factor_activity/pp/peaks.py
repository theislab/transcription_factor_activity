from typing import Union
import tempfile
import os
import shutil


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
    kwargs: dict = None,
):
    """Run relaxed peak calling on pseudo bulk files.

    Parameters
    ----------

    Returns
    -------
    """
    # ENCODE: -B --SPMR --keep-dup all --call-summits
    # find macs2
    macs2_path = macs2_path or shutil.which("macs2")

    if macs2_path is None:
        raise ValueError("macs2 not found in PATH")

    # check if fragpaths is a list
    if isinstance(fragpaths, str):
        fragpaths = [fragpaths]

    # if list of paths given, collapse to a single space-separated string
    fragpaths = " ".join(fragpaths)

    broadstr = "--broad" if broad else ""
    nomod_str = f"--nomodel --extsize {extsize} --shift {shift}" if format is "BED" else ""

    kwargs = str(**kwargs) or ""
    cmd = f"{macs2_path} callpeak -t {fragpaths} -f {format} -g {effective_genome_size} -p {pval_thresh}\
          {broadstr} {nomod_str} -n {outdir}/macs2 {kwargs}"

    # run cmd
    os.system(cmd)
    return
